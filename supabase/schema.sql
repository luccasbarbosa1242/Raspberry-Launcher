-- Run in the Supabase SQL editor of YOUR project, not in local SQLite.
-- ONLY the authenticated user can see their own statistics and preferences.
-- No service_role key should ever be distributed with the launcher.

create table if not exists public.launcher_game_stats (
  user_id uuid not null references auth.users(id) on delete cascade,
  game_id text not null,
  favorite boolean not null default false,
  play_time bigint not null default 0 check (play_time >= 0),
  last_played timestamptz,
  primary key (user_id, game_id)
);

create table if not exists public.launcher_preferences (
  user_id uuid primary key references auth.users(id) on delete cascade,
  theme text not null default 'dark' check (theme in ('dark', 'light', 'system')),
  music_volume integer not null default 50 check (music_volume between 0 and 100)
);

create table if not exists public.launcher_event_receipts (
  user_id uuid not null references auth.users(id) on delete cascade,
  event_id uuid not null,
  received_at timestamptz not null default now(),
  primary key (user_id, event_id)
);

alter table public.launcher_game_stats enable row level security;
alter table public.launcher_preferences enable row level security;
alter table public.launcher_event_receipts enable row level security;

revoke all on public.launcher_game_stats from public, anon, authenticated;
revoke all on public.launcher_preferences from public, anon, authenticated;
revoke all on public.launcher_event_receipts from public, anon, authenticated;

grant select on public.launcher_game_stats to authenticated;
grant select on public.launcher_preferences to authenticated;

drop policy if exists launcher_stats_owner_read on public.launcher_game_stats;
create policy launcher_stats_owner_read on public.launcher_game_stats
  for select to authenticated using ((select auth.uid()) = user_id);

drop policy if exists launcher_preferences_owner_read on public.launcher_preferences;
create policy launcher_preferences_owner_read on public.launcher_preferences
  for select to authenticated using ((select auth.uid()) = user_id);

-- Event receipts are internal and never directly exposed to clients.
-- All writes are atomic and idempotent even if the client retries after a timeout.
create or replace function public.launcher_apply_events(p_events jsonb)
returns integer
language plpgsql security definer
set search_path = ''
as $$
declare
  current_user_id uuid := auth.uid();
  entry jsonb;
  inserted_id uuid;
  event_kind text;
  game text;
  seconds integer;
  count_applied integer := 0;
  selected_theme text;
  selected_volume integer;
begin
  if current_user_id is null then
    raise exception 'Authentication required' using errcode = '28000';
  end if;
  if jsonb_typeof(p_events) is distinct from 'array'
    or jsonb_array_length(p_events) > 50 then
    raise exception 'Expected a batch of at most 50 events';
  end if;
  for entry in
    select e.value from jsonb_array_elements(p_events)
    with ordinality as e(value, number) order by e.number loop
    if jsonb_typeof(entry) is distinct from 'object'
       or (entry->>'id') is null
       or (entry->>'kind') not in ('favorite','played','started','preferences') then
      raise exception 'Invalid event';
    end if;
    event_kind := entry->>'kind';
    game := entry->>'game_id';
    if event_kind <> 'preferences'
       and (game is null or length(game) < 1 or length(game) > 180) then
      raise exception 'Invalid game identifier';
    end if;
    if event_kind = 'played' then
      if jsonb_typeof(entry->'seconds') is distinct from 'number' then
        raise exception 'Invalid play time';
      end if;
      seconds := (entry->>'seconds')::integer;
      if seconds <= 0 or seconds > 86400 then
        raise exception 'Invalid play time';
      end if;
    end if;
    if event_kind = 'favorite'
       and jsonb_typeof(entry->'favorite') is distinct from 'boolean' then
      raise exception 'Invalid favorite';
    end if;
    if event_kind = 'preferences' then
      selected_theme := entry->>'theme';
      if selected_theme is not null
         and selected_theme not in ('dark','light','system') then
        raise exception 'Invalid theme';
      end if;
      if entry ? 'music_volume' then
        if jsonb_typeof(entry->'music_volume') is distinct from 'number' then
          raise exception 'Invalid volume';
        end if;
        selected_volume := (entry->>'music_volume')::integer;
        if selected_volume < 0 or selected_volume > 100 then
          raise exception 'Invalid volume';
        end if;
      else
        selected_volume := null;
      end if;
    end if;

    inserted_id := null;
    insert into public.launcher_event_receipts(user_id, event_id)
      values (current_user_id, (entry->>'id')::uuid)
      on conflict do nothing returning event_id into inserted_id;
    if inserted_id is null then
      continue;
    end if;
    count_applied := count_applied + 1;

    if event_kind = 'favorite' then
      insert into public.launcher_game_stats(user_id, game_id, favorite)
        values(current_user_id, game, (entry->>'favorite')::boolean)
      on conflict(user_id, game_id) do update set favorite = excluded.favorite;
    elsif event_kind = 'played' then
      insert into public.launcher_game_stats(user_id, game_id, play_time, last_played)
        values(current_user_id, game, seconds,
               coalesce((entry->>'occurred_at')::timestamptz, now()))
      on conflict(user_id, game_id) do update
        set play_time = public.launcher_game_stats.play_time + excluded.play_time,
            last_played = greatest(public.launcher_game_stats.last_played, excluded.last_played);
    elsif event_kind = 'started' then
      insert into public.launcher_game_stats(user_id, game_id, last_played)
        values(current_user_id, game,
               coalesce((entry->>'occurred_at')::timestamptz, now()))
      on conflict(user_id, game_id) do update
        set last_played = greatest(public.launcher_game_stats.last_played, excluded.last_played);
    else
      insert into public.launcher_preferences(user_id, theme, music_volume)
        values(current_user_id, coalesce(selected_theme,'dark'), coalesce(selected_volume,50))
      on conflict(user_id) do update
        set theme = coalesce(selected_theme, public.launcher_preferences.theme),
            music_volume = coalesce(selected_volume, public.launcher_preferences.music_volume);
    end if;
  end loop;
  return count_applied;
end;
$$;

revoke execute on function public.launcher_apply_events(jsonb) from public, anon;
grant execute on function public.launcher_apply_events(jsonb) to authenticated;

-- Additional production hardening: enable Supabase Auth email confirmation,
-- rate limiting, SMTP and abuse protection in the Supabase dashboard.

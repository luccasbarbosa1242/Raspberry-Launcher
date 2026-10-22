-- Assertions execute as ordinary unprivileged API roles with fake JWT claims.
set role authenticated;
select set_config('request.jwt.claim.sub', 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa', false);
select public.launcher_apply_events('[
 {"id":"11111111-1111-4111-8111-111111111111",
  "kind":"played","game_id":"daggerfall","seconds":12,
  "occurred_at":"2026-10-20T20:00:00Z"},
 {"id":"22222222-2222-4222-8222-222222222222",
  "kind":"favorite","game_id":"daggerfall","favorite":true},
 {"id":"33333333-3333-4333-8333-333333333333",
  "kind":"preferences","theme":"light","music_volume":37}
]'::jsonb);

-- Repeating a previously accepted batch cannot double-count play time.
select public.launcher_apply_events('[
 {"id":"11111111-1111-4111-8111-111111111111",
  "kind":"played","game_id":"daggerfall","seconds":12}
]'::jsonb);
do $$
declare total bigint;
declare ratio integer;
begin
  select play_time into total from public.launcher_game_stats
  where user_id='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'
    and game_id='daggerfall';
  if total <> 12 then raise exception 'duplicate or lost seconds: %', total; end if;
  select count(*) into ratio from public.launcher_game_stats;
  if ratio <> 1 then raise exception 'unexpected number of visible games'; end if;
  if (select theme from public.launcher_preferences limit 1) <> 'light'
     then raise exception 'preferences did not persist'; end if;
  -- Direct writes must be impossible: the RPC is the only mutation surface.
  begin
    update public.launcher_game_stats set play_time=999;
    raise exception 'direct update unexpectedly allowed';
  exception when insufficient_privilege then null;
  end;
end;
$$;

-- Second account has zero access to first account's data.
select set_config('request.jwt.claim.sub', 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb', false);
do $$
begin
  if (select count(*) from public.launcher_game_stats) <> 0 then
    raise exception 'RLS leaked first account game stats';
  end if;
  if (select count(*) from public.launcher_preferences) <> 0 then
    raise exception 'RLS leaked first account preferences';
  end if;
end;
$$;
select public.launcher_apply_events('[
 {"id":"44444444-4444-4444-8444-444444444444",
  "kind":"played","game_id":"daggerfall","seconds":7}
]'::jsonb);
do $$
begin
  if (select play_time from public.launcher_game_stats limit 1) <> 7 then
    raise exception 'Second account stats incorrect';
  end if;
end;
$$;

reset role;
set role anon;
do $$
begin
  begin
    perform public.launcher_apply_events('[]'::jsonb);
    raise exception 'Anonymous caller unexpectedly allowed';
  exception when insufficient_privilege then null;
  end;
end;
$$;
reset role;

-- Inspect totals as test administrator to confirm both records exist.
do $$
begin
  if (select count(*) from public.launcher_game_stats) <> 2 then
    raise exception 'Wrong total game state row count';
  end if;
  if (select play_time from public.launcher_game_stats
      where user_id='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa') <> 12 then
    raise exception 'First account changed during second account write';
  end if;
end;
$$;

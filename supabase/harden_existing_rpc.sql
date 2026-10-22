-- Upgrade a deployment of raspberry_launcher_online_accounts_v1.
-- Preserves all rows, event receipts, and function behavior.
BEGIN;
create schema if not exists launcher_private;
revoke all on schema launcher_private from public, anon;
grant usage on schema launcher_private to authenticated;
alter function public.launcher_apply_events(jsonb) set schema launcher_private;
revoke execute on function launcher_private.launcher_apply_events(jsonb) from public, anon;
grant execute on function launcher_private.launcher_apply_events(jsonb) to authenticated;
create or replace function public.launcher_apply_events(p_events jsonb)
returns integer
language sql security invoker
set search_path = ''
as 'select launcher_private.launcher_apply_events(p_events);';
revoke execute on function public.launcher_apply_events(jsonb) from public, anon;
grant execute on function public.launcher_apply_events(jsonb) to authenticated;
COMMIT;

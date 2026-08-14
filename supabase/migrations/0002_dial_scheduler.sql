-- ============================================================================
-- Salon Malone — dial scheduler (pg_cron + pg_net)
--
-- HOW TO APPLY: replace __CRON_SECRET__ below with the CRON_SECRET value from
-- .env.local / Vercel, then paste the whole file into the Supabase SQL Editor.
-- `npm run setup:scheduler` prints a filled-in copy you can paste directly.
--
-- WHY THIS EXISTS: ARCHITECTURE.md asks for a dial run every 5 minutes. Vercel
-- rejects any sub-daily cron on a Hobby plan, so the schedule lives here instead.
-- Postgres calls the app; the app still owns every compliance decision. If you
-- later move to Vercel Pro, unschedule the job (bottom of this file) and put the
-- */5 schedule back in vercel.json — nothing else changes.
--
-- SAFE TO RUN EVERY 5 MINUTES, AROUND THE CLOCK. The call-window gate lives in
-- claim_contacts_for_dialing, evaluated per client in that client's own
-- timezone, so a 03:00 tick claims nothing. The scheduler has no say in who
-- gets dialed — it only asks the app to look.
--
-- Idempotent: re-running re-points the secret and replaces the job.
-- ============================================================================

create extension if not exists pg_cron;
create extension if not exists pg_net;

-- ----------------------------------------------------------------------------
-- The bearer token lives in Vault, not inline in the job command.
--
-- cron.job.command is readable by anyone who can query the cron schema, and this
-- token authorizes real outbound phone calls. Vault keeps it encrypted at rest
-- and the job resolves it at execution time.
-- ----------------------------------------------------------------------------
do $$
declare
  v_id uuid;
begin
  select id into v_id from vault.secrets where name = 'salon_malone_cron_secret';

  if v_id is null then
    perform vault.create_secret(
      '__CRON_SECRET__',
      'salon_malone_cron_secret',
      'Bearer token for POST /api/cron/dial. Must equal CRON_SECRET in Vercel.'
    );
  else
    perform vault.update_secret(
      v_id,
      '__CRON_SECRET__',
      'salon_malone_cron_secret',
      'Bearer token for POST /api/cron/dial. Must equal CRON_SECRET in Vercel.'
    );
  end if;
end $$;

-- ----------------------------------------------------------------------------
-- Replace the job rather than stacking duplicates.
-- ----------------------------------------------------------------------------
do $$
begin
  if exists (select 1 from cron.job where jobname = 'salon-malone-dial') then
    perform cron.unschedule('salon-malone-dial');
  end if;
end $$;

select cron.schedule(
  'salon-malone-dial',
  '*/5 * * * *',
  $job$
  select net.http_get(
    url     := 'https://www.startup25.com/api/cron/dial',
    headers := jsonb_build_object(
                 'Authorization',
                 'Bearer ' || (
                   select decrypted_secret
                     from vault.decrypted_secrets
                    where name = 'salon_malone_cron_secret'
                 )
               ),
    -- pg_net is fire-and-forget: this queues the request and returns an id
    -- immediately, so a slow dial run never holds a Postgres worker open.
    timeout_milliseconds := 50000
  );
  $job$
);

-- ============================================================================
-- OPERATING IT
--
--   -- is the job scheduled?
--   select jobid, jobname, schedule, active from cron.job;
--
--   -- did the last 10 ticks fire, and did they succeed?
--   select start_time, status, return_message
--     from cron.job_run_details
--    where jobname = 'salon-malone-dial'
--    order by start_time desc
--    limit 10;
--
--   -- what did the app actually answer? (200 + a JSON body = healthy)
--   select created, status_code, content
--     from net._http_response
--    order by created desc
--    limit 10;
--
--   -- pause dialing entirely, without deleting the job
--   update cron.job set active = false where jobname = 'salon-malone-dial';
--
--   -- remove it (e.g. after moving to Vercel Pro)
--   select cron.unschedule('salon-malone-dial');
-- ============================================================================

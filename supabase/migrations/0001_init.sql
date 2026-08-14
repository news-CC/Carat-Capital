-- ============================================================================
-- Salon Malone — schema v1
--
-- HOW TO APPLY: paste this whole file into the Supabase SQL Editor and run it.
-- (Or: npm run db:migrate -> scripts/apply-migration.mjs.)
--
-- It is idempotent: every statement is `if not exists` / `create or replace` /
-- drop-then-create, so re-running it is safe and never drops data.
--
-- Five tables. No more. If a feature needs a sixth, it is not in v1.
-- ============================================================================

create extension if not exists pgcrypto;

-- ----------------------------------------------------------------------------
-- clients — the salon or med spa paying us
-- ----------------------------------------------------------------------------
create table if not exists public.clients (
  id                 uuid primary key default gen_random_uuid(),
  name               text not null,
  contact_name       text,
  contact_email      text not null,
  contact_phone      text,
  offer_text         text not null,
  timezone           text not null default 'America/New_York',
  vertical           text not null default 'salon',      -- salon | medspa
  avg_ticket_cents   integer not null default 12000,
  stripe_status      text not null default 'trialing',   -- trialing | active | past_due | canceled
  stripe_customer_id text,
  booking_phone      text,                               -- the real number Malone reads on voicemail
  active             boolean not null default true,
  created_at         timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- contacts — uploaded list rows. phone is E.164, or NULL when unusable.
-- ----------------------------------------------------------------------------
create table if not exists public.contacts (
  id                   uuid primary key default gen_random_uuid(),
  client_id            uuid not null references public.clients (id) on delete cascade,
  campaign             text not null default 'default',
  name                 text,
  first_name           text,
  phone                text,
  phone_raw            text,
  email                text,
  consent              boolean not null default false,
  last_visit           date,
  lifetime_value_cents integer,
  status               text not null default 'pending',
  scrub_reason         text,
  attempts             integer not null default 0,
  claimed_at           timestamptz,
  created_at           timestamptz not null default now(),
  -- Upload de-dupe key (upsert target). NULLs are distinct in Postgres, which is
  -- what we want: unusable numbers can pile up without blocking each other.
  constraint contacts_client_campaign_phone_key unique (client_id, campaign, phone)
);

-- ----------------------------------------------------------------------------
-- calls — one row per dial attempt. Every attempt writes a row, even failures.
-- ----------------------------------------------------------------------------
create table if not exists public.calls (
  id               uuid primary key default gen_random_uuid(),
  contact_id       uuid references public.contacts (id) on delete cascade,
  client_id        uuid references public.clients (id) on delete cascade,
  vapi_call_id     text unique,                          -- webhook idempotency key
  outcome          text not null default 'dialing',
  duration_seconds integer,
  cost_usd         numeric(10, 4),
  transcript_url   text,
  recording_url    text,
  summary          text,
  ended_reason     text,
  started_at       timestamptz,
  ended_at         timestamptz,
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- suppression — global do-not-contact. Never scoped to a client.
-- ----------------------------------------------------------------------------
create table if not exists public.suppression (
  id                uuid primary key default gen_random_uuid(),
  phone             text not null unique,                -- E.164
  reason            text not null,                       -- opt_out | dnc | complaint | invalid | manual
  source_contact_id uuid,
  created_at        timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- bookings — the product. A slot Malone captured on a call.
-- ----------------------------------------------------------------------------
create table if not exists public.bookings (
  id                    uuid primary key default gen_random_uuid(),
  contact_id            uuid references public.contacts (id) on delete cascade,
  client_id             uuid references public.clients (id) on delete cascade,
  call_id               uuid references public.calls (id) on delete set null,
  slot_text             text not null,
  confirmed             boolean not null default false,
  notified_at           timestamptz,
  estimated_value_cents integer,
  created_at            timestamptz not null default now()
);

-- Constraint top-ups, for databases created by an earlier run of this file.
do $$
begin
  if not exists (select 1 from pg_constraint where conname = 'contacts_client_campaign_phone_key') then
    alter table public.contacts
      add constraint contacts_client_campaign_phone_key unique (client_id, campaign, phone);
  end if;
end $$;

-- Enumerations live here as CHECKs, not as Postgres enums: adding a value to an
-- enum is a migration, editing a CHECK is one line. Drop-then-add keeps it
-- re-runnable and re-validates existing rows.
alter table public.clients  drop constraint if exists clients_vertical_chk;
alter table public.clients  add  constraint clients_vertical_chk
  check (vertical in ('salon', 'medspa'));

alter table public.clients  drop constraint if exists clients_stripe_status_chk;
alter table public.clients  add  constraint clients_stripe_status_chk
  check (stripe_status in ('trialing', 'active', 'past_due', 'canceled'));

alter table public.clients  drop constraint if exists clients_avg_ticket_chk;
alter table public.clients  add  constraint clients_avg_ticket_chk
  check (avg_ticket_cents >= 0);

alter table public.contacts drop constraint if exists contacts_status_chk;
alter table public.contacts add  constraint contacts_status_chk
  check (status in ('pending', 'calling', 'called', 'booked', 'declined',
                    'opted_out', 'suppressed', 'invalid', 'no_answer', 'failed'));

alter table public.contacts drop constraint if exists contacts_attempts_chk;
alter table public.contacts add  constraint contacts_attempts_chk
  check (attempts >= 0);

alter table public.calls    drop constraint if exists calls_outcome_chk;
alter table public.calls    add  constraint calls_outcome_chk
  check (outcome in ('dialing', 'answered', 'booked', 'declined', 'no_answer',
                     'voicemail', 'busy', 'failed', 'opted_out'));

alter table public.suppression drop constraint if exists suppression_reason_chk;
alter table public.suppression add  constraint suppression_reason_chk
  check (reason in ('opt_out', 'dnc', 'complaint', 'invalid', 'manual'));

-- ----------------------------------------------------------------------------
-- Indexes — one per query the app actually runs.
-- ----------------------------------------------------------------------------
create index if not exists contacts_client_status_idx  on public.contacts (client_id, status);
create index if not exists contacts_status_created_idx  on public.contacts (status, created_at);
create index if not exists contacts_phone_idx           on public.contacts (phone);
create index if not exists calls_client_created_idx     on public.calls (client_id, created_at desc);
create index if not exists calls_vapi_call_id_idx       on public.calls (vapi_call_id);
create index if not exists bookings_client_created_idx  on public.bookings (client_id, created_at desc);
create index if not exists suppression_phone_idx        on public.suppression (phone);

-- ----------------------------------------------------------------------------
-- ROW LEVEL SECURITY
--
-- RLS is enabled on all five tables with ZERO policies. That is deliberate and
-- complete: the service role bypasses RLS entirely, and with no policies the
-- anon and authenticated keys can see NOTHING. There is no browser-side data
-- access in this app, so there is nothing to write a policy for. Do not add one.
-- ----------------------------------------------------------------------------
alter table public.clients     enable row level security;
alter table public.contacts    enable row level security;
alter table public.calls       enable row level security;
alter table public.suppression enable row level security;
alter table public.bookings    enable row level security;

-- ----------------------------------------------------------------------------
-- updated_at trigger on calls (the webhook updates the same row repeatedly)
-- ----------------------------------------------------------------------------
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at := now();
  return new;
end $$;

drop trigger if exists set_updated_at on public.calls;
create trigger set_updated_at
  before update on public.calls
  for each row execute function public.set_updated_at();

-- ----------------------------------------------------------------------------
-- client_local_time — wall-clock time in a client's timezone, or NULL if the
-- timezone string is garbage. NULL fails every `between` test, so a bad
-- timezone silently stops dialing for that client instead of raising and
-- killing the whole claim batch. Fail closed.
-- ----------------------------------------------------------------------------
create or replace function public.client_local_time(p_timezone text)
returns time
language plpgsql
stable
set search_path = public
as $$
begin
  return (now() at time zone p_timezone)::time;
exception
  when others then
    return null;
end $$;

-- ----------------------------------------------------------------------------
-- THE ONE CLEVER QUERY — claim contacts for dialing.
--
-- Two crons may run concurrently. The inner select takes row locks with
-- `skip locked`, so a contact claimed by one worker is invisible to the other:
-- no double dials, no advisory locks, no queue table. Only `contacts` is locked
-- (the client filter is an EXISTS, not a join — `for update` on the join would
-- lock clients rows too, and Postgres would need `of`).
--
-- Every compliance gate is in this WHERE clause. The dial route re-checks all of
-- them in application code as well; two independent gates, on purpose.
-- ----------------------------------------------------------------------------
create or replace function public.claim_contacts_for_dialing(
  p_limit        int,
  p_window_start time,
  p_window_end   time
)
returns setof public.contacts
language plpgsql
security definer
set search_path = public
as $$
begin
  return query
  with candidates as (
    select c2.id
      from public.contacts c2
     where c2.status = 'pending'
       and c2.consent = true                 -- HARD GATE: consent
       and c2.attempts = 0                   -- HARD GATE: one attempt per contact, ever
       and c2.phone is not null
       and exists (
             select 1
               from public.clients cl
              where cl.id = c2.client_id
                and cl.active = true
                and cl.stripe_status in ('active', 'trialing')
                and public.client_local_time(cl.timezone)
                      between p_window_start and p_window_end   -- HARD GATE: call window
           )
       and not exists (
             select 1 from public.suppression s where s.phone = c2.phone
           )                                                    -- HARD GATE: suppression
     order by c2.created_at
     limit greatest(coalesce(p_limit, 0), 0)
     for update skip locked
  )
  update public.contacts c
     set status     = 'calling',
         claimed_at = now(),
         attempts   = c.attempts + 1
    from candidates cand
   where c.id = cand.id
  returning c.*;
end $$;

-- ----------------------------------------------------------------------------
-- expire_stuck_calling — a contact left in 'calling' means we dialed and never
-- got a webhook. One attempt per contact means it goes to 'failed', NEVER back
-- to 'pending'. Returns the number of rows swept.
-- ----------------------------------------------------------------------------
create or replace function public.expire_stuck_calling(p_older_than_minutes int)
returns int
language plpgsql
security definer
set search_path = public
as $$
declare
  v_rows int;
begin
  update public.contacts
     set status       = 'failed',
         scrub_reason = coalesce(scrub_reason, 'stuck_in_calling')
   where status = 'calling'
     and (claimed_at is null
          or claimed_at < now() - make_interval(mins => greatest(coalesce(p_older_than_minutes, 15), 1)));

  get diagnostics v_rows = row_count;
  return v_rows;
end $$;

-- ----------------------------------------------------------------------------
-- Function grants. These are SECURITY DEFINER, so they bypass RLS — the anon
-- key must never be able to call them. Postgres grants EXECUTE to PUBLIC by
-- default; revoke it and hand execution to the service role only.
-- ----------------------------------------------------------------------------
revoke all on function public.claim_contacts_for_dialing(int, time, time) from public;
revoke all on function public.expire_stuck_calling(int) from public;
grant execute on function public.claim_contacts_for_dialing(int, time, time) to service_role;
grant execute on function public.expire_stuck_calling(int) to service_role;

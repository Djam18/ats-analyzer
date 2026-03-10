-- ============================================================
-- ATS Score Analyzer — Initial Schema
-- ============================================================

-- ── profiles ──────────────────────────────────────────────
create table public.profiles (
  id                     uuid primary key references auth.users(id) on delete cascade,
  full_name              text,
  avatar_url             text,
  plan                   text not null default 'free' check (plan in ('free', 'pro', 'expert')),
  stripe_customer_id     text unique,
  stripe_subscription_id text,
  subscription_status    text check (subscription_status in ('active', 'past_due', 'canceled')),
  free_analyses_used     integer not null default 0,
  onboarding_completed   boolean not null default false,
  created_at             timestamptz not null default now(),
  updated_at             timestamptz not null default now()
);

alter table public.profiles enable row level security;

create policy "Users can view their own profile"
  on public.profiles for select
  using (auth.uid() = id);

create policy "Users can update their own profile"
  on public.profiles for update
  using (auth.uid() = id);

-- ── cvs ───────────────────────────────────────────────────
create table public.cvs (
  id             uuid primary key default gen_random_uuid(),
  user_id        uuid not null references public.profiles(id) on delete cascade,
  file_name      text not null,
  display_name   text not null,
  file_path      text not null,
  file_size      integer not null,
  file_type      text not null check (file_type in ('pdf', 'docx')),
  extracted_text text,
  is_scanned     boolean not null default false,
  page_count     integer,
  created_at     timestamptz not null default now()
);

alter table public.cvs enable row level security;

create policy "Users can manage their own CVs"
  on public.cvs for all
  using (auth.uid() = user_id);

-- ── analyses ──────────────────────────────────────────────
create table public.analyses (
  id               uuid primary key default gen_random_uuid(),
  user_id          uuid not null references public.profiles(id) on delete cascade,
  cv_id            uuid not null references public.cvs(id) on delete cascade,
  job_title        text not null,
  company_name     text,
  job_description  text not null,
  status           text not null default 'pending' check (status in ('pending', 'processing', 'completed', 'failed')),
  score            integer check (score >= 0 and score <= 100),
  matched_keywords jsonb,
  missing_keywords jsonb,
  analysis_details jsonb,
  error_message    text,
  created_at       timestamptz not null default now(),
  completed_at     timestamptz
);

alter table public.analyses enable row level security;

create policy "Users can manage their own analyses"
  on public.analyses for all
  using (auth.uid() = user_id);

-- ── webhook_events ────────────────────────────────────────
create table public.webhook_events (
  id               uuid primary key default gen_random_uuid(),
  stripe_event_id  text not null unique,
  event_type       text not null,
  processed_at     timestamptz not null default now()
);

-- No RLS — accessed via service_role key only

-- ── Functions & Triggers ──────────────────────────────────

-- Auto-create profile on user signup
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, full_name, avatar_url)
  values (
    new.id,
    new.raw_user_meta_data->>'full_name',
    new.raw_user_meta_data->>'avatar_url'
  );
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Atomic increment of free analyses counter
create or replace function public.increment_free_analyses(p_user_id uuid)
returns integer
language plpgsql
security definer set search_path = public
as $$
declare
  v_new_count integer;
begin
  update public.profiles
  set free_analyses_used = free_analyses_used + 1,
      updated_at = now()
  where id = p_user_id
  returning free_analyses_used into v_new_count;

  return v_new_count;
end;
$$;

-- Auto-update updated_at on profiles
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_updated_at
  before update on public.profiles
  for each row execute procedure public.set_updated_at();

-- ── Storage ───────────────────────────────────────────────

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'cvs',
  'cvs',
  false,
  5242880, -- 5 MB
  array['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
);

create policy "Users can upload their own CVs"
  on storage.objects for insert
  with check (
    bucket_id = 'cvs'
    and auth.uid()::text = (storage.foldername(name))[1]
  );

create policy "Users can read their own CVs"
  on storage.objects for select
  using (
    bucket_id = 'cvs'
    and auth.uid()::text = (storage.foldername(name))[1]
  );

create policy "Users can delete their own CVs"
  on storage.objects for delete
  using (
    bucket_id = 'cvs'
    and auth.uid()::text = (storage.foldername(name))[1]
  );

-- Performance indexes for common query patterns
create index if not exists idx_cvs_user_id on public.cvs(user_id);
create index if not exists idx_analyses_user_id on public.analyses(user_id);
create index if not exists idx_analyses_user_status_created on public.analyses(user_id, status, created_at desc);

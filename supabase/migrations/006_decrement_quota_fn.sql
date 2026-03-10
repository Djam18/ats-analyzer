-- Atomic decrement for quota refund on failed analysis
create or replace function decrement_free_analyses(p_user_id uuid)
returns void
language plpgsql
security definer
as $$
begin
  update public.profiles
  set free_analyses_used = greatest(0, free_analyses_used - 1)
  where id = p_user_id;
end;
$$;

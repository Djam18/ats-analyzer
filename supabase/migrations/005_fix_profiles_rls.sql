-- Fix: restrict profiles self-update to safe columns only
-- Users must not be able to change plan, quota, or billing fields directly

drop policy if exists "Users can update their own profile" on public.profiles;

create policy "Users can update their own profile"
  on public.profiles for update
  using (auth.uid() = id)
  with check (
    -- Sensitive billing/quota columns must remain unchanged
    plan = (select plan from public.profiles where id = auth.uid())
    and free_analyses_used = (select free_analyses_used from public.profiles where id = auth.uid())
    and subscription_status is not distinct from (select subscription_status from public.profiles where id = auth.uid())
    and stripe_customer_id is not distinct from (select stripe_customer_id from public.profiles where id = auth.uid())
    and stripe_subscription_id is not distinct from (select stripe_subscription_id from public.profiles where id = auth.uid())
  );

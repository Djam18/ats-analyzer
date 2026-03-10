const onboardingCompleted = useState<boolean | null>('onboarding_completed', () => null)

export default defineNuxtRouteMiddleware(async (to) => {
  const user = useSupabaseUser()
  if (!user.value) return

  if (to.path === '/onboarding') return

  // Use cached value to avoid a DB query on every navigation
  if (onboardingCompleted.value === null) {
    const supabase = useSupabaseClient()
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const { data: profile } = await (supabase as any)
      .from('profiles')
      .select('onboarding_completed')
      .eq('id', user.value.id)
      .single()

    onboardingCompleted.value = profile?.onboarding_completed ?? false
  }

  if (!onboardingCompleted.value) {
    return navigateTo('/onboarding')
  }
})

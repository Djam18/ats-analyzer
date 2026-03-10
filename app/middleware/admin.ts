export default defineNuxtRouteMiddleware(async () => {
  const user = useSupabaseUser()

  if (!user.value) {
    return navigateTo('/login')
  }

  // Check admin status server-side to avoid leaking adminEmail in public config
  try {
    await $fetch('/api/admin/check')
  }
  catch {
    return navigateTo('/dashboard')
  }
})

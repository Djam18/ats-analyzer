// ============================================================
// auth.global.ts — Route guard
//
// Rules:
//   - /app/* routes require authentication → redirect to /login
//   - /login and /register redirect to /app/dashboard if already authenticated
//   - /auth/confirm and /auth/reset-password are always accessible
// ============================================================

export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated, loading } = useAuth()

  // Still initializing — let through (app.vue handles the wait)
  if (loading.value) return

  const isAppRoute = to.path.startsWith('/app')
  const isAuthPage = ['/login', '/register'].includes(to.path)
  const isPublicAuthPage =
    to.path.startsWith('/auth/confirm') || to.path.startsWith('/auth/reset-password')

  // Public auth pages (confirm, reset) are always accessible
  if (isPublicAuthPage) return

  // Protect /app/* — must be authenticated
  if (isAppRoute && !isAuthenticated.value) {
    return navigateTo('/login')
  }

  // Redirect logged-in users away from /login and /register
  if (isAuthPage && isAuthenticated.value) {
    return navigateTo('/app/dashboard')
  }
})

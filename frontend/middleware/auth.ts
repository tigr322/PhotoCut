export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()
  auth.init()

  if (!auth.isAuthenticated) {
    return navigateTo('/login')
  }
})

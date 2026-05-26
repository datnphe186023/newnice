export default defineNuxtRouteMiddleware(() => {
  const authStore = useAuthStore()
  authStore.initAuth()

  if (!authStore.isAuthenticated) {
    return navigateTo('/admin/login')
  }
})
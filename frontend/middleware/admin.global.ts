export default defineNuxtRouteMiddleware((to) => {
  if (!to.path.startsWith('/admin')) {
    return
  }

  const authStore = useAuthStore()
  authStore.initAuth()

  if (to.path === '/admin/login') {
    if (authStore.isAuthenticated) {
      return navigateTo('/admin')
    }
    return
  }

  if (!authStore.isAuthenticated) {
    return navigateTo('/admin/login')
  }
})
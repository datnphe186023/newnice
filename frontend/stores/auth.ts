import { computed } from 'vue'
import { defineStore } from 'pinia'

interface User {
  id: number
  email: string
  full_name: string
  is_active: boolean
}

export const useAuthStore = defineStore('auth', () => {
  const cookieOptions = {
    sameSite: 'strict' as const,
    secure: process.env.NODE_ENV === 'production',
    path: '/',
  }

  const token = useCookie<string | null>('auth_token', cookieOptions)
  const user = useCookie<User | null>('auth_user', cookieOptions)

  const isAuthenticated = computed(() => Boolean(token.value && user.value))

  function setAuth(nextToken: string, nextUser: User) {
    token.value = nextToken
    user.value = nextUser
  }

  function logout() {
    token.value = null
    user.value = null
  }

  function initAuth() {
    // Cookies are hydrated on both server and client, so this stays intentionally lightweight.
    token.value = token.value ?? null
    user.value = user.value ?? null
  }

  return {
    user,
    token,
    isAuthenticated,
    setAuth,
    logout,
    initAuth,
    getToken: token,
    getUser: user,
  }
})

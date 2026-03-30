<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md">
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <!-- Logo -->
        <div class="text-center mb-8">
          <h1 class="text-2xl font-bold text-gray-900">AutoFilm Admin</h1>
          <p class="text-gray-500 mt-2">Đăng nhập để quản lý website</p>
        </div>

        <!-- Error message -->
        <div 
          v-if="error"
          class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm"
        >
          {{ error }}
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input 
              v-model="email"
              type="email"
              required
              placeholder="admin@autofilm.vn"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Mật khẩu
            </label>
            <input 
              v-model="password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <button 
            type="submit"
            :disabled="loading"
            class="w-full py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="loading">Đang đăng nhập...</span>
            <span v-else>Đăng nhập</span>
          </button>
        </form>

        <!-- Back to home -->
        <div class="mt-8 text-center">
          <NuxtLink to="/" class="text-sm text-gray-500 hover:text-primary-600">
            ← Về trang chủ
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

// No layout for login page
definePageMeta({
  layout: false,
})

useSeoMeta({
  title: 'Đăng nhập Admin | AutoFilm',
  robots: 'noindex, nofollow',
})

const router = useRouter()
const config = useRuntimeConfig()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

// Check if already logged in
onMounted(() => {
  authStore.initAuth()
  if (authStore.isAuthenticated) {
    router.push('/admin')
  }
})

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    // Create form data
    const formData = new FormData()
    formData.append('username', email.value)
    formData.append('password', password.value)

    const response = await $fetch<{ access_token: string; token_type: string }>(
      `${config.public.apiBase}/auth/login`,
      {
        method: 'POST',
        body: formData,
      }
    )

    // Get user info
    const user = await $fetch<any>(`${config.public.apiBase}/auth/me`, {
      headers: {
        Authorization: `Bearer ${response.access_token}`,
      },
    })

    // Store auth
    authStore.setAuth(response.access_token, user)

    // Redirect to admin
    router.push('/admin')
  } catch (err: any) {
    error.value = err.data?.detail || 'Email hoặc mật khẩu không đúng'
  } finally {
    loading.value = false
  }
}
</script>

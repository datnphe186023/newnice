<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Cài đặt website</h1>
      <button
        @click="save"
        :disabled="saving"
        class="flex items-center gap-2 px-5 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-60 disabled:cursor-not-allowed transition-colors"
      >
        <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
        </svg>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        {{ saving ? 'Đang lưu...' : 'Lưu thay đổi' }}
      </button>
    </div>

    <!-- Success / Error toast -->
    <Transition name="slide-down">
      <div v-if="toast" class="mb-6 flex items-center gap-3 px-4 py-3 rounded-xl border text-sm"
        :class="toast.type === 'success'
          ? 'bg-green-50 border-green-200 text-green-800'
          : 'bg-red-50 border-red-200 text-red-800'"
      >
        <svg v-if="toast.type === 'success'" class="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        <svg v-else class="w-5 h-5 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        {{ toast.message }}
      </div>
    </Transition>

    <div v-if="loading" class="space-y-6">
      <div v-for="i in 4" :key="i" class="bg-white rounded-xl shadow-sm p-6 animate-pulse">
        <div class="h-5 bg-gray-200 rounded w-1/4 mb-4"/>
        <div class="space-y-3">
          <div class="h-10 bg-gray-200 rounded"/>
          <div class="h-10 bg-gray-200 rounded"/>
        </div>
      </div>
    </div>

    <div v-else class="space-y-6">
      <!-- General info -->
      <section class="bg-white rounded-xl shadow-sm p-6">
        <h2 class="text-base font-semibold text-gray-900 mb-5 pb-3 border-b">Thông tin chung</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Tên website</label>
            <input v-model="form.site_name" type="text" class="input" placeholder="Newnice"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Slogan</label>
            <input v-model="form.site_tagline" type="text" class="input" placeholder="Phim cách nhiệt ô tô cao cấp"/>
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Mô tả ngắn (footer)</label>
            <textarea v-model="form.footer_about" rows="2" class="input resize-none" placeholder="Mô tả ngắn về doanh nghiệp..."/>
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Meta description mặc định</label>
            <textarea v-model="form.meta_description" rows="2" class="input resize-none" placeholder="Mô tả SEO mặc định cho trang chủ..."/>
            <p class="text-xs text-gray-400 mt-1">{{ (form.meta_description || '').length }}/160 ký tự</p>
          </div>
        </div>
      </section>

      <!-- Contact info -->
      <section class="bg-white rounded-xl shadow-sm p-6">
        <h2 class="text-base font-semibold text-gray-900 mb-5 pb-3 border-b">Thông tin liên hệ</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Số điện thoại chính</label>
            <input v-model="form.contact_phone" type="text" class="input" placeholder="0901 234 567"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Số điện thoại hero (CTA)</label>
            <input v-model="form.hero_phone" type="text" class="input" placeholder="0901 234 567"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
            <input v-model="form.contact_email" type="email" class="input" placeholder="info@newnice.vn"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Địa chỉ</label>
            <input v-model="form.contact_address" type="text" class="input" placeholder="311 Phúc Diễn, Nam Từ Liêm, Hà Nội"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Tiêu đề bảo hành</label>
            <input v-model="form.warranty_headline" type="text" class="input" placeholder="Bảo hành lên đến 10 năm"/>
          </div>
        </div>
      </section>

      <!-- Social links -->
      <section class="bg-white rounded-xl shadow-sm p-6">
        <h2 class="text-base font-semibold text-gray-900 mb-5 pb-3 border-b">Mạng xã hội</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Facebook URL</label>
            <input v-model="form.facebook_url" type="url" class="input" placeholder="https://facebook.com/newnice.vn"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Zalo URL</label>
            <input v-model="form.zalo_url" type="url" class="input" placeholder="https://zalo.me/newnice"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">YouTube URL</label>
            <input v-model="form.youtube_url" type="url" class="input" placeholder="https://youtube.com/@newnice"/>
          </div>
        </div>
      </section>

      <!-- Analytics -->
      <section class="bg-white rounded-xl shadow-sm p-6">
        <h2 class="text-base font-semibold text-gray-900 mb-5 pb-3 border-b">Analytics & SEO</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Google Analytics 4 ID</label>
            <input v-model="form.ga_measurement_id" type="text" class="input font-mono" placeholder="G-XXXXXXXXXX"/>
            <p class="text-xs text-gray-400 mt-1">Measurement ID từ GA4 property</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Google Search Console token</label>
            <input v-model="form.gsc_verification" type="text" class="input font-mono" placeholder="abc123..."/>
            <p class="text-xs text-gray-400 mt-1">Meta tag verification token từ GSC</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: 'admin' })

useSeoMeta({
  title: 'Cài đặt website | Newnice Admin',
  robots: 'noindex, nofollow',
})

const config = useRuntimeConfig()
const authStore = useAuthStore()

const loading = ref(true)
const saving = ref(false)
const toast = ref<{ type: 'success' | 'error'; message: string } | null>(null)

// All setting keys we manage
const KEYS = [
  'site_name', 'site_tagline', 'contact_phone', 'contact_email',
  'contact_address', 'facebook_url', 'zalo_url', 'youtube_url',
  'footer_about', 'hero_phone', 'ga_measurement_id', 'gsc_verification',
  'warranty_headline', 'meta_description',
] as const

type SettingKey = typeof KEYS[number]

const form = reactive<Record<SettingKey, string>>(
  Object.fromEntries(KEYS.map(k => [k, ''])) as Record<SettingKey, string>
)

// Load settings
onMounted(async () => {
  try {
    const data = await $fetch<Array<{ key: string; value: string | null }>>(
      `${config.public.apiBase}/admin/settings`,
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    )
    for (const row of data) {
      if (KEYS.includes(row.key as SettingKey)) {
        form[row.key as SettingKey] = row.value ?? ''
      }
    }
  } catch (err) {
    showToast('error', 'Không thể tải cài đặt. Vui lòng thử lại.')
  } finally {
    loading.value = false
  }
})

// Save settings
async function save() {
  saving.value = true
  try {
    await $fetch(`${config.public.apiBase}/admin/settings`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${authStore.token}` },
      body: { settings: { ...form } },
    })
    showToast('success', 'Đã lưu cài đặt thành công!')
  } catch (err) {
    showToast('error', 'Lưu thất bại. Vui lòng thử lại.')
  } finally {
    saving.value = false
  }
}

function showToast(type: 'success' | 'error', message: string) {
  toast.value = { type, message }
  setTimeout(() => { toast.value = null }, 4000)
}
</script>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active { transition: all 0.3s ease; }
.slide-down-enter-from,
.slide-down-leave-to { opacity: 0; transform: translateY(-8px); }
</style>

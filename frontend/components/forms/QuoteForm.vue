<template>
  <form @submit.prevent="submit" class="space-y-5">
    <!-- Success message -->
    <Transition name="slide-down">
      <div
        v-if="success"
        class="flex items-start gap-3 bg-green-50 border border-green-200 text-green-800 rounded-xl p-4"
      >
        <CheckCircleIcon class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
        <div>
          <p class="font-medium">Gửi yêu cầu thành công!</p>
          <p class="text-sm mt-0.5">Chúng tôi sẽ liên hệ với bạn trong vòng 24 giờ.</p>
        </div>
      </div>
    </Transition>

    <!-- Error message -->
    <Transition name="slide-down">
      <div
        v-if="error"
        class="flex items-start gap-3 bg-red-50 border border-red-200 text-red-800 rounded-xl p-4"
      >
        <ExclamationCircleIcon class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
        <p class="text-sm">{{ error }}</p>
      </div>
    </Transition>

    <!-- Row: Name + Phone -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div>
        <label for="quote-name" class="label">Họ và tên <span class="text-red-500">*</span></label>
        <input
          id="quote-name"
          v-model="form.customer_name"
          type="text"
          placeholder="Nguyễn Văn A"
          class="input"
          :class="{ 'border-red-400 focus:ring-red-400': errors.customer_name }"
          required
        />
        <p v-if="errors.customer_name" class="text-xs text-red-500 mt-1">{{ errors.customer_name }}</p>
      </div>
      <div>
        <label for="quote-phone" class="label">Số điện thoại <span class="text-red-500">*</span></label>
        <input
          id="quote-phone"
          v-model="form.phone"
          type="tel"
          placeholder="0901 234 567"
          class="input"
          :class="{ 'border-red-400 focus:ring-red-400': errors.phone }"
          required
        />
        <p v-if="errors.phone" class="text-xs text-red-500 mt-1">{{ errors.phone }}</p>
      </div>
    </div>

    <!-- Email -->
    <div>
      <label for="quote-email" class="label">Email</label>
      <input
        id="quote-email"
        v-model="form.email"
        type="email"
        placeholder="example@email.com"
        class="input"
      />
    </div>

    <!-- Car info row -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div>
        <label for="quote-car-brand" class="label">Hãng xe</label>
        <input
          id="quote-car-brand"
          v-model="form.car_brand"
          type="text"
          placeholder="Toyota, Honda..."
          class="input"
        />
      </div>
      <div>
        <label for="quote-car-model" class="label">Dòng xe</label>
        <input
          id="quote-car-model"
          v-model="form.car_model"
          type="text"
          placeholder="Camry, Civic..."
          class="input"
        />
      </div>
      <div>
        <label for="quote-car-year" class="label">Năm sản xuất</label>
        <input
          id="quote-car-year"
          v-model.number="form.car_year"
          type="number"
          placeholder="2022"
          min="1990"
          :max="new Date().getFullYear()"
          class="input"
        />
      </div>
    </div>

    <!-- Service type -->
    <div>
      <label class="label">Loại dịch vụ</label>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
        <label
          v-for="svc in serviceTypes"
          :key="svc.value"
          class="flex items-center gap-2 cursor-pointer p-3 rounded-lg border-2 transition-colors"
          :class="form.service_type === svc.value
            ? 'border-primary-600 bg-primary-50 text-primary-700'
            : 'border-gray-200 hover:border-gray-300'"
        >
          <input
            type="radio"
            :value="svc.value"
            v-model="form.service_type"
            class="sr-only"
          />
          <component :is="svc.icon" class="w-4 h-4 flex-shrink-0" />
          <span class="text-sm font-medium">{{ svc.label }}</span>
        </label>
      </div>
    </div>

    <!-- Film type preference -->
    <div>
      <label for="quote-film-type" class="label">Loại phim yêu thích</label>
      <select id="quote-film-type" v-model="form.film_type_preference" class="input">
        <option value="">-- Chưa biết --</option>
        <option value="ceramic">Phim Ceramic</option>
        <option value="carbon">Phim Carbon</option>
        <option value="metallic">Phim Metallic</option>
        <option value="nano">Phim Nano</option>
        <option value="hybrid">Phim Hybrid</option>
      </select>
    </div>

    <!-- Message -->
    <div>
      <label for="quote-message" class="label">Ghi chú thêm</label>
      <textarea
        id="quote-message"
        v-model="form.message"
        rows="3"
        placeholder="Yêu cầu đặc biệt, thắc mắc..."
        class="input resize-none"
      />
    </div>

    <!-- Submit -->
    <button
      type="submit"
      :disabled="loading"
      class="btn-primary w-full text-base gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
    >
      <ArrowPathIcon v-if="loading" class="w-5 h-5 animate-spin" />
      <PaperAirplaneIcon v-else class="w-5 h-5" />
      {{ loading ? 'Đang gửi...' : 'Gửi yêu cầu báo giá' }}
    </button>

    <p class="text-xs text-gray-400 text-center">
      Thông tin của bạn sẽ được bảo mật tuyệt đối
    </p>
  </form>
</template>

<script setup lang="ts">
import {
  SunIcon,
  ShieldCheckIcon,
  PaintBrushIcon,
  HomeIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  PaperAirplaneIcon,
  ArrowPathIcon,
} from '@heroicons/vue/24/outline'
import type { QuoteRequest } from '~/types'

const config = useRuntimeConfig()

const form = reactive<QuoteRequest>({
  customer_name: '',
  phone: '',
  email: '',
  car_brand: '',
  car_model: '',
  car_year: undefined,
  service_type: '',
  film_type_preference: '',
  message: '',
})

const errors = reactive<Partial<Record<keyof QuoteRequest, string>>>({})
const loading = ref(false)
const success = ref(false)
const error = ref('')

const serviceTypes = [
  { value: 'phim-cach-nhiet', label: 'Cách nhiệt', icon: SunIcon },
  { value: 'phim-ppf', label: 'PPF', icon: ShieldCheckIcon },
  { value: 'phim-doi-mau', label: 'Đổi màu', icon: PaintBrushIcon },
  { value: 'phim-nha-kinh', label: 'Nhà kính', icon: HomeIcon },
]

const validate = (): boolean => {
  errors.customer_name = ''
  errors.phone = ''

  let valid = true
  if (!form.customer_name.trim()) {
    errors.customer_name = 'Vui lòng nhập họ và tên'
    valid = false
  }
  if (!form.phone.trim()) {
    errors.phone = 'Vui lòng nhập số điện thoại'
    valid = false
  } else if (!/^[0-9]{9,11}$/.test(form.phone.replace(/\s/g, ''))) {
    errors.phone = 'Số điện thoại không hợp lệ'
    valid = false
  }
  return valid
}

const submit = async () => {
  if (!validate()) return
  loading.value = true
  error.value = ''
  success.value = false

  try {
    await $fetch(`${config.public.apiBase}/quotes`, {
      method: 'POST',
      body: form,
    })
    success.value = true
    // Reset form
    Object.assign(form, {
      customer_name: '', phone: '', email: '', car_brand: '',
      car_model: '', car_year: undefined, service_type: '',
      film_type_preference: '', message: '',
    })
    // GA4: track quote request
    if (import.meta.client) {
      const { $gtag } = useNuxtApp()
      $gtag('event', 'generate_lead', { form_type: 'quote' })
    }
  } catch (err: unknown) {
    const e = err as { data?: { detail?: string } }
    error.value = e?.data?.detail || 'Có lỗi xảy ra. Vui lòng thử lại sau.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>

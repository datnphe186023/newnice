<template>
  <form @submit.prevent="submit" class="space-y-5">
    <!-- Success -->
    <Transition name="slide-down">
      <div
        v-if="success"
        class="flex items-start gap-3 bg-green-50 border border-green-200 text-green-800 rounded-xl p-4"
      >
        <CheckCircleIcon class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
        <div>
          <p class="font-medium">Tin nhắn đã được gửi!</p>
          <p class="text-sm mt-0.5">Chúng tôi sẽ phản hồi trong vòng 24 giờ làm việc.</p>
        </div>
      </div>
    </Transition>

    <!-- Error -->
    <Transition name="slide-down">
      <div
        v-if="error"
        class="flex items-start gap-3 bg-red-50 border border-red-200 text-red-800 rounded-xl p-4"
      >
        <ExclamationCircleIcon class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
        <p class="text-sm">{{ error }}</p>
      </div>
    </Transition>

    <!-- Name + Phone -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div>
        <label for="contact-name" class="label">Họ và tên <span class="text-red-500">*</span></label>
        <input
          id="contact-name"
          v-model="form.name"
          type="text"
          placeholder="Nguyễn Văn A"
          class="input"
          :class="{ 'border-red-400': errors.name }"
          required
        />
        <p v-if="errors.name" class="text-xs text-red-500 mt-1">{{ errors.name }}</p>
      </div>
      <div>
        <label for="contact-phone" class="label">Số điện thoại</label>
        <input
          id="contact-phone"
          v-model="form.phone"
          type="tel"
          placeholder="0901 234 567"
          class="input"
        />
      </div>
    </div>

    <!-- Email -->
    <div>
      <label for="contact-email" class="label">Email <span class="text-red-500">*</span></label>
      <input
        id="contact-email"
        v-model="form.email"
        type="email"
        placeholder="example@email.com"
        class="input"
        :class="{ 'border-red-400': errors.email }"
        required
      />
      <p v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</p>
    </div>

    <!-- Subject -->
    <div>
      <label for="contact-subject" class="label">Chủ đề</label>
      <select id="contact-subject" v-model="form.subject" class="input">
        <option value="">-- Chọn chủ đề --</option>
        <option value="Tư vấn sản phẩm">Tư vấn sản phẩm</option>
        <option value="Báo giá dịch vụ">Báo giá dịch vụ</option>
        <option value="Hỗ trợ kỹ thuật">Hỗ trợ kỹ thuật</option>
        <option value="Khiếu nại / Bảo hành">Khiếu nại / Bảo hành</option>
        <option value="Khác">Khác</option>
      </select>
    </div>

    <!-- Message -->
    <div>
      <label for="contact-message" class="label">Nội dung <span class="text-red-500">*</span></label>
      <textarea
        id="contact-message"
        v-model="form.message"
        rows="5"
        placeholder="Nội dung tin nhắn của bạn..."
        class="input resize-none"
        :class="{ 'border-red-400': errors.message }"
        required
      />
      <p v-if="errors.message" class="text-xs text-red-500 mt-1">{{ errors.message }}</p>
    </div>

    <!-- Submit -->
    <button
      type="submit"
      :disabled="loading"
      class="btn-primary w-full text-base gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
    >
      <ArrowPathIcon v-if="loading" class="w-5 h-5 animate-spin" />
      <PaperAirplaneIcon v-else class="w-5 h-5" />
      {{ loading ? 'Đang gửi...' : 'Gửi tin nhắn' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  PaperAirplaneIcon,
  ArrowPathIcon,
} from '@heroicons/vue/24/outline'
import type { Contact } from '~/types'

const config = useRuntimeConfig()

const form = reactive<Contact>({
  name: '',
  phone: '',
  email: '',
  subject: '',
  message: '',
})

const errors = reactive<Partial<Record<keyof Contact, string>>>({})
const loading = ref(false)
const success = ref(false)
const error = ref('')

const validate = (): boolean => {
  errors.name = ''
  errors.email = ''
  errors.message = ''

  let valid = true
  if (!form.name.trim()) {
    errors.name = 'Vui lòng nhập họ và tên'
    valid = false
  }
  if (!form.email.trim()) {
    errors.email = 'Vui lòng nhập email'
    valid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Email không hợp lệ'
    valid = false
  }
  if (!form.message.trim()) {
    errors.message = 'Vui lòng nhập nội dung tin nhắn'
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
    await $fetch(`${config.public.apiBase}/contact`, {
      method: 'POST',
      body: form,
    })
    success.value = true
    Object.assign(form, { name: '', phone: '', email: '', subject: '', message: '' })
    // GA4: track contact form submission
    if (import.meta.client) {
      const { $gtag } = useNuxtApp()
      if (typeof $gtag === 'function') {
        $gtag('event', 'contact', { form_type: 'contact' })
      }
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

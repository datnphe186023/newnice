<template>
  <div>
    <!-- Banner -->
    <div class="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-16">
      <div class="container text-center">
        <h1 class="text-3xl md:text-4xl font-bold mb-4">Liên Hệ Với Chúng Tôi</h1>
        <p class="text-xl text-white/80">
          Chúng tôi luôn sẵn sàng hỗ trợ bạn
        </p>
      </div>
    </div>

    <div class="container py-12">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Contact info -->
        <div>
          <h2 class="text-2xl font-bold mb-6">Thông Tin Liên Hệ</h2>
          
          <div class="space-y-6">
            <div class="flex items-start gap-4">
              <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <MapPinIcon class="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h3 class="font-semibold mb-1">Địa chỉ</h3>
                <p class="text-gray-600">123 Nguyễn Văn Linh, Quận 7, TP. Hồ Chí Minh</p>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <PhoneIcon class="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h3 class="font-semibold mb-1">Điện thoại</h3>
                <a href="tel:0901234567" class="text-primary-600 hover:text-primary-700 font-medium">
                  0901 234 567
                </a>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <EnvelopeIcon class="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h3 class="font-semibold mb-1">Email</h3>
                <a href="mailto:info@autofilm.vn" class="text-primary-600 hover:text-primary-700">
                  info@autofilm.vn
                </a>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <ClockIcon class="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h3 class="font-semibold mb-1">Giờ làm việc</h3>
                <p class="text-gray-600">Thứ 2 - Chủ nhật: 8:00 - 18:00</p>
              </div>
            </div>
          </div>

          <!-- Map -->
          <div class="mt-8 rounded-lg overflow-hidden h-64 bg-gray-200">
            <iframe 
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3920.0245!2d106.7!3d10.73!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMTDCsDQzJzQ4LjAiTiAxMDbCsDQyJzAwLjAiRQ!5e0!3m2!1sen!2s!4v1234567890"
              width="100%" 
              height="100%" 
              style="border:0;" 
              allowfullscreen="" 
              loading="lazy"
            />
          </div>
        </div>

        <!-- Contact form -->
        <div>
          <h2 class="text-2xl font-bold mb-6">Gửi Tin Nhắn</h2>
          
          <div class="card p-6">
            <form @submit.prevent="handleSubmit">
              <div class="mb-4">
                <label class="label">Họ và tên *</label>
                <input v-model="form.name" type="text" class="input" required />
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label class="label">Email *</label>
                  <input v-model="form.email" type="email" class="input" required />
                </div>
                <div>
                  <label class="label">Số điện thoại</label>
                  <input v-model="form.phone" type="tel" class="input" />
                </div>
              </div>

              <div class="mb-4">
                <label class="label">Tiêu đề</label>
                <input v-model="form.subject" type="text" class="input" />
              </div>

              <div class="mb-6">
                <label class="label">Nội dung *</label>
                <textarea v-model="form.message" class="input" rows="5" required />
              </div>

              <div v-if="error" class="mb-4 p-4 bg-red-50 text-red-600 rounded-lg">
                {{ error }}
              </div>

              <div v-if="successMessage" class="mb-4 p-4 bg-green-50 text-green-600 rounded-lg">
                {{ successMessage }}
              </div>

              <button type="submit" class="btn-primary w-full" :disabled="isSubmitting">
                {{ isSubmitting ? 'Đang gửi...' : 'Gửi tin nhắn' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MapPinIcon, PhoneIcon, EnvelopeIcon, ClockIcon } from '@heroicons/vue/24/outline'
import type { Contact } from '~/types'

useSeoMeta({
  title: 'Liên hệ | AutoFilm',
  description: 'Liên hệ AutoFilm để được tư vấn về phim cách nhiệt ô tô, phim PPF, phim đổi màu xe.',
})

const { isSubmitting, error, submitContact } = useQuote()
const successMessage = ref('')

const form = reactive<Contact>({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const handleSubmit = async () => {
  const result = await submitContact(form)
  if (result) {
    successMessage.value = result.message
    Object.assign(form, { name: '', email: '', phone: '', subject: '', message: '' })
  }
}
</script>

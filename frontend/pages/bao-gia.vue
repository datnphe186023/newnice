<template>
  <div>
    <!-- Banner -->
    <div class="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-16">
      <div class="container text-center">
        <h1 class="text-3xl md:text-4xl font-bold mb-4">Yêu Cầu Báo Giá</h1>
        <p class="text-xl text-white/80 max-w-2xl mx-auto">
          Điền thông tin bên dưới để nhận báo giá nhanh nhất từ đội ngũ tư vấn của chúng tôi
        </p>
      </div>
    </div>

    <div class="container py-12">
      <div class="max-w-2xl mx-auto">
        <div class="card p-8">
          <form @submit.prevent="handleSubmit">
            <!-- Name -->
            <div class="mb-6">
              <label class="label">Họ và tên *</label>
              <input 
                v-model="form.customer_name"
                type="text" 
                class="input"
                placeholder="Nguyễn Văn A"
                required
              />
            </div>

            <!-- Phone -->
            <div class="mb-6">
              <label class="label">Số điện thoại *</label>
              <input 
                v-model="form.phone"
                type="tel" 
                class="input"
                placeholder="0901 234 567"
                required
              />
            </div>

            <!-- Email -->
            <div class="mb-6">
              <label class="label">Email</label>
              <input 
                v-model="form.email"
                type="email" 
                class="input"
                placeholder="email@example.com"
              />
            </div>

            <!-- Car info -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label class="label">Hãng xe</label>
                <select v-model="form.car_brand" class="input">
                  <option value="">Chọn hãng xe</option>
                  <option v-for="brand in carBrands" :key="brand" :value="brand">
                    {{ brand }}
                  </option>
                </select>
              </div>
              <div>
                <label class="label">Dòng xe</label>
                <input 
                  v-model="form.car_model"
                  type="text" 
                  class="input"
                  placeholder="VD: Camry, C-Class..."
                />
              </div>
            </div>

            <!-- Service type -->
            <div class="mb-6">
              <label class="label">Dịch vụ quan tâm</label>
              <select v-model="form.service_type" class="input">
                <option value="">Chọn dịch vụ</option>
                <option value="Phim cách nhiệt ô tô">Phim cách nhiệt ô tô</option>
                <option value="Phim đổi màu xe">Phim đổi màu xe</option>
                <option value="Phim nhà kính">Phim nhà kính</option>
                <option value="Khác">Khác</option>
              </select>
            </div>

            <!-- Film preference -->
            <div class="mb-6">
              <label class="label">Thương hiệu phim quan tâm</label>
              <select v-model="form.film_type_preference" class="input">
                <option value="">Chọn thương hiệu</option>
                <option value="3M">3M</option>
                <option value="LLumar">LLumar</option>
                <option value="V-KOOL">V-KOOL</option>
                <option value="SunTek">SunTek</option>
                <option value="Ntech">Ntech</option>
                <option value="Chưa biết - Cần tư vấn">Chưa biết - Cần tư vấn</option>
              </select>
            </div>

            <!-- Message -->
            <div class="mb-6">
              <label class="label">Ghi chú thêm</label>
              <textarea 
                v-model="form.message"
                class="input"
                rows="4"
                placeholder="Yêu cầu đặc biệt hoặc câu hỏi..."
              />
            </div>

            <!-- Error -->
            <div v-if="error" class="mb-6 p-4 bg-red-50 text-red-600 rounded-lg">
              {{ error }}
            </div>

            <!-- Success -->
            <div v-if="isSuccess" class="mb-6 p-4 bg-green-50 text-green-600 rounded-lg">
              Cảm ơn bạn! Chúng tôi sẽ liên hệ với bạn trong thời gian sớm nhất.
            </div>

            <!-- Submit -->
            <button 
              type="submit" 
              class="btn-primary w-full text-lg"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting">Đang gửi...</span>
              <span v-else>Gửi yêu cầu báo giá</span>
            </button>
          </form>
        </div>

        <!-- Contact info -->
        <div class="mt-8 text-center">
          <p class="text-gray-600 mb-4">Hoặc liên hệ trực tiếp với chúng tôi:</p>
          <a href="tel:0901234567" class="text-2xl font-bold text-primary-600 hover:text-primary-700">
            0901 234 567
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { QuoteRequest } from '~/types'

useSeoMeta({
  title: 'Yêu cầu báo giá | Newnice',
  description: 'Gửi yêu cầu báo giá phim cách nhiệt ô tô, phim đổi màu xe, phim cách nhiệt nhà kính. Phản hồi nhanh trong 30 phút.',
})

const { isSubmitting, error, submitQuote } = useQuote()
const isSuccess = ref(false)

const form = reactive<QuoteRequest>({
  customer_name: '',
  phone: '',
  email: '',
  car_brand: '',
  car_model: '',
  film_type_preference: '',
  service_type: '',
  message: ''
})

const carBrands = [
  'Toyota', 'Honda', 'Mazda', 'Hyundai', 'Kia', 
  'Mercedes-Benz', 'BMW', 'Audi', 'Lexus', 'Porsche',
  'Ford', 'Chevrolet', 'Mitsubishi', 'Nissan', 'Subaru',
  'VinFast', 'Peugeot', 'Volvo', 'Land Rover', 'Khác'
]

const handleSubmit = async () => {
  const success = await submitQuote(form)
  if (success) {
    isSuccess.value = true
    // Reset form
    Object.assign(form, {
      customer_name: '',
      phone: '',
      email: '',
      car_brand: '',
      car_model: '',
      film_type_preference: '',
      service_type: '',
      message: ''
    })
  }
}
</script>

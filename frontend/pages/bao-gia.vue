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
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
        <!-- Form -->
        <div class="lg:col-span-2">
          <div class="card p-8">
            <h2 class="text-xl font-bold mb-6">Thông tin báo giá</h2>
            <FormsQuoteForm />
          </div>
        </div>

        <!-- Side info -->
        <div class="space-y-4">
          <div class="card p-6">
            <h3 class="font-semibold mb-4 flex items-center gap-2">
              <PhoneIcon class="w-5 h-5 text-primary-600" />
              Liên hệ trực tiếp
            </h3>
            <a href="tel:0869418104" class="block text-2xl font-bold text-primary-600 hover:text-primary-700 mb-1">
              0869 418 104
            </a>
            <p class="text-sm text-gray-500">Thứ 2 - Chủ nhật: 8:00 - 18:00</p>
          </div>

          <div class="card p-6">
            <h3 class="font-semibold mb-3 flex items-center gap-2">
              <ClockIcon class="w-5 h-5 text-primary-600" />
              Tại sao chọn chúng tôi?
            </h3>
            <ul class="space-y-2 text-sm text-gray-600">
              <li class="flex items-center gap-2">
                <CheckCircleIcon class="w-4 h-4 text-green-500 flex-shrink-0" />
                Phản hồi trong vòng 30 phút
              </li>
              <li class="flex items-center gap-2">
                <CheckCircleIcon class="w-4 h-4 text-green-500 flex-shrink-0" />
                Báo giá miễn phí, không ẩn phí
              </li>
              <li class="flex items-center gap-2">
                <CheckCircleIcon class="w-4 h-4 text-green-500 flex-shrink-0" />
                Hơn 10 năm kinh nghiệm
              </li>
              <li class="flex items-center gap-2">
                <CheckCircleIcon class="w-4 h-4 text-green-500 flex-shrink-0" />
                Bảo hành lên đến 10 năm
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PhoneIcon, ClockIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'
import { useCanonical } from '~/composables/useCanonical'

useSeoMeta({
  title: 'Báo giá phim cách nhiệt ô tô — Newnice',
  description: 'Nhận báo giá phim cách nhiệt ô tô, phim PPF, phim đổi màu xe miễn phí. Phản hồi trong 30 phút. Bảo hành lên đến 10 năm.',
  ogTitle: 'Báo giá phim cách nhiệt ô tô — Newnice',
  ogDescription: 'Nhận báo giá phim cách nhiệt ô tô, phim PPF, phim đổi màu xe miễn phí. Phản hồi trong 30 phút.',
})
useCanonical('/bao-gia')
</script>

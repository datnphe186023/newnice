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
                <a href="tel:0869418104" class="text-primary-600 hover:text-primary-700 font-medium">
                  0869 418 104
                </a>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <EnvelopeIcon class="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h3 class="font-semibold mb-1">Email</h3>
                <a href="mailto:newnicefilm@gmail.com" class="text-primary-600 hover:text-primary-700">
                  newnicefilm@gmail.com
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
          <div class="mt-8 rounded-xl overflow-hidden h-64 bg-gray-200">
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
            <FormsContactForm />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MapPinIcon, PhoneIcon, EnvelopeIcon, ClockIcon } from '@heroicons/vue/24/outline'
import { buildLocalBusinessSchema, useJsonLd } from '~/composables/useJsonLd'
import { useCanonical } from '~/composables/useCanonical'

useSeoMeta({
  title: 'Liên hệ Newnice — Tư vấn phim cách nhiệt ô tô tại TP.HCM',
  description: 'Liên hệ Newnice để được tư vấn miễn phí về phim cách nhiệt ô tô, phim PPF, phim đổi màu xe. Hotline: 0869 418 104 · Email: newnicefilm@gmail.com',
  ogTitle: 'Liên hệ Newnice — Tư vấn phim cách nhiệt ô tô tại TP.HCM',
  ogDescription: 'Liên hệ Newnice để được tư vấn miễn phí về phim cách nhiệt ô tô, phim PPF, phim đổi màu xe.',
})
useJsonLd(buildLocalBusinessSchema())
useCanonical('/lien-he')
</script>

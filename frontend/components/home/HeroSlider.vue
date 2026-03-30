<template>
  <div class="relative">
    <Swiper
      :modules="[SwiperAutoplay, SwiperPagination, SwiperNavigation]"
      :slides-per-view="1"
      :loop="true"
      :autoplay="{ delay: 5000, disableOnInteraction: false }"
      :pagination="{ clickable: true }"
      :navigation="true"
      class="hero-slider"
    >
      <SwiperSlide v-for="(slide, index) in slides" :key="index">
        <div 
          class="relative h-[400px] md:h-[500px] lg:h-[600px] bg-cover bg-center"
          :style="{ backgroundImage: `url(${slide.image})` }"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-black/70 to-transparent">
            <div class="container h-full flex items-center">
              <div class="max-w-xl text-white">
                <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
                  {{ slide.title }}
                </h2>
                <p class="text-lg md:text-xl text-gray-200 mb-6">
                  {{ slide.description }}
                </p>
                <div class="flex flex-wrap gap-4">
                  <NuxtLink :to="slide.link" class="btn-accent">
                    Xem ngay
                  </NuxtLink>
                  <NuxtLink to="/bao-gia" class="btn-outline border-white text-white hover:bg-white hover:text-gray-900">
                    Báo giá
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </SwiperSlide>
    </Swiper>
  </div>
</template>

<script setup lang="ts">
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay as SwiperAutoplay, Pagination as SwiperPagination, Navigation as SwiperNavigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'

const slides = [
  {
    title: 'Phim Cách Nhiệt 3M Crystalline',
    description: 'Công nghệ nano đa lớp độc quyền, độ trong suốt vượt trội, chặn 99.9% tia UV',
    image: 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=1920&q=80',
    link: '/danh-muc/phim-cach-nhiet-o-to'
  },
  {
    title: 'Phim PPF Bảo Vệ Sơn Xe',
    description: 'Bảo vệ toàn diện khỏi trầy xước, đá văng, côn trùng với công nghệ tự phục hồi',
    image: 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1920&q=80',
    link: '/danh-muc/phim-ppf'
  },
  {
    title: 'Phim Đổi Màu Xe Cao Cấp',
    description: 'Thay đổi diện mạo xe theo phong cách riêng với hàng trăm màu sắc độc đáo',
    image: 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=1920&q=80',
    link: '/danh-muc/phim-doi-mau-xe'
  }
]
</script>

<style>
.hero-slider .swiper-pagination-bullet {
  @apply bg-white/50 w-3 h-3;
}

.hero-slider .swiper-pagination-bullet-active {
  @apply bg-white;
}

.hero-slider .swiper-button-prev,
.hero-slider .swiper-button-next {
  @apply text-white;
}
</style>

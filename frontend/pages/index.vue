<template>
  <div>
    <!-- Hero Slider -->
    <HomeHeroSlider />

    <!-- Categories -->
    <HomeCategoryGrid />

    <!-- Featured Products (inline to avoid SSR sub-component issues) -->
    <section class="py-14">
      <div class="container">
        <div class="flex items-end justify-between mb-10">
          <div>
            <p class="text-primary-600 font-semibold text-sm uppercase tracking-wider mb-2">Được yêu thích nhất</p>
            <h2 class="section-title">Sản Phẩm Nổi Bật</h2>
          </div>
          <NuxtLink
            to="/san-pham"
            class="hidden sm:flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium transition-colors"
          >
            Xem tất cả →
          </NuxtLink>
        </div>

        <!-- Loading skeleton -->
        <div v-if="featuredPending" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="i in 4" :key="i" class="card animate-pulse">
            <div class="aspect-square bg-gray-200" />
            <div class="p-4 space-y-3">
              <div class="h-3 bg-gray-200 rounded w-1/3" />
              <div class="h-5 bg-gray-200 rounded" />
              <div class="h-4 bg-gray-200 rounded w-3/4" />
            </div>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <ProductCard
            v-for="product in featuredProducts"
            :key="product.id"
            :product="product"
          />
        </div>

        <div class="text-center mt-8 sm:hidden">
          <NuxtLink to="/san-pham" class="btn-outline">Xem tất cả sản phẩm</NuxtLink>
        </div>
      </div>
    </section>

    <!-- Why Choose Us -->
    <section class="py-12 bg-dark text-white">
      <div class="container">
        <h2 class="section-title text-center text-white mb-12">Tại Sao Chọn Newnice?</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div v-for="feature in features" :key="feature.title" class="text-center">
            <div class="w-16 h-16 mx-auto mb-4 bg-accent rounded-full flex items-center justify-center">
              <component :is="feature.icon" class="w-8 h-8 text-white" />
            </div>
            <h3 class="font-semibold text-lg mb-2">{{ feature.title }}</h3>
            <p class="text-gray-400">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 bg-gradient-to-r from-primary-600 to-primary-800 text-white">
      <div class="container text-center">
        <h2 class="text-3xl md:text-4xl font-bold mb-4">Nhận Báo Giá Ngay Hôm Nay</h2>
        <p class="text-xl text-white/80 mb-8 max-w-2xl mx-auto">
          Liên hệ với chúng tôi để được tư vấn và báo giá miễn phí cho xe của bạn
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <NuxtLink to="/bao-gia" class="btn-accent text-lg px-8">
            Báo giá miễn phí
          </NuxtLink>
          <a href="tel:0901234567" class="btn bg-white text-primary-600 hover:bg-gray-100 text-lg px-8" @click="trackPhoneClick('0901234567')">
            Gọi ngay: 0901 234 567
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { 
  ShieldCheckIcon, 
  SparklesIcon, 
  TruckIcon, 
  WrenchScrewdriverIcon,
} from '@heroicons/vue/24/outline'
import type { Product } from '~/types'
import { useJsonLd, buildOrganizationSchema } from '~/composables/useJsonLd'
import { useCanonical } from '~/composables/useCanonical'
import { usePhoneTracking } from '~/composables/usePhoneTracking'

const config = useRuntimeConfig()

// SEO
useSeoMeta({
  title: 'Newnice - Phim Cách Nhiệt Ô Tô Cao Cấp',
  description: 'Newnice - Chuyên cung cấp và thi công phim cách nhiệt ô tô Newnice, 3M, phim đổi màu xe, phim cách nhiệt nhà kính cao cấp tại TP.HCM',
  ogTitle: 'Newnice - Phim Cách Nhiệt Ô Tô Cao Cấp',
  ogDescription: 'Chuyên cung cấp và thi công phim cách nhiệt ô tô, phim đổi màu xe, phim cách nhiệt nhà kính cao cấp',
})
useJsonLd(buildOrganizationSchema())
useCanonical('/')

const { trackPhoneClick } = usePhoneTracking()

// Featured products
const { data: featuredProducts, pending: featuredPending } = await useFetch<Product[]>(
  `${config.public.apiBase}/products/featured?limit=8`,
  { default: () => [] }
)

// Features
const features = [
  {
    title: 'Sản phẩm chính hãng',
    description: 'Cam kết 100% sản phẩm chính hãng từ các thương hiệu hàng đầu',
    icon: ShieldCheckIcon
  },
  {
    title: 'Kỹ thuật chuyên nghiệp',
    description: 'Đội ngũ thợ lành nghề với hơn 10 năm kinh nghiệm',
    icon: WrenchScrewdriverIcon
  },
  {
    title: 'Bảo hành dài hạn',
    description: 'Bảo hành lên đến 10 năm theo tiêu chuẩn nhà sản xuất',
    icon: SparklesIcon
  },
  {
    title: 'Dịch vụ tận nơi',
    description: 'Hỗ trợ tư vấn và thi công tại nhà theo yêu cầu',
    icon: TruckIcon
  }
]

</script>


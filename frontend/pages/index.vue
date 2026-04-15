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
    <section class="py-12 bg-white text-gray-900 border-y border-gray-100">
      <div class="container">
        <h2 class="section-title text-center text-gray-900 mb-12">Tại Sao Chọn Newnice?</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div v-for="feature in features" :key="feature.title" class="text-center">
            <div class="w-16 h-16 mx-auto mb-4 bg-accent rounded-full flex items-center justify-center">
              <component :is="feature.icon" class="w-8 h-8 text-white" />
            </div>
            <h3 class="font-semibold text-lg mb-2 text-gray-900">{{ feature.title }}</h3>
            <p class="text-gray-500">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Newnice Price Table -->
    <section class="py-16 bg-gray-50">
      <div class="container">
        <!-- Header -->
        <div class="text-center mb-10">
          <img src="/logo.png" alt="Newnice" class="h-16 w-auto mx-auto mb-4" />
          <h2 class="text-2xl md:text-3xl font-black uppercase tracking-wide text-gray-900">
            Bảng Báo Giá Film Cách Nhiệt Newnice
          </h2>
        </div>

        <!-- Price table -->
        <div class="overflow-x-auto rounded-xl border border-yellow-300 shadow-md">
          <table class="w-full text-sm text-center">
            <thead>
              <tr class="bg-yellow-50 border-b-2 border-yellow-300">
                <th class="px-4 py-3 font-bold text-gray-700 text-left w-40">Hạng mục</th>
                <th v-for="pkg in newnicePrices.packages" :key="pkg.name"
                    class="px-4 py-3 font-bold text-gray-900 border-l border-yellow-200">
                  {{ pkg.name }}
                </th>
              </tr>
            </thead>
            <tbody>
              <!-- SEDAN -->
              <tr class="border-b border-gray-200 bg-white">
                <td class="px-4 py-3 text-left font-semibold text-gray-700">SEDAN - Xe 5 chỗ</td>
                <td v-for="pkg in newnicePrices.packages" :key="pkg.name + '-sedan'"
                    class="px-4 py-3 border-l border-gray-100">
                  <div class="font-bold text-accent text-base">{{ formatVND(pkg.sedan) }}</div>
                </td>
              </tr>
              <!-- SUV -->
              <tr class="border-b border-gray-200 bg-gray-50">
                <td class="px-4 py-3 text-left font-semibold text-gray-700">SUV - Xe 7 chỗ</td>
                <td v-for="pkg in newnicePrices.packages" :key="pkg.name + '-suv'"
                    class="px-4 py-3 border-l border-gray-100">
                  <div class="font-bold text-accent text-base">{{ formatVND(pkg.suv) }}</div>
                </td>
              </tr>
              <!-- Per-window rows -->
              <tr v-for="(row, i) in newnicePrices.rows" :key="row.position"
                  :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
                  class="border-b border-gray-200">
                <td class="px-4 py-3 text-left text-gray-600 font-medium">{{ row.position }}</td>
                <td v-for="pkg in newnicePrices.packages" :key="pkg.name + row.position"
                    class="px-4 py-3 border-l border-gray-100">
                  <div class="text-xs text-gray-500">{{ row.codes[pkg.name] }}</div>
                  <div class="font-semibold text-accent">{{ formatVND(row.prices[pkg.name]) }}</div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Notes -->
        <ul class="mt-6 space-y-1 text-sm text-gray-500 list-none">
          <li>- Giá trên chưa bao gồm thuế VAT.</li>
          <li>- Đối với xe có kính nóc tính thêm giá 1 nóc bằng giá 1 sườn.</li>
          <li>- Không bảo hành trong trường hợp lỗi Film do người sử dụng gây nên.</li>
          <li>- Phục vụ lắp đặt tại cơ quan, nhà riêng cho quý khách.</li>
        </ul>

        <!-- CTA -->
        <div class="text-center mt-10 flex flex-wrap justify-center gap-4">
          <NuxtLink to="/bao-gia" class="btn-accent text-lg px-8">
            Báo giá miễn phí
          </NuxtLink>
          <a href="tel:0869418104" class="btn bg-gray-900 text-white hover:bg-gray-700 text-lg px-8" @click="trackPhoneClick('0869418104')">
            Gọi ngay: 0869 418 104
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
  description: 'Newnice - Chuyên cung cấp và thi công phim cách nhiệt ô tô Newnice, 3M, phim đổi màu xe, phim cách nhiệt nhà kính cao cấp tại Hà Nội',
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
const formatVND = (n?: number) =>
  n ? new Intl.NumberFormat('vi-VN').format(n) + ' ₫' : '—'

const newnicePrices = {
  packages: [
    { name: 'NewNice Eco',     sedan:  5_800_000, suv:  7_000_000 },
    { name: 'NewNice Premium', sedan: 10_500_000, suv: 11_500_000 },
    { name: 'NewNice Crystal', sedan: 12_500_000, suv: 14_500_000 },
    { name: 'NewNice Royal',   sedan: 15_500_000, suv: 17_500_000 },
  ],
  rows: [
    {
      position: 'Kính lái',
      codes:  { 'NewNice Eco': 'NE75',        'NewNice Premium': 'NP62/NP66',  'NewNice Crystal': 'HD/NC60-70', 'NewNice Royal': 'NR/60-70'   },
      prices: { 'NewNice Eco': 2_500_000,     'NewNice Premium': 3_600_000,    'NewNice Crystal': 5_500_000,    'NewNice Royal': 5_500_000    },
    },
    {
      position: 'Kính sườn (trước)',
      codes:  { 'NewNice Eco': 'NE25',        'NewNice Premium': 'NP40/NP25',  'NewNice Crystal': 'NC40/NC25',  'NewNice Royal': 'NR40/NR25'  },
      prices: { 'NewNice Eco': 500_000,       'NewNice Premium': 1_000_000,    'NewNice Crystal': 1_600_000,    'NewNice Royal': 1_600_000    },
    },
    {
      position: 'Kính sườn (sau)',
      codes:  { 'NewNice Eco': 'NE25',        'NewNice Premium': 'NP40/NP25',  'NewNice Crystal': 'NC40/NC25',  'NewNice Royal': 'NR40/NR25'  },
      prices: { 'NewNice Eco': 500_000,       'NewNice Premium': 1_050_000,    'NewNice Crystal': 1_600_000,    'NewNice Royal': 1_600_000    },
    },
    {
      position: 'Kính hậu',
      codes:  { 'NewNice Eco': 'NE25',        'NewNice Premium': 'NP15',       'NewNice Crystal': 'NC15',       'NewNice Royal': 'NR40/NR25'  },
      prices: { 'NewNice Eco': 1_200_000,     'NewNice Premium': 1_800_000,    'NewNice Crystal': 1_800_000,    'NewNice Royal': 3_800_000    },
    },
  ],
}

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


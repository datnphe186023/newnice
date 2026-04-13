<template>
  <section class="py-14 bg-gray-50">
    <div class="container">
      <div class="text-center mb-10">
        <h2 class="section-title mb-3">Danh Mục Sản Phẩm</h2>
        <p class="text-gray-500 max-w-xl mx-auto">
          Khám phá các dòng sản phẩm phim chuyên dụng từ thương hiệu hàng đầu thế giới
        </p>
      </div>

      <!-- Loading skeleton -->
      <div v-if="pending" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="i in 4" :key="i" class="card animate-pulse">
          <div class="aspect-[4/3] bg-gray-200" />
          <div class="p-5 space-y-2">
            <div class="h-5 bg-gray-200 rounded w-3/4" />
            <div class="h-4 bg-gray-200 rounded w-full" />
            <div class="h-4 bg-gray-200 rounded w-1/2" />
          </div>
        </div>
      </div>

      <!-- Category grid -->
      <div v-else-if="categories?.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <NuxtLink
          v-for="category in categories"
          :key="category.slug"
          :to="`/danh-muc/${category.slug}`"
          class="card group overflow-hidden cursor-pointer"
        >
          <!-- Image -->
          <div class="relative aspect-[4/3] overflow-hidden bg-gradient-to-br from-primary-100 to-primary-200">
            <img
              v-if="category.image"
              :src="category.image"
              :alt="category.name"
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              loading="lazy"
            />
            <!-- Fallback icon for categories with no image -->
            <div v-else class="w-full h-full flex items-center justify-center">
              <component
                :is="getCategoryIcon(category.slug)"
                class="w-16 h-16 text-primary-400 group-hover:scale-110 transition-transform duration-300"
              />
            </div>
            <!-- Dark overlay on hover -->
            <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300" />
            <!-- Arrow icon appearing on hover -->
            <div class="absolute bottom-3 right-3 w-9 h-9 bg-white/0 group-hover:bg-white/90 rounded-full flex items-center justify-center transition-all duration-300 translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100">
              <ArrowRightIcon class="w-4 h-4 text-primary-600" />
            </div>
          </div>

          <!-- Info -->
          <div class="p-5">
            <h3
              class="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors mb-1.5 text-base"
            >
              {{ category.name }}
            </h3>
            <p v-if="category.description" class="text-sm text-gray-500 line-clamp-2">
              {{ category.description }}
            </p>
            <!-- Product count badge (static for now) -->
            <div class="mt-3 flex items-center gap-1.5 text-xs text-primary-600 font-medium">
              <span>Xem sản phẩm</span>
              <ArrowRightIcon class="w-3.5 h-3.5" />
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- Fallback static categories if API has no data -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <NuxtLink
          v-for="cat in staticCategories"
          :key="cat.slug"
          :to="`/danh-muc/${cat.slug}`"
          class="card group overflow-hidden cursor-pointer"
        >
          <div
            class="aspect-[4/3] flex items-center justify-center transition-colors duration-300"
            :class="cat.bgClass"
          >
            <component :is="cat.icon" class="w-16 h-16 transition-transform duration-300 group-hover:scale-110" :class="cat.iconClass" />
          </div>
          <div class="p-5">
            <h3 class="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors mb-1.5">
              {{ cat.name }}
            </h3>
            <p class="text-sm text-gray-500">{{ cat.description }}</p>
            <div class="mt-3 flex items-center gap-1.5 text-xs text-primary-600 font-medium">
              <span>Xem sản phẩm</span>
              <ArrowRightIcon class="w-3.5 h-3.5" />
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- View all link -->
      <div class="text-center mt-10">
        <NuxtLink to="/san-pham" class="btn-outline">
          Xem tất cả sản phẩm
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import {
  SunIcon,
  PaintBrushIcon,
  HomeIcon,
  ShieldCheckIcon,
  ArrowRightIcon,
  FilmIcon,
} from '@heroicons/vue/24/outline'
import type { Category } from '~/types'

const config = useRuntimeConfig()
const { data: categories, pending } = await useFetch<Category[]>(
  `${config.public.apiBase}/categories`,
  { default: () => [] }
)

const getCategoryIcon = (slug: string) => {
  const map: Record<string, unknown> = {
    'phim-cach-nhiet-o-to': SunIcon,
    'phim-doi-mau-xe': PaintBrushIcon,
    'phim-cach-nhiet-nha-kinh': HomeIcon,
    'phim-ppf': ShieldCheckIcon,
  }
  return map[slug] || FilmIcon
}

const staticCategories = [
  {
    name: 'Phim cách nhiệt ô tô',
    slug: 'phim-cach-nhiet-o-to',
    description: 'Giảm nhiệt, chống UV, bảo vệ nội thất xe',
    icon: SunIcon,
    bgClass: 'bg-amber-50 group-hover:bg-amber-100',
    iconClass: 'text-amber-400',
  },
  {
    name: 'Phim PPF',
    slug: 'phim-ppf',
    description: 'Bảo vệ sơn xe khỏi trầy xước và tác động ngoại lực',
    icon: ShieldCheckIcon,
    bgClass: 'bg-blue-50 group-hover:bg-blue-100',
    iconClass: 'text-blue-400',
  },
  {
    name: 'Phim đổi màu xe',
    slug: 'phim-doi-mau-xe',
    description: 'Đổi màu xe theo phong cách riêng với hàng trăm màu sắc',
    icon: PaintBrushIcon,
    bgClass: 'bg-purple-50 group-hover:bg-purple-100',
    iconClass: 'text-purple-400',
  },
  {
    name: 'Phim nhà kính',
    slug: 'phim-cach-nhiet-nha-kinh',
    description: 'Cách nhiệt chống nắng hiệu quả cho nhà ở và văn phòng',
    icon: HomeIcon,
    bgClass: 'bg-green-50 group-hover:bg-green-100',
    iconClass: 'text-green-400',
  },
]
</script>

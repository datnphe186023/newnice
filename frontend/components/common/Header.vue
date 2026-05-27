<template>
  <header class="bg-gray-900 shadow-sm sticky top-0 z-50">
    <!-- Top bar -->
    <div class="bg-black text-white py-2 hidden md:block border-b border-gray-800">
      <div class="container flex items-center justify-between">
        <div class="flex items-center gap-6 text-sm">
          <a href="tel:0869418104" class="flex items-center gap-2 hover:text-accent transition-colors">
            <PhoneIcon class="w-4 h-4" />
            <span>Hotline: <strong>0869 418 104</strong></span>
          </a>
          <span class="flex items-center gap-2 text-gray-400">
            <MapPinIcon class="w-4 h-4" />
            <span>311 Phúc Diễn, Nam Từ Liêm, Hà Nội</span>
          </span>
        </div>
        <div class="flex items-center gap-4 text-sm">
          <NuxtLink to="/bao-gia" class="hover:text-accent transition-colors text-gray-300">
            Báo giá nhanh
          </NuxtLink>
          <NuxtLink to="/lien-he" class="hover:text-accent transition-colors text-gray-300">
            Liên hệ
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- Main header -->
    <div class="container py-3">
      <div class="flex items-center justify-between gap-4">
        <!-- Logo -->
        <NuxtLink to="/" class="flex-shrink-0">
          <img src="/logo.png" alt="Newnice" class="h-20 w-auto" />
        </NuxtLink>

        <!-- Search bar - Desktop -->
        <div class="hidden md:flex flex-1 max-w-xl mx-8">
          <div class="relative w-full">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Tìm kiếm sản phẩm..."
              class="input pr-12"
              @keyup.enter="handleSearch"
            />
            <button
              class="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-500 hover:text-primary-600"
              @click="handleSearch"
            >
              <MagnifyingGlassIcon class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-4">
          <a href="tel:0869418104" class="hidden sm:flex items-center gap-2 text-white font-semibold hover:text-accent transition-colors">
            <PhoneIcon class="w-5 h-5" />
            <span class="hidden lg:inline">0869 418 104</span>
          </a>

          <NuxtLink to="/bao-gia" class="btn-accent hidden sm:flex">
            Báo giá ngay
          </NuxtLink>

          <!-- Mobile menu button -->
          <button
            class="md:hidden p-2 text-white"
            @click="isMobileMenuOpen = true"
          >
            <Bars3Icon class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="bg-accent hidden md:block">
      <div class="container">
        <ul class="flex items-center gap-1">
          <li v-for="item in primaryMenuItems" :key="item.href">
            <NuxtLink
              :to="item.href"
              class="block px-4 py-3 text-white font-medium hover:bg-accent-600 transition-colors text-sm tracking-wide uppercase"
              :class="{ 'bg-accent-600': isActiveRoute(item.href) }"
            >
              {{ item.label }}
            </NuxtLink>
          </li>

          <li
            class="relative"
            @mouseenter="isCategoryMenuOpen = true"
            @mouseleave="isCategoryMenuOpen = false"
          >
            <button
              type="button"
              class="flex items-center gap-1 px-4 py-3 text-white font-medium hover:bg-accent-600 transition-colors text-sm tracking-wide uppercase"
              :class="{ 'bg-accent-600': isActiveRoute('/danh-muc') }"
              @click="isCategoryMenuOpen = !isCategoryMenuOpen"
              @focus="isCategoryMenuOpen = true"
              @keydown.escape="isCategoryMenuOpen = false"
            >
              Danh mục
              <ChevronDownIcon
                class="h-4 w-4 transition-transform"
                :class="{ 'rotate-180': isCategoryMenuOpen }"
              />
            </button>

            <div
              v-show="isCategoryMenuOpen"
              class="absolute left-0 top-full min-w-64 rounded-b bg-white py-2 shadow-xl ring-1 ring-black/5"
            >
              <NuxtLink
                v-for="category in categoryMenuItems"
                :key="category.href"
                :to="category.href"
                class="block px-4 py-2.5 text-sm font-semibold text-gray-800 hover:bg-gray-100 hover:text-primary-600"
                :class="{ 'bg-gray-100 text-primary-600': isActiveRoute(category.href) }"
                @click="isCategoryMenuOpen = false"
              >
                {{ category.label }}
              </NuxtLink>
              <div
                v-if="!categoryMenuItems.length"
                class="px-4 py-2.5 text-sm text-gray-500"
              >
                Chưa có danh mục
              </div>
            </div>
          </li>

          <li v-for="item in secondaryMenuItems" :key="item.href">
            <NuxtLink
              :to="item.href"
              class="block px-4 py-3 text-white font-medium hover:bg-accent-600 transition-colors text-sm tracking-wide uppercase"
              :class="{ 'bg-accent-600': isActiveRoute(item.href) }"
            >
              {{ item.label }}
            </NuxtLink>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Mobile Menu -->
    <CommonMobileMenu
      :is-open="isMobileMenuOpen"
      :menu-items="menuItems"
      :category-items="categoryMenuItems"
      @close="isMobileMenuOpen = false"
    />
  </header>
</template>

<script setup lang="ts">
import {
  PhoneIcon,
  MapPinIcon,
  MagnifyingGlassIcon,
  Bars3Icon,
  ChevronDownIcon,
} from '@heroicons/vue/24/outline'
import type { Category } from '~/types'

const route = useRoute()
const router = useRouter()
const config = useRuntimeConfig()

const searchQuery = ref('')
const isMobileMenuOpen = ref(false)
const isCategoryMenuOpen = ref(false)

const { data: categories } = await useFetch<Category[]>(`${config.public.apiBase}/categories`, {
  key: 'header-categories',
  default: () => [],
})

const primaryMenuItems = [
  { label: 'Trang chủ', href: '/' },
]

const secondaryMenuItems = [
  { label: 'Tất cả sản phẩm', href: '/san-pham' },
  { label: 'Tin tức', href: '/tin-tuc' },
  { label: 'Liên hệ', href: '/lien-he' },
]

const menuItems = [...primaryMenuItems, ...secondaryMenuItems]

const categoryMenuItems = computed(() =>
  (categories.value || [])
    .filter((category) => category.is_active)
    .slice()
    .sort((left, right) => left.sort_order - right.sort_order)
    .map((category) => ({
      label: category.name,
      href: `/danh-muc/${category.slug}`,
    })),
)

const isActiveRoute = (href: string) => {
  if (href === '/') return route.path === '/'
  return route.path.startsWith(href)
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/san-pham?search=${encodeURIComponent(searchQuery.value)}`)
  }
}
</script>

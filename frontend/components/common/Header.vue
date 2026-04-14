<template>
  <header class="bg-white shadow-sm sticky top-0 z-50">
    <!-- Top bar -->
    <div class="bg-dark text-white py-2 hidden md:block">
      <div class="container flex items-center justify-between">
        <div class="flex items-center gap-6 text-sm">
          <a href="tel:0869418104" class="flex items-center gap-2 hover:text-accent transition-colors">
            <PhoneIcon class="w-4 h-4" />
            <span>Hotline: <strong>0869 418 104</strong></span>
          </a>
          <span class="flex items-center gap-2">
            <MapPinIcon class="w-4 h-4" />
            <span>311 Phúc Diễn, Nam Từ Liêm, Hà Nội</span>
          </span>
        </div>
        <div class="flex items-center gap-4 text-sm">
          <NuxtLink to="/bao-gia" class="hover:text-accent transition-colors">
            Báo giá nhanh
          </NuxtLink>
          <NuxtLink to="/lien-he" class="hover:text-accent transition-colors">
            Liên hệ
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- Main header -->
    <div class="container py-4">
      <div class="flex items-center justify-between gap-4">
        <!-- Logo -->
        <NuxtLink to="/" class="flex-shrink-0 flex items-center gap-0.5">
          <span class="text-2xl font-black tracking-tight text-gray-900 uppercase">New</span>
          <span class="relative text-2xl font-black tracking-tight text-primary-600 uppercase">
            Nice
            <!-- swoosh star accent -->
            <svg class="absolute -top-1 -right-2 w-3 h-3 text-primary-500" viewBox="0 0 12 12" fill="currentColor">
              <polygon points="6,0 7.5,4.5 12,4.5 8.5,7 10,12 6,9 2,12 3.5,7 0,4.5 4.5,4.5"/>
            </svg>
          </span>
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
          <a href="tel:0869418104" class="hidden sm:flex items-center gap-2 text-primary-600 font-semibold">
            <PhoneIcon class="w-5 h-5" />
            <span class="hidden lg:inline">0869 418 104</span>
          </a>
          
          <NuxtLink to="/bao-gia" class="btn-primary hidden sm:flex">
            Báo giá ngay
          </NuxtLink>

          <!-- Mobile menu button -->
          <button 
            class="md:hidden p-2"
            @click="isMobileMenuOpen = true"
          >
            <Bars3Icon class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="bg-primary-600 hidden md:block">
      <div class="container">
        <ul class="flex items-center gap-1">
          <li v-for="item in menuItems" :key="item.href">
            <NuxtLink 
              :to="item.href" 
              class="block px-4 py-3 text-white font-medium hover:bg-primary-700 transition-colors"
              :class="{ 'bg-primary-700': isActiveRoute(item.href) }"
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
      @close="isMobileMenuOpen = false" 
    />
  </header>
</template>

<script setup lang="ts">
import { 
  PhoneIcon, 
  MapPinIcon, 
  MagnifyingGlassIcon,
  Bars3Icon 
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()

const searchQuery = ref('')
const isMobileMenuOpen = ref(false)

const menuItems = [
  { label: 'Trang chủ', href: '/' },
  { label: 'Phim cách nhiệt 3M', href: '/danh-muc/phim-cach-nhiet-3m' },
  { label: 'Phim cách nhiệt Newnice', href: '/danh-muc/phim-cach-nhiet-newnice' },
  { label: 'Tất cả sản phẩm', href: '/san-pham' },
  { label: 'Tin tức', href: '/tin-tuc' },
  { label: 'Giới thiệu', href: '/gioi-thieu' },
  { label: 'Liên hệ', href: '/lien-he' },
]

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

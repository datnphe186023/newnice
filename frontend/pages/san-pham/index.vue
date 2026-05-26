<template>
  <div>
    <!-- Breadcrumb -->
    <div class="bg-gray-50 py-4">
      <div class="container">
        <nav class="flex items-center gap-2 text-sm">
          <NuxtLink to="/" class="text-gray-500 hover:text-primary-600">Trang chủ</NuxtLink>
          <span class="text-gray-400">/</span>
          <span class="text-gray-900">Sản phẩm</span>
        </nav>
      </div>
    </div>

    <div class="container py-8">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Sidebar filters -->
        <aside class="lg:w-64 flex-shrink-0">
          <div class="card p-6 sticky top-24">
            <h3 class="font-semibold text-lg mb-4">Bộ lọc</h3>
            
            <!-- Categories -->
            <div class="mb-6">
              <h4 class="font-medium mb-2">Danh mục</h4>
              <ul class="space-y-2">
                <li v-for="cat in categories" :key="cat.slug">
                  <button 
                    @click="setCategoryFilter(cat.slug)"
                    class="text-sm w-full text-left py-1 hover:text-primary-600 transition-colors"
                    :class="{ 'text-primary-600 font-medium': selectedCategory === cat.slug }"
                  >
                    {{ cat.name }}
                  </button>
                </li>
              </ul>
            </div>

            <!-- Brands -->
            <div class="mb-6">
              <h4 class="font-medium mb-2">Thương hiệu</h4>
              <ul class="space-y-2">
                <li v-for="brand in brands" :key="brand.slug">
                  <button 
                    @click="setBrandFilter(brand.slug)"
                    class="text-sm w-full text-left py-1 hover:text-primary-600 transition-colors"
                    :class="{ 'text-primary-600 font-medium': selectedBrand === brand.slug }"
                  >
                    {{ brand.name }}
                  </button>
                </li>
              </ul>
            </div>

            <!-- Clear filters -->
            <button 
              v-if="selectedCategory || selectedBrand || searchQuery"
              @click="clearFilters"
              class="text-sm text-red-500 hover:text-red-600"
            >
              Xóa bộ lọc
            </button>
          </div>
        </aside>

        <!-- Products -->
        <div class="flex-1">
          <!-- Header -->
          <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold">
              {{ pageTitle }}
              <span v-if="products?.total" class="text-gray-500 font-normal text-lg">
                ({{ products.total }} sản phẩm)
              </span>
            </h1>
          </div>

          <!-- Loading -->
          <div v-if="pending" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="i in 6" :key="i" class="card animate-pulse">
              <div class="aspect-square bg-gray-200" />
              <div class="p-4 space-y-3">
                <div class="h-4 bg-gray-200 rounded w-1/2" />
                <div class="h-5 bg-gray-200 rounded" />
                <div class="h-4 bg-gray-200 rounded w-3/4" />
              </div>
            </div>
          </div>

          <!-- Error state -->
          <div v-else-if="productsError" class="text-center py-12">
            <p class="text-red-500">Không tải được danh sách sản phẩm. Vui lòng thử lại.</p>
          </div>

          <!-- Products grid -->
          <div v-else-if="products?.items.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <ProductCard 
              v-for="product in products.items" 
              :key="product.id" 
              :product="product" 
            />
          </div>

          <!-- Empty state -->
          <div v-else class="text-center py-12">
            <p class="text-gray-500">Không tìm thấy sản phẩm nào.</p>
          </div>

          <!-- Pagination -->
          <div v-if="products && products.total_pages > 1" class="flex justify-center gap-2 mt-8">
            <button 
              v-for="p in products.total_pages" 
              :key="p"
              @click="setPage(p)"
              class="w-10 h-10 rounded-lg font-medium transition-colors"
              :class="currentPage === p ? 'bg-primary-600 text-white' : 'bg-gray-100 hover:bg-gray-200'"
            >
              {{ p }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product, Category, Brand, PaginatedResponse } from '~/types'
import { buildBreadcrumbSchema, useJsonLd } from '~/composables/useJsonLd'
import { useCanonical } from '~/composables/useCanonical'

// SEO
useSeoMeta({
  title: 'Sản phẩm phim cách nhiệt ô tô | Newnice',
  description: 'Khám phá các sản phẩm phim cách nhiệt ô tô, phim đổi màu xe, phim cách nhiệt nhà kính cao cấp từ Newnice và 3M',
})
useJsonLd(buildBreadcrumbSchema([
  { name: 'Trang chủ', url: '/' },
  { name: 'Sản phẩm', url: '/san-pham' },
]))
useCanonical('/san-pham')

const route = useRoute()
const router = useRouter()
const config = useRuntimeConfig()

// Filters
const currentPage = computed(() => Number(route.query.page) || 1)
const selectedCategory = computed(() => (route.query.category as string) || '')
const selectedBrand = computed(() => (route.query.brand as string) || '')
const searchQuery = computed(() => (route.query.search as string) || '')

// Page title
const pageTitle = computed(() => {
  if (searchQuery.value) return `Kết quả tìm kiếm: "${searchQuery.value}"`
  return 'Tất cả sản phẩm'
})

// Fetch categories
const { data: categories } = await useFetch<Category[]>(`${config.public.apiBase}/categories`)

// Fetch brands
const { data: brands } = await useFetch<Brand[]>(`${config.public.apiBase}/brands`)

// Fetch products
const queryParams = computed(() => {
  const params = new URLSearchParams()
  params.append('page', String(currentPage.value))
  params.append('page_size', '12')
  if (selectedCategory.value) params.append('category_slug', selectedCategory.value)
  if (selectedBrand.value) params.append('brand_slug', selectedBrand.value)
  if (searchQuery.value) params.append('search', searchQuery.value)
  return params.toString()
})

const productsUrl = computed(() => `${config.public.apiBase}/products?${queryParams.value}`)

const { data: products, pending, error: productsError } = await useFetch<PaginatedResponse<Product>>(
  productsUrl,
  {
    key: computed(() => `products:${queryParams.value}`),
    default: () => ({
      items: [],
      total: 0,
      page: currentPage.value,
      page_size: 12,
      total_pages: 0,
    }),
  }
)

const navigateWithFilters = (filters: {
  category?: string
  brand?: string
  search?: string
  page?: number
}) => {
  const nextCategory = filters.category ?? selectedCategory.value
  const nextBrand = filters.brand ?? selectedBrand.value
  const nextSearch = filters.search ?? searchQuery.value
  const nextPage = filters.page ?? currentPage.value
  const query: Record<string, string> = {}

  if (nextCategory) query.category = nextCategory
  if (nextBrand) query.brand = nextBrand
  if (nextSearch) query.search = nextSearch
  if (nextPage > 1) query.page = String(nextPage)

  return router.push({ path: '/san-pham', query })
}

const setCategoryFilter = (slug: string) => {
  const nextCategory = selectedCategory.value === slug ? '' : slug
  navigateWithFilters({ category: nextCategory, page: 1 })
}

const setBrandFilter = (slug: string) => {
  const nextBrand = selectedBrand.value === slug ? '' : slug
  navigateWithFilters({ brand: nextBrand, page: 1 })
}

const setPage = (page: number) => {
  navigateWithFilters({ page })
}

const clearFilters = () => {
  navigateWithFilters({ category: '', brand: '', search: '', page: 1 })
}
</script>

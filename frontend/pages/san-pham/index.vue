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
                    @click="selectedCategory = selectedCategory === cat.slug ? '' : cat.slug"
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
                    @click="selectedBrand = selectedBrand === brand.slug ? '' : brand.slug"
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

          <!-- Products grid -->
          <div v-else-if="products?.items.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <ProductProductCard 
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
              @click="currentPage = p"
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

// SEO
useSeoMeta({
  title: 'Sản phẩm phim cách nhiệt ô tô | Newnice',
  description: 'Khám phá các sản phẩm phim cách nhiệt ô tô, phim đổi màu xe, phim cách nhiệt nhà kính cao cấp từ 3M, LLumar, V-KOOL, SunTek',
})

const route = useRoute()
const config = useRuntimeConfig()

// Filters
const currentPage = ref(1)
const selectedCategory = ref((route.query.category as string) || '')
const selectedBrand = ref((route.query.brand as string) || '')
const searchQuery = ref((route.query.search as string) || '')

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

const { data: products, pending, refresh } = await useFetch<PaginatedResponse<Product>>(
  () => `${config.public.apiBase}/products?${queryParams.value}`
)

// Watch for filter changes
watch([selectedCategory, selectedBrand, currentPage], () => {
  refresh()
})

const clearFilters = () => {
  selectedCategory.value = ''
  selectedBrand.value = ''
  searchQuery.value = ''
  currentPage.value = 1
}
</script>

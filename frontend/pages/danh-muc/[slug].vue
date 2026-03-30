<template>
  <div>
    <!-- Breadcrumb -->
    <div class="bg-gray-50 py-4">
      <div class="container">
        <nav class="flex items-center gap-2 text-sm">
          <NuxtLink to="/" class="text-gray-500 hover:text-primary-600">Trang chủ</NuxtLink>
          <span class="text-gray-400">/</span>
          <NuxtLink to="/san-pham" class="text-gray-500 hover:text-primary-600">Sản phẩm</NuxtLink>
          <span class="text-gray-400">/</span>
          <span class="text-gray-900">{{ category?.name || 'Danh mục' }}</span>
        </nav>
      </div>
    </div>

    <!-- Category banner -->
    <div v-if="category?.banner_image" class="relative h-64 md:h-80">
      <img 
        :src="category.banner_image" 
        :alt="category.name"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
      <div class="absolute bottom-0 left-0 right-0 p-8">
        <div class="container">
          <h1 class="text-3xl md:text-4xl font-bold text-white">{{ category.name }}</h1>
          <p v-if="category.description" class="text-white/80 mt-2 max-w-2xl">
            {{ category.description }}
          </p>
        </div>
      </div>
    </div>

    <div class="container py-8">
      <!-- Header (when no banner) -->
      <div v-if="!category?.banner_image" class="mb-8">
        <h1 class="text-2xl md:text-3xl font-bold text-gray-900">
          {{ category?.name || 'Danh mục' }}
        </h1>
        <p v-if="category?.description" class="text-gray-600 mt-2 max-w-2xl">
          {{ category.description }}
        </p>
      </div>

      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Sidebar filters -->
        <aside class="lg:w-64 flex-shrink-0">
          <div class="card p-6 sticky top-24">
            <h3 class="font-semibold text-lg mb-4">Bộ lọc</h3>
            
            <!-- Subcategories -->
            <div v-if="category?.children?.length" class="mb-6">
              <h4 class="font-medium mb-2">Danh mục con</h4>
              <ul class="space-y-2">
                <li v-for="child in category.children" :key="child.slug">
                  <NuxtLink 
                    :to="`/danh-muc/${child.slug}`"
                    class="text-sm block py-1 hover:text-primary-600 transition-colors"
                  >
                    {{ child.name }}
                  </NuxtLink>
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
              v-if="selectedBrand"
              @click="selectedBrand = ''"
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
            <p v-if="products?.total" class="text-gray-600">
              Hiển thị {{ products.items.length }} / {{ products.total }} sản phẩm
            </p>
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
            <div class="text-gray-400 mb-4">
              <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <p class="text-gray-500 mb-4">Không tìm thấy sản phẩm nào trong danh mục này.</p>
            <NuxtLink to="/san-pham" class="btn-primary">
              Xem tất cả sản phẩm
            </NuxtLink>
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

      <!-- Category SEO content -->
      <div v-if="category?.description" class="mt-12 prose prose-lg max-w-none">
        <h2>Về {{ category.name }}</h2>
        <div v-html="category.description" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product, Category, Brand, PaginatedResponse } from '~/types'

const route = useRoute()
const config = useRuntimeConfig()
const slug = computed(() => route.params.slug as string)

// Fetch category
const { data: category, error: categoryError } = await useFetch<Category>(
  () => `${config.public.apiBase}/categories/${slug.value}`
)

// Handle 404
if (categoryError.value) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Không tìm thấy danh mục',
    fatal: true
  })
}

// SEO
useSeoMeta({
  title: () => category.value?.meta_title || `${category.value?.name} | AutoFilm`,
  description: () => category.value?.meta_description || category.value?.description || `Khám phá các sản phẩm ${category.value?.name} chất lượng cao tại AutoFilm`,
  ogTitle: () => category.value?.meta_title || category.value?.name,
  ogDescription: () => category.value?.meta_description || category.value?.description,
  ogImage: () => category.value?.banner_image || category.value?.image,
})

// Filters
const currentPage = ref(1)
const selectedBrand = ref('')

// Fetch brands
const { data: brands } = await useFetch<Brand[]>(`${config.public.apiBase}/brands`)

// Fetch products
const queryParams = computed(() => {
  const params = new URLSearchParams()
  params.append('page', String(currentPage.value))
  params.append('page_size', '12')
  params.append('category_slug', slug.value)
  if (selectedBrand.value) params.append('brand_slug', selectedBrand.value)
  return params.toString()
})

const { data: products, pending, refresh } = await useFetch<PaginatedResponse<Product>>(
  () => `${config.public.apiBase}/products?${queryParams.value}`
)

// Watch for filter changes
watch([selectedBrand, currentPage], () => {
  refresh()
})

// Reset page when slug changes
watch(slug, () => {
  currentPage.value = 1
  selectedBrand.value = ''
})
</script>

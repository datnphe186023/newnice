<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Quản lý sản phẩm</h1>
      <NuxtLink to="/admin/products/new" class="btn-primary">
        + Thêm sản phẩm
      </NuxtLink>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl shadow-sm p-4 mb-6">
      <div class="flex flex-wrap gap-4">
        <input 
          v-model="search"
          type="text"
          placeholder="Tìm kiếm sản phẩm..."
          class="flex-1 min-w-[200px] px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <select 
          v-model="categoryFilter"
          class="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
        >
          <option value="">Tất cả danh mục</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.slug">
            {{ cat.name }}
          </option>
        </select>
        <select 
          v-model="brandFilter"
          class="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
        >
          <option value="">Tất cả thương hiệu</option>
          <option v-for="brand in brands" :key="brand.id" :value="brand.slug">
            {{ brand.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Products table -->
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="text-left p-4 font-medium text-gray-600">Sản phẩm</th>
              <th class="text-left p-4 font-medium text-gray-600">Danh mục</th>
              <th class="text-left p-4 font-medium text-gray-600">Thương hiệu</th>
              <th class="text-left p-4 font-medium text-gray-600">Giá</th>
              <th class="text-left p-4 font-medium text-gray-600">Trạng thái</th>
              <th class="text-right p-4 font-medium text-gray-600">Thao tác</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="product in products?.items" :key="product.id" class="hover:bg-gray-50">
              <td class="p-4">
                <div class="flex items-center gap-3">
                  <img 
                    :src="product.thumbnail || 'https://via.placeholder.com/60'"
                    :alt="product.name"
                    class="w-12 h-12 rounded-lg object-cover"
                  />
                  <div>
                    <p class="font-medium text-gray-900">{{ product.name }}</p>
                    <p class="text-sm text-gray-500">{{ product.sku }}</p>
                  </div>
                </div>
              </td>
              <td class="p-4 text-gray-600">{{ product.category?.name || '-' }}</td>
              <td class="p-4 text-gray-600">{{ product.brand?.name || '-' }}</td>
              <td class="p-4">
                <span v-if="product.is_contact_price" class="text-gray-500">Liên hệ</span>
                <span v-else class="font-medium">{{ formatPrice(product.price) }}</span>
              </td>
              <td class="p-4">
                <span 
                  class="px-2 py-1 text-xs rounded-full"
                  :class="product.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                >
                  {{ product.is_active ? 'Hiển thị' : 'Ẩn' }}
                </span>
              </td>
              <td class="p-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <NuxtLink 
                    :to="`/admin/products/${product.id}`"
                    class="p-2 text-gray-600 hover:text-primary-600 hover:bg-gray-100 rounded-lg"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </NuxtLink>
                  <button 
                    @click="confirmDelete(product)"
                    class="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty state -->
      <div v-if="!products?.items?.length" class="p-12 text-center text-gray-500">
        Không tìm thấy sản phẩm nào
      </div>

      <!-- Pagination -->
      <div v-if="products && products.total_pages > 1" class="p-4 border-t flex justify-center gap-2">
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

    <!-- Delete confirmation modal -->
    <div 
      v-if="deleteProduct"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click.self="deleteProduct = null"
    >
      <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold text-gray-900 mb-2">Xác nhận xóa</h3>
        <p class="text-gray-600 mb-6">
          Bạn có chắc chắn muốn xóa sản phẩm "{{ deleteProduct.name }}"?
        </p>
        <div class="flex gap-3 justify-end">
          <button 
            @click="deleteProduct = null"
            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            Hủy
          </button>
          <button 
            @click="handleDelete"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Xóa
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import type { Product, Category, Brand, PaginatedResponse } from '~/types'

definePageMeta({
  layout: 'admin',
})

useSeoMeta({
  title: 'Quản lý sản phẩm | AutoFilm Admin',
  robots: 'noindex, nofollow',
})

const config = useRuntimeConfig()
const authStore = useAuthStore()

// Filters
const currentPage = ref(1)
const search = ref('')
const categoryFilter = ref('')
const brandFilter = ref('')

// Delete modal
const deleteProduct = ref<Product | null>(null)

// Fetch categories and brands
const { data: categories } = await useFetch<Category[]>(`${config.public.apiBase}/categories`)
const { data: brands } = await useFetch<Brand[]>(`${config.public.apiBase}/brands`)

// Build query params
const queryParams = computed(() => {
  const params = new URLSearchParams()
  params.append('page', String(currentPage.value))
  params.append('page_size', '10')
  if (search.value) params.append('search', search.value)
  if (categoryFilter.value) params.append('category_slug', categoryFilter.value)
  if (brandFilter.value) params.append('brand_slug', brandFilter.value)
  return params.toString()
})

// Fetch products
const { data: products, refresh } = await useFetch<PaginatedResponse<Product>>(
  () => `${config.public.apiBase}/products?${queryParams.value}`
)

// Watch for filter changes (debounced)
let searchTimeout: NodeJS.Timeout
watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    refresh()
  }, 300)
})

watch([categoryFilter, brandFilter, currentPage], () => {
  refresh()
})

const formatPrice = (price?: number) => {
  if (!price) return '-'
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(price)
}

const confirmDelete = (product: Product) => {
  deleteProduct.value = product
}

const handleDelete = async () => {
  if (!deleteProduct.value || !authStore.token) return
  
  try {
    await $fetch(`${config.public.apiBase}/products/${deleteProduct.value.id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    })
    
    deleteProduct.value = null
    refresh()
  } catch (err) {
    console.error('Failed to delete product:', err)
    alert('Không thể xóa sản phẩm')
  }
}
</script>

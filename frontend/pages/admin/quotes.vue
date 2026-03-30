<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Yêu cầu báo giá</h1>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl shadow-sm p-4 mb-6">
      <div class="flex flex-wrap gap-4">
        <input 
          v-model="search"
          type="text"
          placeholder="Tìm kiếm theo tên, SĐT..."
          class="flex-1 min-w-[200px] px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <select 
          v-model="statusFilter"
          class="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
        >
          <option value="">Tất cả trạng thái</option>
          <option value="pending">Chờ xử lý</option>
          <option value="contacted">Đã liên hệ</option>
          <option value="quoted">Đã báo giá</option>
          <option value="completed">Hoàn thành</option>
          <option value="cancelled">Đã hủy</option>
        </select>
      </div>
    </div>

    <!-- Quotes table -->
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="text-left p-4 font-medium text-gray-600">Khách hàng</th>
              <th class="text-left p-4 font-medium text-gray-600">Xe</th>
              <th class="text-left p-4 font-medium text-gray-600">Dịch vụ</th>
              <th class="text-left p-4 font-medium text-gray-600">Trạng thái</th>
              <th class="text-left p-4 font-medium text-gray-600">Ngày tạo</th>
              <th class="text-right p-4 font-medium text-gray-600">Thao tác</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="quote in quotes?.items" :key="quote.id" class="hover:bg-gray-50">
              <td class="p-4">
                <div>
                  <p class="font-medium text-gray-900">{{ quote.customer_name }}</p>
                  <p class="text-sm text-gray-500">{{ quote.phone }}</p>
                  <p v-if="quote.email" class="text-sm text-gray-500">{{ quote.email }}</p>
                </div>
              </td>
              <td class="p-4 text-gray-600">
                <span v-if="quote.car_brand || quote.car_model">
                  {{ quote.car_brand }} {{ quote.car_model }} {{ quote.car_year }}
                </span>
                <span v-else class="text-gray-400">-</span>
              </td>
              <td class="p-4 text-gray-600">
                {{ quote.service_type || quote.film_type_preference || '-' }}
              </td>
              <td class="p-4">
                <select 
                  :value="quote.status"
                  @change="updateStatus(quote.id, ($event.target as HTMLSelectElement).value)"
                  class="px-2 py-1 text-sm rounded-lg border focus:ring-2 focus:ring-primary-500"
                  :class="getStatusClass(quote.status)"
                >
                  <option value="pending">Chờ xử lý</option>
                  <option value="contacted">Đã liên hệ</option>
                  <option value="quoted">Đã báo giá</option>
                  <option value="completed">Hoàn thành</option>
                  <option value="cancelled">Đã hủy</option>
                </select>
              </td>
              <td class="p-4 text-gray-600">
                {{ formatDate(quote.created_at) }}
              </td>
              <td class="p-4 text-right">
                <button 
                  @click="viewQuote = quote"
                  class="p-2 text-gray-600 hover:text-primary-600 hover:bg-gray-100 rounded-lg"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty state -->
      <div v-if="!quotes?.items?.length" class="p-12 text-center text-gray-500">
        Không tìm thấy yêu cầu báo giá nào
      </div>

      <!-- Pagination -->
      <div v-if="quotes && quotes.total_pages > 1" class="p-4 border-t flex justify-center gap-2">
        <button 
          v-for="p in quotes.total_pages" 
          :key="p"
          @click="currentPage = p"
          class="w-10 h-10 rounded-lg font-medium transition-colors"
          :class="currentPage === p ? 'bg-primary-600 text-white' : 'bg-gray-100 hover:bg-gray-200'"
        >
          {{ p }}
        </button>
      </div>
    </div>

    <!-- View quote modal -->
    <div 
      v-if="viewQuote"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click.self="viewQuote = null"
    >
      <div class="bg-white rounded-xl p-6 max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">Chi tiết yêu cầu</h3>
          <button @click="viewQuote = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="space-y-4">
          <div>
            <p class="text-sm text-gray-500">Khách hàng</p>
            <p class="font-medium">{{ viewQuote.customer_name }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Số điện thoại</p>
            <p class="font-medium">
              <a :href="`tel:${viewQuote.phone}`" class="text-primary-600">{{ viewQuote.phone }}</a>
            </p>
          </div>
          <div v-if="viewQuote.email">
            <p class="text-sm text-gray-500">Email</p>
            <p class="font-medium">
              <a :href="`mailto:${viewQuote.email}`" class="text-primary-600">{{ viewQuote.email }}</a>
            </p>
          </div>
          <div v-if="viewQuote.car_brand || viewQuote.car_model">
            <p class="text-sm text-gray-500">Thông tin xe</p>
            <p class="font-medium">{{ viewQuote.car_brand }} {{ viewQuote.car_model }} {{ viewQuote.car_year }}</p>
          </div>
          <div v-if="viewQuote.service_type">
            <p class="text-sm text-gray-500">Loại dịch vụ</p>
            <p class="font-medium">{{ viewQuote.service_type }}</p>
          </div>
          <div v-if="viewQuote.film_type_preference">
            <p class="text-sm text-gray-500">Loại phim</p>
            <p class="font-medium">{{ viewQuote.film_type_preference }}</p>
          </div>
          <div v-if="viewQuote.message">
            <p class="text-sm text-gray-500">Ghi chú</p>
            <p class="font-medium whitespace-pre-wrap">{{ viewQuote.message }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Ngày tạo</p>
            <p class="font-medium">{{ formatDateTime(viewQuote.created_at) }}</p>
          </div>
        </div>

        <div class="mt-6 pt-6 border-t flex gap-3">
          <a 
            :href="`tel:${viewQuote.phone}`"
            class="flex-1 py-2 bg-green-600 text-white text-center rounded-lg hover:bg-green-700"
          >
            Gọi điện
          </a>
          <button 
            @click="viewQuote = null"
            class="flex-1 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
          >
            Đóng
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

interface QuoteRequest {
  id: number
  customer_name: string
  phone: string
  email?: string
  car_brand?: string
  car_model?: string
  car_year?: number
  film_type_preference?: string
  service_type?: string
  message?: string
  status: string
  created_at: string
}

definePageMeta({
  layout: 'admin',
})

useSeoMeta({
  title: 'Yêu cầu báo giá | AutoFilm Admin',
  robots: 'noindex, nofollow',
})

const config = useRuntimeConfig()
const authStore = useAuthStore()

// Filters
const currentPage = ref(1)
const search = ref('')
const statusFilter = ref('')

// View modal
const viewQuote = ref<QuoteRequest | null>(null)

// Build query params
const queryParams = computed(() => {
  const params = new URLSearchParams()
  params.append('page', String(currentPage.value))
  params.append('page_size', '10')
  if (statusFilter.value) params.append('status', statusFilter.value)
  return params.toString()
})

// Fetch quotes
const { data: quotes, refresh } = await useFetch<{ items: QuoteRequest[], total: number, page: number, page_size: number, total_pages: number }>(
  () => `${config.public.apiBase}/quotes?${queryParams.value}`,
  {
    headers: authStore.token ? { Authorization: `Bearer ${authStore.token}` } : {},
  }
)

// Watch for filter changes
watch([statusFilter, currentPage], () => {
  refresh()
})

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    pending: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    contacted: 'bg-blue-50 border-blue-200 text-blue-800',
    quoted: 'bg-purple-50 border-purple-200 text-purple-800',
    completed: 'bg-green-50 border-green-200 text-green-800',
    cancelled: 'bg-gray-50 border-gray-200 text-gray-800',
  }
  return classes[status] || ''
}

const updateStatus = async (id: number, status: string) => {
  if (!authStore.token) return
  
  try {
    await $fetch(`${config.public.apiBase}/quotes/${id}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: { status },
    })
    refresh()
  } catch (err) {
    console.error('Failed to update status:', err)
  }
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('vi-VN')
}

const formatDateTime = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('vi-VN')
}
</script>

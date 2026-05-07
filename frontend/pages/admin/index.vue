<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-8">Dashboard</h1>

    <!-- Stats cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">Sản phẩm</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats?.products || 0 }}</p>
          </div>
          <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">Yêu cầu báo giá</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats?.quotes || 0 }}</p>
            <p v-if="stats?.pending_quotes" class="text-xs text-orange-500 mt-1">
              {{ stats.pending_quotes }} chờ xử lý
            </p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">Bài viết</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats?.posts || 0 }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">Liên hệ</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats?.contacts || 0 }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Price table -->
    <div class="mt-8 bg-white rounded-xl shadow-sm overflow-hidden">
      <div class="p-6 border-b flex items-center justify-between">
        <div>
          <h2 class="font-semibold text-gray-900">Bảng giá phim cách nhiệt Newnice</h2>
          <p class="text-xs text-gray-400 mt-0.5">Giá chưa bao gồm thuế VAT</p>
        </div>
        <span class="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded-full font-medium">Cập nhật mới nhất</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b">
              <th class="text-left px-4 py-3 font-semibold text-gray-700 w-44">Vị trí kính</th>
              <th v-for="pkg in priceTable.packages" :key="pkg.name"
                  class="text-center px-3 py-3 font-semibold text-gray-700 min-w-[140px]">
                {{ pkg.name }}
              </th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="row in priceTable.rows" :key="row.position" class="hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-600 font-medium">{{ row.position }}</td>
              <td v-for="pkg in priceTable.packages" :key="pkg.name" class="px-3 py-3 text-center">
                <div v-if="row.cells[pkg.name]">
                  <div class="text-xs text-gray-500">{{ row.cells[pkg.name].code }}</div>
                  <div class="font-semibold text-red-600 text-sm">
                    {{ formatVND(row.cells[pkg.name].price) }}
                  </div>
                </div>
                <span v-else class="text-gray-300">—</span>
              </td>
            </tr>
            <!-- SEDAN / SUV totals -->
            <tr class="bg-gray-50 font-semibold border-t-2 border-gray-200">
              <td class="px-4 py-3 text-gray-800">SEDAN</td>
              <td v-for="pkg in priceTable.packages" :key="pkg.name + '-sedan'"
                  class="px-3 py-3 text-center text-gray-800">
                {{ formatVND(pkg.sedan) }}
              </td>
            </tr>
            <tr class="bg-gray-50 font-semibold">
              <td class="px-4 py-3 text-gray-800">SUV</td>
              <td v-for="pkg in priceTable.packages" :key="pkg.name + '-suv'"
                  class="px-3 py-3 text-center text-gray-800">
                {{ formatVND(pkg.suv) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Recent activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent quotes -->
      <div class="bg-white rounded-xl shadow-sm">
        <div class="p-6 border-b">
          <div class="flex items-center justify-between">
            <h2 class="font-semibold text-gray-900">Yêu cầu báo giá gần đây</h2>
            <NuxtLink to="/admin/quotes" class="text-sm text-primary-600 hover:text-primary-700">
              Xem tất cả →
            </NuxtLink>
          </div>
        </div>
        <div class="divide-y">
          <div v-for="quote in recentQuotes" :key="quote.id" class="p-4 hover:bg-gray-50">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-900">{{ quote.customer_name }}</p>
                <p class="text-sm text-gray-500">{{ quote.phone }}</p>
              </div>
              <span 
                class="px-2 py-1 text-xs rounded-full"
                :class="getStatusClass(quote.status)"
              >
                {{ getStatusLabel(quote.status) }}
              </span>
            </div>
          </div>
          <div v-if="!recentQuotes?.length" class="p-8 text-center text-gray-500">
            Chưa có yêu cầu báo giá nào
          </div>
        </div>
      </div>

      <!-- Recent contacts -->
      <div class="bg-white rounded-xl shadow-sm">
        <div class="p-6 border-b">
          <div class="flex items-center justify-between">
            <h2 class="font-semibold text-gray-900">Liên hệ gần đây</h2>
            <NuxtLink to="/admin/contacts" class="text-sm text-primary-600 hover:text-primary-700">
              Xem tất cả →
            </NuxtLink>
          </div>
        </div>
        <div class="divide-y">
          <div v-for="contact in recentContacts" :key="contact.id" class="p-4 hover:bg-gray-50">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-900">{{ contact.name }}</p>
                <p class="text-sm text-gray-500 truncate max-w-xs">{{ contact.subject || contact.message }}</p>
              </div>
              <span class="text-xs text-gray-400">
                {{ formatDate(contact.created_at) }}
              </span>
            </div>
          </div>
          <div v-if="!recentContacts?.length" class="p-8 text-center text-gray-500">
            Chưa có liên hệ nào
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  layout: 'admin',
})

useSeoMeta({
  title: 'Dashboard | Newnice Admin',
  robots: 'noindex, nofollow',
})

const config = useRuntimeConfig()
const authStore = useAuthStore()

// Placeholder data - will be replaced with API calls
const stats = ref({
  products: 0,
  quotes: 0,
  pending_quotes: 0,
  posts: 0,
  contacts: 0,
})

const recentQuotes = ref<any[]>([])
const recentContacts = ref<any[]>([])

// Fetch dashboard data
onMounted(async () => {
  authStore.initAuth()
  if (!authStore.isAuthenticated) return
  
  try {
    const headers = { Authorization: `Bearer ${authStore.token}` }

    const [productsRes, quotesRes, contactsRes, postsRes] = await Promise.all([
      $fetch<{ total: number }>(`${config.public.apiBase}/products?page=1&page_size=1`),
      $fetch<{ total: number; items: any[] }>(`${config.public.apiBase}/quotes?page=1&page_size=5`, { headers }),
      $fetch<{ total: number; items: any[] }>(`${config.public.apiBase}/contacts?page=1&page_size=5`, { headers }),
      $fetch<{ total: number }>(`${config.public.apiBase}/admin/posts?page=1&page_size=1`, { headers }),
    ])

    stats.value = {
      products: productsRes.total || 0,
      quotes: quotesRes.total || 0,
      pending_quotes: (quotesRes.items || []).filter((q) => q.status === 'pending').length,
      posts: postsRes.total || 0,
      contacts: contactsRes.total || 0,
    }

    recentQuotes.value = quotesRes.items || []
    recentContacts.value = contactsRes.items || []
  } catch (err) {
    console.error('Failed to fetch dashboard data:', err)
  }
})

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    contacted: 'bg-blue-100 text-blue-800',
    quoted: 'bg-purple-100 text-purple-800',
    completed: 'bg-green-100 text-green-800',
    cancelled: 'bg-gray-100 text-gray-800',
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    pending: 'Chờ xử lý',
    contacted: 'Đã liên hệ',
    quoted: 'Đã báo giá',
    completed: 'Hoàn thành',
    cancelled: 'Đã hủy',
  }
  return labels[status] || status
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('vi-VN')
}

// ── Price table (Newnice) ───────────────────────────────────────────────────
const formatVND = (n?: number) =>
  n ? new Intl.NumberFormat('vi-VN').format(n) + ' ₫' : '—'

const priceTable = {
  packages: [
    { name: 'Eco',     sedan:  5_800_000, suv:  7_000_000 },
    { name: 'Premium', sedan: 10_500_000, suv: 11_500_000 },
    { name: 'Crystal', sedan: 12_500_000, suv: 14_500_000 },
    { name: 'Royal',   sedan: 15_500_000, suv: 17_500_000 },
  ],
  rows: [
    {
      position: 'Kính lái',
      cells: {
        'Eco':     { code: 'NE75',       price: 2_500_000 },
        'Premium': { code: 'NP62/NP66',  price: 3_600_000 },
        'Crystal': { code: 'HD/NC60-70', price: 5_500_000 },
        'Royal':   { code: 'NR/60-70',   price: 5_500_000 },
      },
    },
    {
      position: 'Kính sườn (trước)',
      cells: {
        'Eco':     { code: 'NE25',      price: 500_000   },
        'Premium': { code: 'NP40/NP25', price: 1_000_000 },
        'Crystal': { code: 'NC40/NC25', price: 1_600_000 },
        'Royal':   { code: 'NR40/NR25', price: 1_600_000 },
      },
    },
    {
      position: 'Kính sườn (sau)',
      cells: {
        'Eco':     { code: 'NE25',      price: 500_000   },
        'Premium': { code: 'NP40/NP25', price: 1_050_000 },
        'Crystal': { code: 'NC40/NC25', price: 1_600_000 },
        'Royal':   { code: 'NR40/NR25', price: 1_600_000 },
      },
    },
    {
      position: 'Kính hậu',
      cells: {
        'Eco':     { code: 'NE25', price: 1_200_000 },
        'Premium': { code: 'NP15', price: 1_800_000 },
        'Crystal': { code: 'NC15', price: 1_800_000 },
        'Royal':   { code: 'NR40/NR25', price: 3_800_000 },
      },
    },
  ],
}
</script>

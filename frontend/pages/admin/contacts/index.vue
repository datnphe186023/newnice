<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Tin nhắn liên hệ</h1>
    </div>

    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="text-left p-4 font-medium text-gray-600">Người gửi</th>
              <th class="text-left p-4 font-medium text-gray-600">Liên hệ</th>
              <th class="text-left p-4 font-medium text-gray-600">Nội dung</th>
              <th class="text-left p-4 font-medium text-gray-600">Ngày tạo</th>
              <th class="text-center p-4 font-medium text-gray-600">Trạng thái</th>
              <th class="text-right p-4 font-medium text-gray-600">Thao tác</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="item in contacts?.items" :key="item.id" class="hover:bg-gray-50">
              <td class="p-4 font-medium text-gray-900">{{ item.name }}</td>
              <td class="p-4 text-gray-600">
                <div>{{ item.email }}</div>
                <div class="text-sm text-gray-500">{{ item.phone || '-' }}</div>
              </td>
              <td class="p-4 text-gray-600">
                <div class="font-medium">{{ item.subject || 'Không có chủ đề' }}</div>
                <div class="text-sm text-gray-500 line-clamp-2">{{ item.message }}</div>
              </td>
              <td class="p-4 text-gray-500">{{ formatDate(item.created_at) }}</td>
              <td class="p-4 text-center">
                <span
                  class="px-2 py-1 rounded-full text-xs"
                  :class="item.is_read ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
                >
                  {{ item.is_read ? 'Đã đọc' : 'Chưa đọc' }}
                </span>
              </td>
              <td class="p-4 text-right">
                <button
                  v-if="!item.is_read"
                  @click="markRead(item.id)"
                  class="px-3 py-1.5 rounded-lg bg-primary-600 text-white hover:bg-primary-700"
                >
                  Đánh dấu đã đọc
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="!contacts?.items?.length" class="p-12 text-center text-gray-500">Chưa có tin nhắn liên hệ</div>

      <div v-if="contacts && contacts.total_pages > 1" class="p-4 border-t flex justify-center gap-2">
        <button
          v-for="p in contacts.total_pages"
          :key="p"
          @click="currentPage = p"
          class="w-10 h-10 rounded-lg font-medium"
          :class="currentPage === p ? 'bg-primary-600 text-white' : 'bg-gray-100 hover:bg-gray-200'"
        >
          {{ p }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import type { PaginatedResponse } from '~/types'

definePageMeta({ layout: 'admin' })
useSeoMeta({ title: 'Liên hệ | Newnice Admin', robots: 'noindex, nofollow' })

const config = useRuntimeConfig()
const authStore = useAuthStore()

interface ContactItem {
  id: number
  name: string
  phone?: string
  email: string
  subject?: string
  message: string
  is_read: boolean
  created_at: string
}

const currentPage = ref(1)

const headers = computed(() => (authStore.token ? { Authorization: `Bearer ${authStore.token}` } : {}))
const endpoint = computed(() => `${config.public.apiBase}/contacts?page=${currentPage.value}&page_size=10`)

const { data: contacts, refresh } = await useFetch<PaginatedResponse<ContactItem>>(endpoint, {
  headers,
  watch: [endpoint, headers],
})

onMounted(() => {
  authStore.initAuth()
  refresh()
})

const markRead = async (id: number) => {
  await $fetch(`${config.public.apiBase}/contacts/${id}/read`, {
    method: 'PUT',
    headers: headers.value,
  })
  refresh()
}

const formatDate = (value: string) => new Date(value).toLocaleString('vi-VN')
</script>

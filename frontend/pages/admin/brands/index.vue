<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Quản lý thương hiệu</h1>
      <button
        @click="openCreateModal"
        class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
      >
        + Thêm thương hiệu
      </button>
    </div>

    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="text-left p-4 font-medium text-gray-600">Logo</th>
              <th class="text-left p-4 font-medium text-gray-600">Tên</th>
              <th class="text-left p-4 font-medium text-gray-600">Quốc gia</th>
              <th class="text-left p-4 font-medium text-gray-600">Slug</th>
              <th class="text-center p-4 font-medium text-gray-600">Trạng thái</th>
              <th class="text-right p-4 font-medium text-gray-600">Thao tác</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="brand in brands" :key="brand.id" class="hover:bg-gray-50">
              <td class="p-4">
                <img
                  v-if="brand.logo"
                  :src="brand.logo"
                  :alt="brand.name"
                  class="w-12 h-12 object-cover rounded-lg"
                />
                <div v-else class="w-12 h-12 bg-gray-100 rounded-lg" />
              </td>
              <td class="p-4 text-gray-900 font-medium">{{ brand.name }}</td>
              <td class="p-4 text-gray-600">{{ brand.country || '-' }}</td>
              <td class="p-4 text-gray-500 font-mono text-sm">{{ brand.slug }}</td>
              <td class="p-4 text-center">
                <span
                  class="px-2 py-1 rounded-full text-xs"
                  :class="brand.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
                >
                  {{ brand.is_active ? 'Hiển thị' : 'Ẩn' }}
                </span>
              </td>
              <td class="p-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button
                    @click="editBrand(brand)"
                    class="p-2 text-gray-600 hover:text-primary-600 hover:bg-gray-100 rounded-lg"
                  >
                    Sửa
                  </button>
                  <button
                    @click="confirmDelete(brand)"
                    class="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    Xóa
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="!brands.length" class="p-12 text-center text-gray-500">Chưa có thương hiệu nào</div>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-xl p-6 max-w-lg w-full mx-4">
        <h3 class="text-lg font-semibold text-gray-900 mb-5">
          {{ editingBrand ? 'Chỉnh sửa thương hiệu' : 'Thêm thương hiệu' }}
        </h3>

        <form @submit.prevent="saveBrand" class="space-y-4">
          <div>
            <label class="block text-sm text-gray-700 mb-1">Tên thương hiệu</label>
            <input v-model="form.name" required class="w-full px-4 py-2 border rounded-lg" />
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Logo URL</label>
            <input v-model="form.logo" class="w-full px-4 py-2 border rounded-lg" />
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Quốc gia</label>
            <input v-model="form.country" class="w-full px-4 py-2 border rounded-lg" />
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Mô tả</label>
            <textarea v-model="form.description" rows="3" class="w-full px-4 py-2 border rounded-lg" />
          </div>
          <label class="flex items-center gap-2 text-sm text-gray-700">
            <input v-model="form.is_active" type="checkbox" />
            Hiển thị thương hiệu
          </label>

          <div class="flex justify-end gap-3 pt-2">
            <button type="button" @click="closeModal" class="px-4 py-2 rounded-lg text-gray-600 hover:bg-gray-100">
              Hủy
            </button>
            <button type="submit" class="px-4 py-2 rounded-lg bg-primary-600 text-white hover:bg-primary-700">
              {{ editingBrand ? 'Lưu thay đổi' : 'Tạo mới' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div
      v-if="deletingBrand"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click.self="deletingBrand = null"
    >
      <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold text-gray-900 mb-2">Xác nhận xóa</h3>
        <p class="text-gray-600 mb-5">Xóa thương hiệu "{{ deletingBrand.name }}"?</p>
        <div class="flex justify-end gap-3">
          <button @click="deletingBrand = null" class="px-4 py-2 rounded-lg text-gray-600 hover:bg-gray-100">Hủy</button>
          <button @click="deleteBrand" class="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700">Xóa</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import type { Brand } from '~/types'

definePageMeta({ layout: 'admin' })
useSeoMeta({ title: 'Quản lý thương hiệu | Newnice Admin', robots: 'noindex, nofollow' })

const config = useRuntimeConfig()
const authStore = useAuthStore()

type BrandForm = {
  name: string
  logo: string
  description: string
  country: string
  is_active: boolean
}

const brands = ref<Brand[]>([])
const showModal = ref(false)
const editingBrand = ref<Brand | null>(null)
const deletingBrand = ref<Brand | null>(null)

const defaultForm: BrandForm = {
  name: '',
  logo: '',
  description: '',
  country: '',
  is_active: true,
}
const form = ref<BrandForm>({ ...defaultForm })

const authHeaders = computed(() => ({ Authorization: `Bearer ${authStore.token}` }))

const fetchBrands = async () => {
  if (!authStore.token) return
  brands.value = await $fetch<Brand[]>(`${config.public.apiBase}/brands/admin/all`, {
    headers: authHeaders.value,
  })
}

onMounted(async () => {
  authStore.initAuth()
  await fetchBrands()
})

const openCreateModal = () => {
  editingBrand.value = null
  form.value = { ...defaultForm }
  showModal.value = true
}

const editBrand = (brand: Brand) => {
  editingBrand.value = brand
  form.value = {
    name: brand.name,
    logo: brand.logo || '',
    description: brand.description || '',
    country: brand.country || '',
    is_active: brand.is_active,
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingBrand.value = null
}

const saveBrand = async () => {
  const payload = {
    ...form.value,
    logo: form.value.logo || null,
    description: form.value.description || null,
    country: form.value.country || null,
  }

  if (editingBrand.value) {
    await $fetch(`${config.public.apiBase}/brands/${editingBrand.value.id}`, {
      method: 'PUT',
      headers: authHeaders.value,
      body: payload,
    })
  } else {
    await $fetch(`${config.public.apiBase}/brands`, {
      method: 'POST',
      headers: authHeaders.value,
      body: payload,
    })
  }

  closeModal()
  await fetchBrands()
}

const confirmDelete = (brand: Brand) => {
  deletingBrand.value = brand
}

const deleteBrand = async () => {
  if (!deletingBrand.value) return
  await $fetch(`${config.public.apiBase}/brands/${deletingBrand.value.id}`, {
    method: 'DELETE',
    headers: authHeaders.value,
  })
  deletingBrand.value = null
  await fetchBrands()
}
</script>

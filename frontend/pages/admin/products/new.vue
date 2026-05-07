<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Thêm sản phẩm</h1>
      <NuxtLink to="/admin/products" class="text-gray-600 hover:text-gray-900">← Quay lại</NuxtLink>
    </div>

    <div class="bg-white rounded-xl shadow-sm p-6">
      <form @submit.prevent="createProduct" class="space-y-5">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="block text-sm text-gray-700 mb-1">Tên sản phẩm *</label>
            <input v-model="form.name" required class="w-full px-4 py-2 border rounded-lg" />
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Mã SKU</label>
            <input v-model="form.sku" class="w-full px-4 py-2 border rounded-lg" />
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Danh mục</label>
            <select v-model="form.category_id" class="w-full px-4 py-2 border rounded-lg">
              <option :value="null">-- Chọn danh mục --</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Thương hiệu</label>
            <select v-model="form.brand_id" class="w-full px-4 py-2 border rounded-lg">
              <option :value="null">-- Chọn thương hiệu --</option>
              <option v-for="brand in brands" :key="brand.id" :value="brand.id">{{ brand.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Giá Sedan</label>
            <input v-model.number="form.price_sedan" type="number" min="0" class="w-full px-4 py-2 border rounded-lg" />
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Giá SUV</label>
            <input v-model.number="form.price_suv" type="number" min="0" class="w-full px-4 py-2 border rounded-lg" />
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm text-gray-700 mb-1">Mô tả ngắn</label>
            <textarea v-model="form.short_description" rows="2" class="w-full px-4 py-2 border rounded-lg" />
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm text-gray-700 mb-1">Mô tả chi tiết</label>
            <textarea v-model="form.description" rows="6" class="w-full px-4 py-2 border rounded-lg" />
          </div>
        </div>

        <div class="flex items-center gap-6 text-sm">
          <label class="flex items-center gap-2">
            <input v-model="form.is_contact_price" type="checkbox" />
            Giá liên hệ
          </label>
          <label class="flex items-center gap-2">
            <input v-model="form.is_featured" type="checkbox" />
            Sản phẩm nổi bật
          </label>
          <label class="flex items-center gap-2">
            <input v-model="form.is_active" type="checkbox" />
            Hiển thị
          </label>
        </div>

        <div v-if="error" class="p-3 rounded-lg bg-red-50 text-red-700 text-sm">{{ error }}</div>

        <div class="flex justify-end gap-3">
          <NuxtLink to="/admin/products" class="px-4 py-2 rounded-lg text-gray-600 hover:bg-gray-100">Hủy</NuxtLink>
          <button :disabled="saving" class="px-4 py-2 rounded-lg bg-primary-600 text-white hover:bg-primary-700 disabled:opacity-50">
            {{ saving ? 'Đang lưu...' : 'Tạo sản phẩm' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import type { Category, Brand } from '~/types'

definePageMeta({ layout: 'admin' })
useSeoMeta({ title: 'Thêm sản phẩm | Newnice Admin', robots: 'noindex, nofollow' })

const config = useRuntimeConfig()
const router = useRouter()
const authStore = useAuthStore()

type ProductForm = {
  name: string
  sku: string
  category_id: number | null
  brand_id: number | null
  short_description: string
  description: string
  price_sedan: number | null
  price_suv: number | null
  is_contact_price: boolean
  is_featured: boolean
  is_active: boolean
}

const form = ref<ProductForm>({
  name: '',
  sku: '',
  category_id: null,
  brand_id: null,
  short_description: '',
  description: '',
  price_sedan: null,
  price_suv: null,
  is_contact_price: false,
  is_featured: false,
  is_active: true,
})

const categories = ref<Category[]>([])
const brands = ref<Brand[]>([])
const saving = ref(false)
const error = ref('')

const headers = computed(() => ({ Authorization: `Bearer ${authStore.token}` }))

onMounted(async () => {
  authStore.initAuth()
  if (!authStore.token) return

  const [catRes, brandRes] = await Promise.all([
    $fetch<Category[]>(`${config.public.apiBase}/categories/admin/all`, { headers: headers.value }),
    $fetch<Brand[]>(`${config.public.apiBase}/brands/admin/all`, { headers: headers.value }),
  ])
  categories.value = catRes
  brands.value = brandRes
})

const createProduct = async () => {
  saving.value = true
  error.value = ''
  try {
    await $fetch(`${config.public.apiBase}/products`, {
      method: 'POST',
      headers: headers.value,
      body: {
        ...form.value,
        sku: form.value.sku || null,
        short_description: form.value.short_description || null,
        description: form.value.description || null,
      },
    })
    router.push('/admin/products')
  } catch (err: any) {
    error.value = err?.data?.detail || 'Không thể tạo sản phẩm'
  } finally {
    saving.value = false
  }
}
</script>

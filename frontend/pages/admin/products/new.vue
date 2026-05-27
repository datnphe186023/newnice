<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Thêm sản phẩm</h1>
      <NuxtLink to="/admin/products" class="text-gray-600 hover:text-gray-900">← Quay lại</NuxtLink>
    </div>

    <div class="bg-white rounded-xl shadow-sm p-6">
      <form class="space-y-5" @submit.prevent="createProduct">
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
          <div class="md:col-span-2">
            <label class="block text-sm text-gray-700 mb-2">Ảnh sản phẩm</label>
            <AdminImageUpload
              v-model="form.thumbnail"
              subfolder="products"
              :preview-class="'max-h-56 object-cover'"
            />
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Giá hiển thị 1</label>
            <input
              v-model="form.price_sedan"
              type="text"
              maxlength="120"
              placeholder="VD: Sedan: 5.800.000đ hoặc Theo mét: 450.000đ/m²"
              class="w-full px-4 py-2 border rounded-lg"
            />
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-1">Giá hiển thị 2</label>
            <input
              v-model="form.price_suv"
              type="text"
              maxlength="120"
              placeholder="VD: SUV: 7.000.000đ hoặc Thi công: liên hệ"
              class="w-full px-4 py-2 border rounded-lg"
            />
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
  thumbnail: string | null
  price_sedan: string
  price_suv: string
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
  thumbnail: null,
  price_sedan: '',
  price_suv: '',
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

const buildPayload = () => ({
  ...form.value,
  sku: form.value.sku || null,
  short_description: form.value.short_description || null,
  description: form.value.description || null,
  thumbnail: form.value.thumbnail || null,
  price_sedan: form.value.price_sedan.trim() || null,
  price_suv: form.value.price_suv.trim() || null,
})

const createProduct = async () => {
  saving.value = true
  error.value = ''
  try {
    await $fetch(`${config.public.apiBase}/products`, {
      method: 'POST',
      headers: headers.value,
      body: buildPayload(),
    })
    router.push('/admin/products')
  } catch (err: any) {
    error.value = err?.data?.detail || 'Không thể tạo sản phẩm'
  } finally {
    saving.value = false
  }
}
</script>

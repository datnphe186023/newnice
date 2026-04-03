<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Quản lý danh mục</h1>
      <button
        @click="openCreateModal"
        class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Thêm danh mục
      </button>
    </div>

    <!-- Categories list -->
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div class="p-4 border-b bg-gray-50">
        <p class="text-sm text-gray-600">
          Kéo thả để sắp xếp thứ tự hiển thị. Nhấn vào danh mục để chỉnh sửa.
        </p>
      </div>

      <!-- Categories table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="w-12 p-4"></th>
              <th class="text-left p-4 font-medium text-gray-600">Hình ảnh</th>
              <th class="text-left p-4 font-medium text-gray-600">Tên danh mục</th>
              <th class="text-left p-4 font-medium text-gray-600">Slug</th>
              <th class="text-center p-4 font-medium text-gray-600">Trạng thái</th>
              <th class="text-right p-4 font-medium text-gray-600">Thao tác</th>
            </tr>
          </thead>
          <tbody ref="sortableContainer" class="divide-y">
            <template v-for="category in categories" :key="category.id">
              <!-- Parent category -->
              <tr 
                :data-id="category.id"
                class="hover:bg-gray-50 cursor-move"
              >
                <td class="p-4 text-gray-400">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16" />
                  </svg>
                </td>
                <td class="p-4">
                  <img 
                    v-if="category.image" 
                    :src="getImageUrl(category.image)"
                    :alt="category.name"
                    class="w-12 h-12 object-cover rounded-lg"
                  />
                  <div v-else class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                </td>
                <td class="p-4">
                  <span class="font-medium text-gray-900">{{ category.name }}</span>
                  <span v-if="category.children?.length" class="ml-2 text-sm text-gray-500">
                    ({{ category.children.length }} danh mục con)
                  </span>
                </td>
                <td class="p-4 text-gray-500 font-mono text-sm">
                  {{ category.slug }}
                </td>
                <td class="p-4 text-center">
                  <button
                    @click.stop="toggleStatus(category)"
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors"
                    :class="category.is_active 
                      ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                  >
                    {{ category.is_active ? 'Hiển thị' : 'Ẩn' }}
                  </button>
                </td>
                <td class="p-4 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button
                      @click="editCategory(category)"
                      class="p-2 text-gray-600 hover:text-primary-600 hover:bg-gray-100 rounded-lg"
                      title="Chỉnh sửa"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      @click="confirmDelete(category)"
                      class="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                      title="Xóa"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>

              <!-- Child categories (indented) -->
              <tr 
                v-for="child in category.children" 
                :key="child.id"
                :data-id="child.id"
                class="hover:bg-gray-50 bg-gray-50/50"
              >
                <td class="p-4 text-gray-400 pl-8">
                  <svg class="w-4 h-4 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </td>
                <td class="p-4">
                  <img 
                    v-if="child.image" 
                    :src="getImageUrl(child.image)"
                    :alt="child.name"
                    class="w-10 h-10 object-cover rounded-lg"
                  />
                  <div v-else class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                </td>
                <td class="p-4">
                  <span class="text-gray-700">{{ child.name }}</span>
                </td>
                <td class="p-4 text-gray-500 font-mono text-sm">
                  {{ child.slug }}
                </td>
                <td class="p-4 text-center">
                  <button
                    @click.stop="toggleStatus(child)"
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors"
                    :class="child.is_active 
                      ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                  >
                    {{ child.is_active ? 'Hiển thị' : 'Ẩn' }}
                  </button>
                </td>
                <td class="p-4 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button
                      @click="editCategory(child)"
                      class="p-2 text-gray-600 hover:text-primary-600 hover:bg-gray-100 rounded-lg"
                      title="Chỉnh sửa"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      @click="confirmDelete(child)"
                      class="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                      title="Xóa"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>

      <!-- Empty state -->
      <div v-if="!categories?.length" class="p-12 text-center text-gray-500">
        <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <p>Chưa có danh mục nào</p>
        <button
          @click="openCreateModal"
          class="mt-4 text-primary-600 hover:text-primary-700 font-medium"
        >
          Thêm danh mục đầu tiên
        </button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div 
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-xl p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">
            {{ editingCategory ? 'Chỉnh sửa danh mục' : 'Thêm danh mục mới' }}
          </h3>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveCategory" class="space-y-6">
          <!-- Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Tên danh mục <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.name"
              type="text"
              required
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Ví dụ: Phim cách nhiệt ô tô"
            />
          </div>

          <!-- Parent Category -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Danh mục cha
            </label>
            <select
              v-model="form.parent_id"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option :value="null">-- Danh mục gốc --</option>
              <option 
                v-for="cat in parentCategories" 
                :key="cat.id" 
                :value="cat.id"
                :disabled="cat.id === editingCategory?.id"
              >
                {{ cat.name }}
              </option>
            </select>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Mô tả
            </label>
            <textarea
              v-model="form.description"
              rows="3"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Mô tả ngắn về danh mục"
            />
          </div>

          <!-- Images -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Category Image -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Hình ảnh danh mục
              </label>
              <AdminImageUpload
                v-model="form.image"
                subfolder="categories"
                :preview-class="'max-h-32 object-cover'"
              />
            </div>

            <!-- Banner Image -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Hình banner
              </label>
              <AdminImageUpload
                v-model="form.banner_image"
                subfolder="categories/banners"
                :is-banner="true"
                :preview-class="'max-h-32 object-cover w-full'"
              />
            </div>
          </div>

          <!-- SEO Fields -->
          <div class="border-t pt-6">
            <h4 class="text-sm font-medium text-gray-900 mb-4">SEO</h4>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Meta Title
                </label>
                <input
                  v-model="form.meta_title"
                  type="text"
                  class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Tiêu đề SEO (để trống sẽ dùng tên danh mục)"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Meta Description
                </label>
                <textarea
                  v-model="form.meta_description"
                  rows="2"
                  class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Mô tả SEO"
                />
              </div>
            </div>
          </div>

          <!-- Status -->
          <div class="flex items-center gap-2">
            <input
              v-model="form.is_active"
              type="checkbox"
              id="is_active"
              class="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
            />
            <label for="is_active" class="text-sm text-gray-700">
              Hiển thị danh mục
            </label>
          </div>

          <!-- Error message -->
          <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {{ error }}
          </div>

          <!-- Actions -->
          <div class="flex gap-3 pt-4 border-t">
            <button
              type="button"
              @click="closeModal"
              class="flex-1 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
            >
              Hủy
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="flex-1 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <svg v-if="saving" class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {{ editingCategory ? 'Cập nhật' : 'Tạo danh mục' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div 
      v-if="deletingCategory"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click.self="deletingCategory = null"
    >
      <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4">
        <div class="text-center">
          <div class="mx-auto w-12 h-12 rounded-full bg-red-100 flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Xóa danh mục?</h3>
          <p class="text-gray-600 mb-6">
            Bạn có chắc chắn muốn xóa danh mục <strong>{{ deletingCategory.name }}</strong>? 
            Hành động này không thể hoàn tác.
          </p>
          <div class="flex gap-3">
            <button
              @click="deletingCategory = null"
              class="flex-1 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
            >
              Hủy
            </button>
            <button
              @click="deleteCategory"
              :disabled="saving"
              class="flex-1 py-2.5 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
            >
              Xóa
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

interface Category {
  id: number
  name: string
  slug: string
  description?: string
  image?: string
  banner_image?: string
  parent_id?: number | null
  sort_order: number
  is_active: boolean
  meta_title?: string
  meta_description?: string
  children?: Category[]
  created_at: string
  updated_at: string
}

interface CategoryForm {
  name: string
  description: string
  image: string | null
  banner_image: string | null
  parent_id: number | null
  is_active: boolean
  meta_title: string
  meta_description: string
}

definePageMeta({
  layout: 'admin',
})

useSeoMeta({
  title: 'Quản lý danh mục | AutoFilm Admin',
  robots: 'noindex, nofollow',
})

const config = useRuntimeConfig()
const authStore = useAuthStore()

// State
const categories = ref<Category[]>([])
const showModal = ref(false)
const editingCategory = ref<Category | null>(null)
const deletingCategory = ref<Category | null>(null)
const saving = ref(false)
const error = ref<string | null>(null)

// Form
const defaultForm: CategoryForm = {
  name: '',
  description: '',
  image: null,
  banner_image: null,
  parent_id: null,
  is_active: true,
  meta_title: '',
  meta_description: '',
}

const form = ref<CategoryForm>({ ...defaultForm })

// Computed
const parentCategories = computed(() => {
  // Only root categories can be parents
  return categories.value.filter(c => !c.parent_id)
})

// Get image URL
const getImageUrl = (path: string) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  const apiBase = config.public.apiBase || 'http://localhost:8000'
  return `${apiBase}${path}`
}

// Fetch categories
const fetchCategories = async () => {
  try {
    const data = await $fetch<Category[]>(`${config.public.apiBase}/categories/admin/all`, {
      headers: authStore.token ? { Authorization: `Bearer ${authStore.token}` } : {},
    })
    categories.value = data
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

// Initialize
onMounted(() => {
  fetchCategories()
})

// Modal functions
const openCreateModal = () => {
  editingCategory.value = null
  form.value = { ...defaultForm }
  error.value = null
  showModal.value = true
}

const editCategory = (category: Category) => {
  editingCategory.value = category
  form.value = {
    name: category.name,
    description: category.description || '',
    image: category.image || null,
    banner_image: category.banner_image || null,
    parent_id: category.parent_id || null,
    is_active: category.is_active,
    meta_title: category.meta_title || '',
    meta_description: category.meta_description || '',
  }
  error.value = null
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingCategory.value = null
  form.value = { ...defaultForm }
  error.value = null
}

// Save category
const saveCategory = async () => {
  if (!form.value.name.trim()) {
    error.value = 'Vui lòng nhập tên danh mục'
    return
  }

  saving.value = true
  error.value = null

  try {
    const payload = {
      ...form.value,
      parent_id: form.value.parent_id || null,
    }

    if (editingCategory.value) {
      // Update
      await $fetch(`${config.public.apiBase}/categories/${editingCategory.value.id}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'application/json',
        },
        body: payload,
      })
    } else {
      // Create
      await $fetch(`${config.public.apiBase}/categories`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'application/json',
        },
        body: payload,
      })
    }

    closeModal()
    await fetchCategories()
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Có lỗi xảy ra'
  } finally {
    saving.value = false
  }
}

// Toggle status
const toggleStatus = async (category: Category) => {
  try {
    await $fetch(`${config.public.apiBase}/categories/${category.id}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: { is_active: !category.is_active },
    })
    await fetchCategories()
  } catch (err) {
    console.error('Failed to toggle status:', err)
  }
}

// Delete
const confirmDelete = (category: Category) => {
  deletingCategory.value = category
}

const deleteCategory = async () => {
  if (!deletingCategory.value) return

  saving.value = true

  try {
    await $fetch(`${config.public.apiBase}/categories/${deletingCategory.value.id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    })
    deletingCategory.value = null
    await fetchCategories()
  } catch (err: any) {
    alert(err.data?.detail || 'Không thể xóa danh mục')
  } finally {
    saving.value = false
  }
}
</script>

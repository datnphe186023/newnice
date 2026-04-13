<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Quản lý bài viết</h1>
        <p class="text-sm text-gray-500 mt-1">{{ posts?.total || 0 }} bài viết tổng cộng</p>
      </div>
      <button
        @click="openModal()"
        class="btn-primary flex items-center gap-2"
      >
        <PlusIcon class="w-5 h-5" />
        Thêm bài viết
      </button>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl shadow-sm p-4 mb-6">
      <div class="flex flex-wrap gap-4">
        <input
          v-model="search"
          type="text"
          placeholder="Tìm kiếm bài viết..."
          class="flex-1 min-w-[200px] px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <select v-model="publishFilter" class="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500">
          <option value="">Tất cả trạng thái</option>
          <option value="published">Đã xuất bản</option>
          <option value="draft">Nháp</option>
        </select>
      </div>
    </div>

    <!-- Posts table -->
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="text-left p-4 font-medium text-gray-600">Bài viết</th>
              <th class="text-left p-4 font-medium text-gray-600">Trạng thái</th>
              <th class="text-left p-4 font-medium text-gray-600">Ngày tạo</th>
              <th class="text-right p-4 font-medium text-gray-600">Thao tác</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="post in posts?.items" :key="post.id" class="hover:bg-gray-50">
              <td class="p-4">
                <div class="flex items-center gap-3">
                  <img
                    v-if="post.thumbnail"
                    :src="post.thumbnail"
                    :alt="post.title"
                    class="w-12 h-12 rounded-lg object-cover flex-shrink-0"
                  />
                  <div v-else class="w-12 h-12 rounded-lg bg-gray-100 flex items-center justify-center flex-shrink-0">
                    <DocumentTextIcon class="w-6 h-6 text-gray-400" />
                  </div>
                  <div class="min-w-0">
                    <p class="font-medium text-gray-900 truncate max-w-xs">{{ post.title }}</p>
                    <p class="text-sm text-gray-400 truncate max-w-xs">{{ post.excerpt }}</p>
                  </div>
                </div>
              </td>
              <td class="p-4">
                <span
                  class="px-2 py-1 text-xs rounded-full font-medium"
                  :class="post.is_published
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'"
                >
                  {{ post.is_published ? 'Đã xuất bản' : 'Nháp' }}
                </span>
              </td>
              <td class="p-4 text-sm text-gray-500">
                {{ formatDate(post.created_at) }}
              </td>
              <td class="p-4">
                <div class="flex items-center justify-end gap-2">
                  <a
                    :href="`/tin-tuc/${post.slug}`"
                    target="_blank"
                    class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="Xem bài viết"
                  >
                    <EyeIcon class="w-5 h-5" />
                  </a>
                  <button
                    @click="openModal(post)"
                    class="p-2 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                    title="Chỉnh sửa"
                  >
                    <PencilSquareIcon class="w-5 h-5" />
                  </button>
                  <button
                    @click="confirmDelete(post)"
                    class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Xóa"
                  >
                    <TrashIcon class="w-5 h-5" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty state -->
      <div v-if="!posts?.items?.length" class="p-12 text-center text-gray-500">
        <DocumentTextIcon class="w-12 h-12 mx-auto mb-3 text-gray-300" />
        <p class="font-medium">Chưa có bài viết nào</p>
        <p class="text-sm mt-1">Thêm bài viết đầu tiên để bắt đầu</p>
      </div>

      <!-- Pagination -->
      <div v-if="posts && posts.total_pages > 1" class="p-4 border-t flex justify-center gap-2">
        <button
          v-for="p in posts.total_pages"
          :key="p"
          @click="currentPage = p"
          class="w-10 h-10 rounded-lg font-medium transition-colors"
          :class="currentPage === p ? 'bg-primary-600 text-white' : 'bg-gray-100 hover:bg-gray-200'"
        >
          {{ p }}
        </button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div
          v-if="showModal"
          class="fixed inset-0 z-50 flex items-start justify-center bg-black/60 p-4 overflow-y-auto"
          @click.self="showModal = false"
        >
          <div class="bg-white rounded-2xl w-full max-w-2xl my-8 shadow-2xl">
            <!-- Modal header -->
            <div class="flex items-center justify-between p-6 border-b">
              <h2 class="text-lg font-bold text-gray-900">
                {{ editingPost ? 'Chỉnh sửa bài viết' : 'Thêm bài viết mới' }}
              </h2>
              <button @click="showModal = false" class="p-2 hover:bg-gray-100 rounded-lg">
                <XMarkIcon class="w-5 h-5 text-gray-500" />
              </button>
            </div>

            <!-- Modal body -->
            <form @submit.prevent="savePost" class="p-6 space-y-5">
              <!-- Title -->
              <div>
                <label class="label">Tiêu đề <span class="text-red-500">*</span></label>
                <input
                  v-model="form.title"
                  type="text"
                  class="input"
                  placeholder="Tiêu đề bài viết..."
                  required
                  @input="autoSlug"
                />
              </div>

              <!-- Slug -->
              <div>
                <label class="label">Slug (URL)</label>
                <input v-model="form.slug" type="text" class="input" placeholder="url-bai-viet" />
              </div>

              <!-- Excerpt -->
              <div>
                <label class="label">Mô tả ngắn</label>
                <textarea v-model="form.excerpt" class="input resize-none" rows="2" placeholder="Tóm tắt bài viết..." />
              </div>

              <!-- Content -->
              <div>
                <label class="label">Nội dung</label>
                <textarea
                  v-model="form.content"
                  class="input resize-none font-mono text-sm"
                  rows="10"
                  placeholder="Nội dung bài viết (HTML hoặc Markdown)..."
                />
              </div>

              <!-- Thumbnail -->
              <div>
                <label class="label">Ảnh đại diện (URL)</label>
                <input v-model="form.thumbnail" type="url" class="input" placeholder="https://..." />
              </div>

              <!-- Publish toggle -->
              <div class="flex items-center gap-3 p-4 bg-gray-50 rounded-xl">
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="form.is_published" class="sr-only peer" />
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4
                              peer-focus:ring-primary-300 rounded-full peer
                              peer-checked:after:translate-x-full peer-checked:after:border-white
                              after:content-[''] after:absolute after:top-[2px] after:left-[2px]
                              after:bg-white after:border-gray-300 after:border after:rounded-full
                              after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600" />
                </label>
                <div>
                  <p class="font-medium text-gray-900 text-sm">
                    {{ form.is_published ? 'Xuất bản ngay' : 'Lưu nháp' }}
                  </p>
                  <p class="text-xs text-gray-500">
                    {{ form.is_published ? 'Bài viết sẽ hiển thị trên website' : 'Bài viết chỉ hiển thị trong admin' }}
                  </p>
                </div>
              </div>

              <!-- Error -->
              <p v-if="modalError" class="text-sm text-red-600 bg-red-50 p-3 rounded-lg">{{ modalError }}</p>

              <!-- Actions -->
              <div class="flex gap-3 justify-end pt-2">
                <button type="button" @click="showModal = false" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-xl">
                  Hủy
                </button>
                <button
                  type="submit"
                  :disabled="saving"
                  class="btn-primary disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  <ArrowPathIcon v-if="saving" class="w-4 h-4 animate-spin" />
                  {{ saving ? 'Đang lưu...' : (editingPost ? 'Cập nhật' : 'Tạo bài viết') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Delete confirmation modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div
          v-if="deletePost"
          class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
          @click.self="deletePost = null"
        >
          <div class="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                <TrashIcon class="w-5 h-5 text-red-600" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900">Xác nhận xóa</h3>
            </div>
            <p class="text-gray-600 mb-6">
              Bạn có chắc chắn muốn xóa bài viết
              <strong>"{{ deletePost.title }}"</strong>? Hành động này không thể hoàn tác.
            </p>
            <div class="flex gap-3 justify-end">
              <button @click="deletePost = null" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-xl">
                Hủy
              </button>
              <button @click="handleDelete" :disabled="deleting" class="px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 disabled:opacity-60">
                {{ deleting ? 'Đang xóa...' : 'Xóa' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import {
  PlusIcon,
  PencilSquareIcon,
  TrashIcon,
  EyeIcon,
  XMarkIcon,
  ArrowPathIcon,
  DocumentTextIcon,
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '~/stores/auth'
import type { PaginatedResponse } from '~/types'

definePageMeta({ layout: 'admin' })
useSeoMeta({ title: 'Quản lý bài viết | Newnice Admin', robots: 'noindex, nofollow' })

const config = useRuntimeConfig()
const authStore = useAuthStore()

interface Post {
  id: number
  title: string
  slug: string
  excerpt?: string
  content?: string
  thumbnail?: string
  is_published: boolean
  published_at?: string
  created_at: string
  updated_at: string
}

// Filters
const currentPage = ref(1)
const search = ref('')
const publishFilter = ref('')

// Modal state
const showModal = ref(false)
const editingPost = ref<Post | null>(null)
const saving = ref(false)
const modalError = ref('')

// Delete state
const deletePost = ref<Post | null>(null)
const deleting = ref(false)

// Form
const form = reactive({
  title: '',
  slug: '',
  excerpt: '',
  content: '',
  thumbnail: '',
  is_published: false,
})

// Fetch posts
const queryParams = computed(() => {
  const p = new URLSearchParams()
  p.append('page', String(currentPage.value))
  p.append('page_size', '10')
  if (search.value) p.append('search', search.value)
  if (publishFilter.value) p.append('published', publishFilter.value === 'published' ? 'true' : 'false')
  return p.toString()
})

const { data: posts, refresh } = await useFetch<PaginatedResponse<Post>>(
  () => `${config.public.apiBase}/admin/posts?${queryParams.value}`,
  {
    headers: computed(() => ({ Authorization: `Bearer ${authStore.token}` })),
  }
)

// Watch filters
let searchTimeout: ReturnType<typeof setTimeout>
watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => { currentPage.value = 1; refresh() }, 300)
})
watch([publishFilter, currentPage], () => refresh())

// Auto-generate slug from title
const autoSlug = () => {
  if (editingPost.value) return // Don't overwrite slug when editing
  form.slug = form.title
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
}

const openModal = (post?: Post) => {
  editingPost.value = post || null
  modalError.value = ''
  if (post) {
    Object.assign(form, {
      title: post.title,
      slug: post.slug,
      excerpt: post.excerpt || '',
      content: post.content || '',
      thumbnail: post.thumbnail || '',
      is_published: post.is_published,
    })
  } else {
    Object.assign(form, { title: '', slug: '', excerpt: '', content: '', thumbnail: '', is_published: false })
  }
  showModal.value = true
}

const savePost = async () => {
  if (!authStore.token) return
  saving.value = true
  modalError.value = ''

  try {
    const payload = {
      title: form.title,
      slug: form.slug || undefined,
      excerpt: form.excerpt || undefined,
      content: form.content || undefined,
      thumbnail: form.thumbnail || undefined,
      is_published: form.is_published,
    }

    if (editingPost.value) {
      await $fetch(`${config.public.apiBase}/admin/posts/${editingPost.value.id}`, {
        method: 'PATCH',
        headers: { Authorization: `Bearer ${authStore.token}` },
        body: payload,
      })
    } else {
      await $fetch(`${config.public.apiBase}/admin/posts`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${authStore.token}` },
        body: payload,
      })
    }

    showModal.value = false
    await refresh()
  } catch (err: unknown) {
    const e = err as { data?: { detail?: string } }
    modalError.value = e?.data?.detail || 'Có lỗi xảy ra, vui lòng thử lại.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (post: Post) => { deletePost.value = post }

const handleDelete = async () => {
  if (!deletePost.value || !authStore.token) return
  deleting.value = true
  try {
    await $fetch(`${config.public.apiBase}/admin/posts/${deletePost.value.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    deletePost.value = null
    await refresh()
  } catch {
    alert('Không thể xóa bài viết')
  } finally {
    deleting.value = false
  }
}

const formatDate = (d: string) => new Date(d).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>

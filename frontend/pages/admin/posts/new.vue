<template>
  <div>
    <div class="mb-8 flex items-center justify-between gap-4">
      <div>
        <NuxtLink to="/admin/posts" class="text-sm text-gray-500 hover:text-gray-700">
          ← Quay lại danh sách
        </NuxtLink>
        <h1 class="mt-2 text-2xl font-bold text-gray-900">Tạo bài viết mới</h1>
      </div>
      <NuxtLink to="/admin/posts" class="text-sm text-gray-600 hover:text-gray-900">
        Đóng
      </NuxtLink>
    </div>

    <div class="rounded-xl bg-white p-6 shadow-sm">
      <form class="space-y-6" @submit.prevent="savePost">
        <div class="grid grid-cols-1 gap-5 md:grid-cols-2">
          <div class="md:col-span-2">
            <label class="mb-1 block text-sm font-medium text-gray-700">Tiêu đề</label>
            <input v-model="form.title" type="text" required class="input" placeholder="Tiêu đề bài viết" />
          </div>

          <div class="md:col-span-2">
            <label class="mb-1 block text-sm font-medium text-gray-700">Slug</label>
            <input v-model="form.slug" type="text" class="input" placeholder="slug-bai-viet" />
          </div>

          <div class="md:col-span-2">
            <label class="mb-1 block text-sm font-medium text-gray-700">Mô tả ngắn</label>
            <textarea v-model="form.excerpt" rows="3" class="input resize-none" placeholder="Tóm tắt ngắn cho danh sách bài viết"></textarea>
          </div>

          <div class="md:col-span-2">
            <label class="mb-1 block text-sm font-medium text-gray-700">Nội dung</label>
            <textarea v-model="form.content" rows="12" class="input resize-none font-mono text-sm" placeholder="Nội dung HTML hoặc Markdown"></textarea>
          </div>

          <div class="md:col-span-2">
            <label class="mb-1 block text-sm font-medium text-gray-700">Ảnh đại diện URL</label>
            <input v-model="form.thumbnail" type="url" class="input" placeholder="https://..." />
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Meta title</label>
            <input v-model="form.meta_title" type="text" class="input" placeholder="Tiêu đề SEO" />
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Meta description</label>
            <input v-model="form.meta_description" type="text" class="input" placeholder="Mô tả SEO" />
          </div>
        </div>

        <label class="flex items-center gap-2 text-sm text-gray-700">
          <input v-model="form.is_published" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
          Xuất bản ngay
        </label>

        <p v-if="error" class="rounded-lg bg-red-50 p-3 text-sm text-red-700">{{ error }}</p>

        <div class="flex justify-end gap-3">
          <NuxtLink to="/admin/posts" class="rounded-lg px-4 py-2 text-gray-600 hover:bg-gray-100">
            Hủy
          </NuxtLink>
          <button :disabled="saving" class="rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-60">
            {{ saving ? 'Đang lưu...' : 'Tạo bài viết' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
})

useSeoMeta({
  title: 'Tạo bài viết | Newnice Admin',
  robots: 'noindex, nofollow',
})

const config = useRuntimeConfig()
const router = useRouter()
const authStore = useAuthStore()

const saving = ref(false)
const error = ref('')

const form = reactive({
  title: '',
  slug: '',
  excerpt: '',
  content: '',
  thumbnail: '',
  meta_title: '',
  meta_description: '',
  is_published: false,
})

const headers = computed(() => ({ Authorization: `Bearer ${authStore.token}` }))

const savePost = async () => {
  saving.value = true
  error.value = ''

  try {
    await $fetch(`${config.public.apiBase}/admin/posts`, {
      method: 'POST',
      headers: headers.value,
      body: {
        ...form,
        slug: form.slug || undefined,
        excerpt: form.excerpt || undefined,
        content: form.content || undefined,
        thumbnail: form.thumbnail || undefined,
        meta_title: form.meta_title || undefined,
        meta_description: form.meta_description || undefined,
      },
    })

    await router.push('/admin/posts')
  } catch (err: any) {
    error.value = err?.data?.detail || 'Không thể tạo bài viết'
  } finally {
    saving.value = false
  }
}
</script>

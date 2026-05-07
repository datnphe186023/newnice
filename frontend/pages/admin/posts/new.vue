<template>
  <div>
    <!-- Header -->
    <div class="mb-8">
      <NuxtLink to="/admin/posts" class="text-blue-600 hover:text-blue-800">
        ← Quay lại danh sách
      </NuxtLink>
      <h1 class="text-2xl font-bold text-gray-900 mt-2">{{ postId ? 'Cập nhật bài viết' : 'Tạo bài viết mới' }}</h1>
    </div>

    <!-- Form -->
    <div class="bg-white rounded-xl shadow-sm p-6">
      <form @submit.prevent="handleSubmit">
        <div class="space-y-6">
          <!-- Title -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Tiêu đề</label>
            <input 
              v-model="form.title"
              type="text"
              required
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Nhập tiêu đề bài viết"
            />
          </div>

          <!-- Content -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Nội dung</label>
            <textarea 
              v-model="form.content"
              rows="10"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Nhập nội dung bài viết"
            />
          </div>

          <!-- Excerpt -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Tóm tắt</label>
            <textarea 
              v-model="form.excerpt"
              rows="3"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Tóm tắt bài viết (hiển thị trong danh sách)"
            />
          </div>

          <!-- Meta Title -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Meta Title (SEO)</label>
            <input 
              v-model="form.meta_title"
              type="text"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Tiêu đề cho search engines"
            />
          </div>

          <!-- Meta Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Meta Description (SEO)</label>
            <textarea 
              v-model="form.meta_description"
              rows="2"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Mô tả cho search engines"
            />
          </div>

          <!-- Status -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Trạng thái</label>
            <select 
              v-model="form.is_active"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option :value="true">Xuất bản</option>
              <option :value="false">Bản nháp</option>
            </select>
          </div>

          <!-- Buttons -->
          <div class="flex gap-4">
            <button
              type="submit"
              :disabled="loading"
              class="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
            >
              {{ loading ? 'Đang lưu...' : 'Lưu' }}
            </button>
            <NuxtLink 
              to="/admin/posts"
              class="px-6 py-2 bg-gray-200 text-gray-900 rounded-lg hover:bg-gray-300"
            >
              Hủy
            </NuxtLink>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

const route = useRoute();
const router = useRouter();
const postId = computed(() => {
  const id = route.params.id;
  return id && id !== 'new' ? parseInt(id as string) : null;
});

const loading = ref(false);
const form = reactive({
  title: '',
  content: '',
  excerpt: '',
  meta_title: '',
  meta_description: '',
  is_active: true,
});

// Load existing post if editing
if (postId.value) {
  onMounted(async () => {
    try {
      // TODO: Fetch post from API
      // const post = await $fetch(`/api/v1/admin/posts/${postId.value}`);
      // Object.assign(form, post);
    } catch (error) {
      console.error('Error loading post:', error);
    }
  });
}

const handleSubmit = async () => {
  loading.value = true;
  try {
    // TODO: Submit form to API
    // if (postId.value) {
    //   await $fetch(`/api/v1/admin/posts/${postId.value}`, {
    //     method: 'PATCH',
    //     body: form,
    //   });
    // } else {
    //   await $fetch('/api/v1/admin/posts', {
    //     method: 'POST',
    //     body: form,
    //   });
    // }
    // await router.push('/admin/posts');
  } catch (error) {
    console.error('Error saving post:', error);
  } finally {
    loading.value = false;
  }
};
</script>

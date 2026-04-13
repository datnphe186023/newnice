<template>
  <div>
    <!-- Breadcrumb -->
    <div class="bg-gray-50 py-4">
      <div class="container">
        <nav class="flex items-center gap-2 text-sm">
          <NuxtLink to="/" class="text-gray-500 hover:text-primary-600">Trang chủ</NuxtLink>
          <span class="text-gray-400">/</span>
          <span class="text-gray-900">Tin tức</span>
        </nav>
      </div>
    </div>

    <div class="container py-8">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Tin tức & Kiến thức</h1>
        <p class="text-gray-600 max-w-2xl mx-auto">
          Cập nhật những thông tin mới nhất về phim cách nhiệt ô tô, phim đổi màu xe và các công nghệ bảo vệ xe hơi
        </p>
      </div>

      <!-- Loading -->
      <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="i in 6" :key="i" class="card animate-pulse">
          <div class="aspect-video bg-gray-200" />
          <div class="p-6 space-y-3">
            <div class="h-4 bg-gray-200 rounded w-1/3" />
            <div class="h-6 bg-gray-200 rounded" />
            <div class="h-4 bg-gray-200 rounded" />
            <div class="h-4 bg-gray-200 rounded w-2/3" />
          </div>
        </div>
      </div>

      <!-- Posts grid -->
      <div v-else-if="posts?.items.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <NuxtLink 
          v-for="post in posts.items" 
          :key="post.id"
          :to="`/tin-tuc/${post.slug}`"
          class="card group overflow-hidden"
        >
          <!-- Thumbnail -->
          <div class="relative aspect-video overflow-hidden">
            <img 
              :src="post.thumbnail || 'https://via.placeholder.com/600x400?text=No+Image'"
              :alt="post.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
            />
          </div>
          
          <!-- Content -->
          <div class="p-6">
            <!-- Date -->
            <p class="text-sm text-gray-500 mb-2">
              {{ formatDate(post.published_at || post.created_at) }}
            </p>
            
            <!-- Title -->
            <h2 class="font-semibold text-lg text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2 mb-3">
              {{ post.title }}
            </h2>
            
            <!-- Excerpt -->
            <p v-if="post.excerpt" class="text-gray-600 text-sm line-clamp-3">
              {{ post.excerpt }}
            </p>
            
            <!-- Read more -->
            <p class="mt-4 text-primary-600 font-medium text-sm group-hover:text-primary-700">
              Đọc thêm →
            </p>
          </div>
        </NuxtLink>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-16">
        <div class="text-gray-400 mb-4">
          <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
          </svg>
        </div>
        <p class="text-gray-500 mb-4">Chưa có bài viết nào.</p>
        <NuxtLink to="/" class="btn-primary">
          Về trang chủ
        </NuxtLink>
      </div>

      <!-- Pagination -->
      <div v-if="posts && posts.total_pages > 1" class="flex justify-center gap-2 mt-12">
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
  </div>
</template>

<script setup lang="ts">
import type { PostList, PaginatedResponse } from '~/types'
import { buildBreadcrumbSchema, useJsonLd } from '~/composables/useJsonLd'
import { useCanonical } from '~/composables/useCanonical'

// SEO
useSeoMeta({
  title: 'Tin tức & Kiến thức phim cách nhiệt | Newnice',
  description: 'Cập nhật những thông tin mới nhất về phim cách nhiệt ô tô, phim đổi màu xe, phim cách nhiệt nhà kính và các công nghệ bảo vệ xe hơi',
})
useJsonLd(buildBreadcrumbSchema([
  { name: 'Trang chủ', url: '/' },
  { name: 'Tin tức', url: '/tin-tuc' },
]))
useCanonical('/tin-tuc')

const config = useRuntimeConfig()
const currentPage = ref(1)

// Fetch posts
const { data: posts, pending, refresh } = await useFetch<PaginatedResponse<PostList>>(
  () => `${config.public.apiBase}/posts?page=${currentPage.value}&page_size=9`
)

// Watch for page changes
watch(currentPage, () => {
  refresh()
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

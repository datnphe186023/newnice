<template>
  <div>
    <!-- Breadcrumb -->
    <div class="bg-gray-50 py-4">
      <div class="container">
        <nav class="flex items-center gap-2 text-sm">
          <NuxtLink to="/" class="text-gray-500 hover:text-primary-600">Trang chủ</NuxtLink>
          <span class="text-gray-400">/</span>
          <NuxtLink to="/tin-tuc" class="text-gray-500 hover:text-primary-600">Tin tức</NuxtLink>
          <span class="text-gray-400">/</span>
          <span class="text-gray-900 truncate max-w-xs">{{ post?.title }}</span>
        </nav>
      </div>
    </div>

    <article class="container py-8">
      <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <header class="mb-8">
          <p class="text-primary-600 font-medium mb-3">
            {{ formatDate(post?.published_at || post?.created_at || '') }}
          </p>
          <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {{ post?.title }}
          </h1>
          <p v-if="post?.excerpt" class="text-xl text-gray-600">
            {{ post.excerpt }}
          </p>
        </header>

        <!-- Featured image -->
        <div v-if="post?.thumbnail" class="mb-8 rounded-xl overflow-hidden">
          <img 
            :src="post.thumbnail" 
            :alt="post.title"
            class="w-full h-auto"
          />
        </div>

        <!-- Content -->
        <div 
          v-if="post?.content"
          class="prose prose-lg max-w-none prose-headings:font-bold prose-a:text-primary-600 prose-img:rounded-lg"
          v-html="post.content"
        />

        <!-- Share and CTA -->
        <div class="mt-12 pt-8 border-t">
          <div class="flex flex-col md:flex-row items-center justify-between gap-6">
            <!-- Share buttons -->
            <div class="flex items-center gap-4">
              <span class="text-gray-600">Chia sẻ:</span>
              <button 
                @click="shareOnFacebook"
                class="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 transition-colors"
                aria-label="Share on Facebook"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.77 7.46H14.5v-1.9c0-.9.6-1.1 1-1.1h3V.5h-4.33C10.24.5 9.5 3.44 9.5 5.32v2.15h-3v4h3v12h5v-12h3.85l.42-4z"/>
                </svg>
              </button>
              <button 
                @click="copyLink"
                class="w-10 h-10 rounded-full bg-gray-200 text-gray-700 flex items-center justify-center hover:bg-gray-300 transition-colors"
                aria-label="Copy link"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                </svg>
              </button>
            </div>

            <!-- CTA -->
            <NuxtLink to="/bao-gia" class="btn-primary">
              Nhận báo giá miễn phí
            </NuxtLink>
          </div>
        </div>

        <!-- Related posts -->
        <div v-if="recentPosts?.length" class="mt-16">
          <h2 class="text-2xl font-bold mb-6">Bài viết khác</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <NuxtLink 
              v-for="relatedPost in recentPosts.filter(p => p.slug !== post?.slug).slice(0, 3)" 
              :key="relatedPost.id"
              :to="`/tin-tuc/${relatedPost.slug}`"
              class="card group overflow-hidden"
            >
              <div class="relative aspect-video overflow-hidden">
                <img 
                  :src="relatedPost.thumbnail || 'https://via.placeholder.com/400x300?text=No+Image'"
                  :alt="relatedPost.title"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  loading="lazy"
                />
              </div>
              <div class="p-4">
                <p class="text-xs text-gray-500 mb-1">
                  {{ formatDate(relatedPost.published_at || relatedPost.created_at) }}
                </p>
                <h3 class="font-medium text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2">
                  {{ relatedPost.title }}
                </h3>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>
    </article>
  </div>
</template>

<script setup lang="ts">
import type { Post, PostList } from '~/types'

const route = useRoute()
const config = useRuntimeConfig()
const slug = computed(() => route.params.slug as string)

// Fetch post
const { data: post, error } = await useFetch<Post>(
  () => `${config.public.apiBase}/posts/${slug.value}`
)

// Handle 404
if (error.value) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Không tìm thấy bài viết',
    fatal: true
  })
}

// SEO
useSeoMeta({
  title: () => post.value?.meta_title || `${post.value?.title} | AutoFilm`,
  description: () => post.value?.meta_description || post.value?.excerpt || '',
  ogTitle: () => post.value?.meta_title || post.value?.title,
  ogDescription: () => post.value?.meta_description || post.value?.excerpt,
  ogImage: () => post.value?.thumbnail,
  ogType: 'article',
  articlePublishedTime: () => post.value?.published_at,
  articleModifiedTime: () => post.value?.updated_at,
})

// JSON-LD structured data
if (post.value) {
  useJsonLd([
    buildArticleSchema(post.value),
    buildBreadcrumbSchema([
      { name: 'Trang chủ', url: '/' },
      { name: 'Tin tức', url: '/tin-tuc' },
      { name: post.value.title, url: `/tin-tuc/${post.value.slug}` },
    ]),
  ])
}

// Fetch recent posts for related section
const { data: recentPosts } = await useFetch<PostList[]>(
  `${config.public.apiBase}/posts/recent?limit=4`
)

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const shareOnFacebook = () => {
  const url = encodeURIComponent(window.location.href)
  window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank', 'width=600,height=400')
}

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    alert('Đã sao chép liên kết!')
  } catch {
    console.error('Failed to copy link')
  }
}
</script>

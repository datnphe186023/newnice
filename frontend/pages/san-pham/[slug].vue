<template>
  <div>
    <!-- Breadcrumb -->
    <div class="bg-gray-50 py-4">
      <div class="container">
        <nav class="flex items-center gap-2 text-sm">
          <NuxtLink to="/" class="text-gray-500 hover:text-primary-600">Trang chủ</NuxtLink>
          <span class="text-gray-400">/</span>
          <NuxtLink to="/san-pham" class="text-gray-500 hover:text-primary-600">Sản phẩm</NuxtLink>
          <span class="text-gray-400">/</span>
          <span class="text-gray-900">{{ product?.name }}</span>
        </nav>
      </div>
    </div>

    <div v-if="product" class="container py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <!-- Images -->
        <div>
          <div class="card overflow-hidden mb-4">
            <img 
              :src="mainImage" 
              :alt="product.name"
              class="w-full aspect-square object-cover"
            />
          </div>
          <div v-if="product.images?.length" class="grid grid-cols-4 gap-2">
            <button 
              v-for="(img, index) in [{ image_url: product.thumbnail }, ...product.images]" 
              :key="index"
              @click="mainImage = img.image_url"
              class="aspect-square rounded-lg overflow-hidden border-2 transition-colors"
              :class="mainImage === img.image_url ? 'border-primary-600' : 'border-transparent'"
            >
              <img :src="img.image_url" class="w-full h-full object-cover" />
            </button>
          </div>
        </div>

        <!-- Info -->
        <div>
          <div class="mb-4">
            <span v-if="product.brand" class="text-sm text-primary-600 font-medium">
              {{ product.brand.name }}
            </span>
          </div>
          
          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>
          
          <p v-if="product.short_description" class="text-gray-600 mb-6">
            {{ product.short_description }}
          </p>

          <!-- Specs -->
          <div v-if="hasSpecs" class="bg-gray-50 rounded-lg p-6 mb-6">
            <h3 class="font-semibold mb-4">Thông số kỹ thuật</h3>
            <div class="grid grid-cols-2 gap-4">
              <div v-if="product.vlt" class="flex justify-between">
                <span class="text-gray-500">VLT (Độ trong):</span>
                <span class="font-medium">{{ product.vlt }}%</span>
              </div>
              <div v-if="product.uv_rejection" class="flex justify-between">
                <span class="text-gray-500">Chặn UV:</span>
                <span class="font-medium">{{ product.uv_rejection }}%</span>
              </div>
              <div v-if="product.ir_rejection" class="flex justify-between">
                <span class="text-gray-500">Chặn hồng ngoại:</span>
                <span class="font-medium">{{ product.ir_rejection }}%</span>
              </div>
              <div v-if="product.heat_rejection" class="flex justify-between">
                <span class="text-gray-500">Giảm nhiệt:</span>
                <span class="font-medium">{{ product.heat_rejection }}%</span>
              </div>
              <div v-if="product.thickness" class="flex justify-between">
                <span class="text-gray-500">Độ dày:</span>
                <span class="font-medium">{{ product.thickness }}</span>
              </div>
              <div v-if="product.warranty_years" class="flex justify-between">
                <span class="text-gray-500">Bảo hành:</span>
                <span class="font-medium">{{ product.warranty_years }} năm</span>
              </div>
            </div>
          </div>

          <!-- Price -->
          <div class="mb-6">
            <span class="text-3xl font-bold text-primary-600">
              {{ product.is_contact_price ? 'Liên hệ báo giá' : formatPrice(product.price) }}
            </span>
          </div>

          <!-- CTA -->
          <div class="flex flex-wrap gap-4">
            <NuxtLink to="/bao-gia" class="btn-primary text-lg px-8">
              Yêu cầu báo giá
            </NuxtLink>
            <a href="tel:0901234567" class="btn-outline text-lg px-8">
              <PhoneIcon class="w-5 h-5 mr-2" />
              Gọi ngay
            </a>
          </div>
        </div>
      </div>

      <!-- Description -->
      <div v-if="product.description" class="card p-8 mb-12">
        <h2 class="text-2xl font-bold mb-6">Mô tả sản phẩm</h2>
        <div class="prose max-w-none" v-html="product.description" />
      </div>

      <!-- Related products -->
      <div v-if="relatedProducts?.length">
        <h2 class="text-2xl font-bold mb-6">Sản phẩm liên quan</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <ProductProductCard 
            v-for="p in relatedProducts" 
            :key="p.id" 
            :product="p" 
          />
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-else class="container py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="card aspect-square animate-pulse bg-gray-200" />
        <div class="space-y-4">
          <div class="h-8 bg-gray-200 rounded w-3/4 animate-pulse" />
          <div class="h-4 bg-gray-200 rounded w-full animate-pulse" />
          <div class="h-4 bg-gray-200 rounded w-2/3 animate-pulse" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PhoneIcon } from '@heroicons/vue/24/outline'
import type { Product } from '~/types'

const route = useRoute()
const config = useRuntimeConfig()
const slug = route.params.slug as string

// Fetch product
const { data: product } = await useFetch<Product>(
  `${config.public.apiBase}/products/${slug}`
)

// Main image
const mainImage = ref(product.value?.thumbnail || '')

watch(product, (p) => {
  if (p?.thumbnail) mainImage.value = p.thumbnail
}, { immediate: true })

// Has specs
const hasSpecs = computed(() => {
  if (!product.value) return false
  return product.value.vlt || product.value.uv_rejection || 
         product.value.ir_rejection || product.value.heat_rejection ||
         product.value.thickness || product.value.warranty_years
})

// Format price
const formatPrice = (price?: number) => {
  if (!price) return 'Liên hệ'
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(price)
}

// Related products
const { data: relatedProducts } = await useFetch<Product[]>(
  () => `${config.public.apiBase}/products/featured?limit=4`
)

// SEO
useSeoMeta({
  title: () => product.value?.meta_title || `${product.value?.name} | AutoFilm`,
  description: () => product.value?.meta_description || product.value?.short_description,
  ogTitle: () => product.value?.name,
  ogDescription: () => product.value?.short_description,
  ogImage: () => product.value?.thumbnail,
})
</script>

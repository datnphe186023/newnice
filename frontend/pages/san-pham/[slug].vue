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
          <span class="text-gray-900 line-clamp-1">{{ product?.name }}</span>
        </nav>
      </div>
    </div>

    <div v-if="product" class="container py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 mb-12">
        <!-- Image Gallery -->
        <ProductImageGallery
          :thumbnail="product.thumbnail"
          :images="product.images"
          :alt="product.name"
        />

        <!-- Info -->
        <div>
          <div class="mb-3">
            <span v-if="product.brand" class="text-sm text-primary-600 font-medium">
              {{ product.brand.name }}
            </span>
            <span v-if="product.category" class="text-sm text-gray-400 ml-2">
              • {{ product.category.name }}
            </span>
          </div>

          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>

          <p v-if="product.short_description" class="text-gray-600 mb-6 leading-relaxed">
            {{ product.short_description }}
          </p>

          <!-- Specs table -->
          <div v-if="hasSpecs" class="mb-6">
            <ProductSpecsTable
              :vlt="product.vlt"
              :uv-rejection="product.uv_rejection"
              :ir-rejection="product.ir_rejection"
              :heat-rejection="product.heat_rejection"
              :thickness="product.thickness"
              :warranty-years="product.warranty_years"
              :film-type="product.film_type"
            />
          </div>

          <!-- Price -->
          <div class="mb-6">
            <div v-if="product.is_contact_price" class="text-2xl font-bold text-primary-600">
              Liên hệ báo giá
            </div>
            <div v-else class="space-y-2">
              <div
                v-for="price in productPriceLines"
                :key="price"
                class="text-2xl font-bold text-primary-600"
              >
                {{ price }}
              </div>
              <p v-if="productPriceLines.length" class="text-xs text-gray-400 mt-1">
                Giá tham khảo, chi tiết theo hạng mục thi công thực tế.
              </p>
            </div>
          </div>

          <!-- CTA -->
          <div class="flex flex-wrap gap-4">
            <NuxtLink to="/bao-gia" class="btn-primary text-lg px-8">
              Yêu cầu báo giá
            </NuxtLink>
            <a href="tel:0869418104" class="btn-outline text-lg px-8" @click="trackPhoneClick('0869418104')">
              <PhoneIcon class="w-5 h-5 mr-2" />
              Gọi ngay
            </a>
          </div>

          <!-- Trust badges -->
          <div class="mt-6 pt-6 border-t border-gray-100 flex flex-wrap gap-4 text-sm text-gray-500">
            <span class="flex items-center gap-1.5">
              <ShieldCheckIcon class="w-4 h-4 text-green-500" />
              Sản phẩm chính hãng
            </span>
            <span class="flex items-center gap-1.5">
              <StarIcon class="w-4 h-4 text-amber-400" />
              Bảo hành {{ product.warranty_years ? `${product.warranty_years} năm` : 'theo NSX' }}
            </span>
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
        <ProductProductGrid :products="relatedProducts" :columns="4" />
      </div>
    </div>

    <!-- Loading skeleton -->
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
import { PhoneIcon, ShieldCheckIcon, StarIcon } from '@heroicons/vue/24/outline'
import type { Product } from '~/types'
import { usePhoneTracking } from '~/composables/usePhoneTracking'

const route = useRoute()
const config = useRuntimeConfig()
const slug = route.params.slug as string
const { $gtag } = useNuxtApp()
const { trackPhoneClick } = usePhoneTracking()

// Fetch product
const { data: product } = await useFetch<Product>(
  `${config.public.apiBase}/products/${slug}`
)

// Has specs
const hasSpecs = computed(() => {
  if (!product.value) return false
  return product.value.vlt || product.value.uv_rejection ||
         product.value.ir_rejection || product.value.heat_rejection ||
         product.value.thickness || product.value.warranty_years ||
         product.value.film_type
})

const productPriceLines = computed(() => {
  if (!product.value) return []
  return [product.value.price_sedan, product.value.price_suv].filter(Boolean)
})

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

// JSON-LD structured data
if (product.value) {
  useJsonLd([
    buildProductSchema(product.value),
    buildBreadcrumbSchema([
      { name: 'Trang chủ', url: '/' },
      { name: 'Sản phẩm', url: '/san-pham' },
      { name: product.value.name, url: `/san-pham/${product.value.slug}` },
    ]),
  ])
}

// GA4: track product view on mount
onMounted(() => {
  if (product.value) {
    $gtag('event', 'view_item', {
      item_id: String(product.value.id),
      item_name: product.value.name,
      item_category: product.value.category?.name,
      item_brand: product.value.brand?.name,
    })
  }
})
</script>

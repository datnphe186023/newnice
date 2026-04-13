<template>
  <section class="py-14">
    <div class="container">
      <!-- Section header -->
      <div class="flex items-end justify-between mb-10">
        <div>
          <p class="text-primary-600 font-semibold text-sm uppercase tracking-wider mb-2">Được yêu thích nhất</p>
          <h2 class="section-title">Sản Phẩm Nổi Bật</h2>
        </div>
        <NuxtLink
          to="/san-pham"
          class="hidden sm:flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium transition-colors group"
        >
          Xem tất cả
          <ArrowRightIcon class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </NuxtLink>
      </div>

      <!-- Loading skeleton -->
      <div v-if="pending" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="i in 8" :key="i" class="card animate-pulse">
          <div class="aspect-square bg-gray-200" />
          <div class="p-4 space-y-3">
            <div class="h-3 bg-gray-200 rounded w-1/3" />
            <div class="h-5 bg-gray-200 rounded" />
            <div class="h-4 bg-gray-200 rounded w-3/4" />
            <div class="flex gap-2">
              <div class="h-6 bg-gray-200 rounded w-16" />
              <div class="h-6 bg-gray-200 rounded w-16" />
            </div>
          </div>
        </div>
      </div>

      <!-- Products grid -->
      <div v-else-if="products?.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-16">
        <FilmIcon class="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-500">Chưa có sản phẩm nổi bật.</p>
      </div>

      <!-- Mobile "view all" -->
      <div class="text-center mt-8 sm:hidden">
        <NuxtLink to="/san-pham" class="btn-outline">
          Xem tất cả sản phẩm
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ArrowRightIcon, FilmIcon } from '@heroicons/vue/24/outline'
import type { Product } from '~/types'

const config = useRuntimeConfig()
const { data: products, pending } = await useFetch<Product[]>(
  `${config.public.apiBase}/products/featured?limit=8`,
  { default: () => [] }
)
</script>

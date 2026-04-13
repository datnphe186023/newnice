<template>
  <div>
    <!-- Loading -->
    <div v-if="pending" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in skeletonCount" :key="i" class="card animate-pulse">
        <div class="aspect-square bg-gray-200" />
        <div class="p-4 space-y-3">
          <div class="h-3 bg-gray-200 rounded w-1/3" />
          <div class="h-5 bg-gray-200 rounded" />
          <div class="h-4 bg-gray-200 rounded w-3/4" />
          <div class="flex gap-2">
            <div class="h-6 bg-gray-200 rounded w-14" />
            <div class="h-6 bg-gray-200 rounded w-14" />
          </div>
        </div>
      </div>
    </div>

    <!-- Grid -->
    <div v-else-if="products?.length" :class="gridClass">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </div>

    <!-- Empty state -->
    <div v-else class="text-center py-16">
      <slot name="empty">
        <FilmIcon class="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-500 text-lg mb-2">Không tìm thấy sản phẩm nào</p>
        <p class="text-gray-400 text-sm">Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm</p>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FilmIcon } from '@heroicons/vue/24/outline'
import type { Product } from '~/types'

const props = withDefaults(defineProps<{
  products?: Product[]
  pending?: boolean
  columns?: 2 | 3 | 4
  skeletonCount?: number
}>(), {
  columns: 3,
  skeletonCount: 6,
})

const gridClass = computed(() => {
  const colMap = {
    2: 'grid grid-cols-1 sm:grid-cols-2 gap-6',
    3: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6',
    4: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6',
  }
  return colMap[props.columns]
})
</script>

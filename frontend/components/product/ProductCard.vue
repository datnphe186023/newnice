<template>
  <NuxtLink :to="`/san-pham/${product.slug}`" class="card group">
    <!-- Image -->
    <div class="relative aspect-square overflow-hidden">
      <img
        :src="product.thumbnail || 'https://via.placeholder.com/400x400?text=No+Image'"
        :alt="product.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        loading="lazy"
      />

      <!-- Featured badge -->
      <span
        v-if="product.is_featured"
        class="absolute top-3 left-3 bg-accent text-white text-xs font-semibold px-2 py-1 rounded"
      >
        Nổi bật
      </span>

      <!-- Brand badge -->
      <span
        v-if="product.brand"
        class="absolute top-3 right-3 bg-white/90 text-gray-800 text-xs font-semibold px-2 py-1 rounded"
      >
        {{ product.brand.name }}
      </span>
    </div>

    <!-- Info -->
    <div class="p-4">
      <!-- Category -->
      <p v-if="product.category" class="text-sm text-gray-500 mb-1">
        {{ product.category.name }}
      </p>

      <!-- Name -->
      <h3 class="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2 mb-2">
        {{ product.name }}
      </h3>

      <!-- Specs -->
      <div v-if="product.vlt || product.uv_rejection || product.heat_rejection" class="flex flex-wrap gap-2 mb-3">
        <span v-if="product.vlt" class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
          VLT {{ product.vlt }}%
        </span>
        <span v-if="product.uv_rejection" class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
          UV {{ product.uv_rejection }}%
        </span>
        <span v-if="product.heat_rejection" class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
          Nhiệt {{ product.heat_rejection }}%
        </span>
      </div>

      <!-- Price -->
      <div class="flex items-center justify-between gap-3">
        <span v-if="product.is_contact_price" class="text-primary-600 font-semibold">
          Liên hệ
        </span>
        <span v-else class="text-primary-600 font-semibold line-clamp-1">
          {{ primaryPrice }}
        </span>

        <span class="text-sm text-gray-400 group-hover:text-primary-600 transition-colors whitespace-nowrap">
          Xem chi tiết →
        </span>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { Product } from '~/types'

const props = defineProps<{
  product: Product
}>()

const primaryPrice = computed(() => props.product.price_sedan || props.product.price_suv || 'Liên hệ')
</script>

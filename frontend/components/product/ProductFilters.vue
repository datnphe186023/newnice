<template>
  <div class="card p-6 sticky top-24">
    <div class="flex items-center justify-between mb-5">
      <h3 class="font-semibold text-lg">Bộ lọc</h3>
      <button
        v-if="hasActiveFilters"
        @click="clearAll"
        class="text-xs text-red-500 hover:text-red-600 font-medium flex items-center gap-1"
      >
        <XMarkIcon class="w-3.5 h-3.5" />
        Xóa tất cả
      </button>
    </div>

    <!-- Search -->
    <div class="mb-6">
      <label class="label">Tìm kiếm</label>
      <div class="relative">
        <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          v-model="localSearch"
          type="text"
          placeholder="Tên sản phẩm..."
          class="input pl-9 text-sm"
          @keydown.enter="emit('update:search', localSearch)"
        />
      </div>
    </div>

    <!-- Categories -->
    <div v-if="categories?.length" class="mb-6">
      <h4 class="font-medium text-sm text-gray-700 mb-3">Danh mục</h4>
      <ul class="space-y-1.5">
        <li v-for="cat in categories" :key="cat.slug">
          <button
            @click="toggleCategory(cat.slug)"
            class="text-sm w-full text-left py-1.5 px-2 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-between group"
            :class="isSelectedCategory(cat.slug) ? 'text-primary-600 font-medium bg-primary-50' : 'text-gray-600'"
          >
            <span>{{ cat.name }}</span>
            <CheckIcon
              v-if="isSelectedCategory(cat.slug)"
              class="w-4 h-4 text-primary-600 flex-shrink-0"
            />
          </button>
        </li>
      </ul>
    </div>

    <!-- Brands -->
    <div v-if="brands?.length" class="mb-6">
      <h4 class="font-medium text-sm text-gray-700 mb-3">Thương hiệu</h4>
      <ul class="space-y-1.5">
        <li v-for="brand in brands" :key="brand.slug">
          <button
            @click="toggleBrand(brand.slug)"
            class="text-sm w-full text-left py-1.5 px-2 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-between group"
            :class="isSelectedBrand(brand.slug) ? 'text-primary-600 font-medium bg-primary-50' : 'text-gray-600'"
          >
            <span>{{ brand.name }}</span>
            <CheckIcon
              v-if="isSelectedBrand(brand.slug)"
              class="w-4 h-4 text-primary-600 flex-shrink-0"
            />
          </button>
        </li>
      </ul>
    </div>

    <!-- Film type -->
    <div class="mb-6">
      <h4 class="font-medium text-sm text-gray-700 mb-3">Loại phim</h4>
      <ul class="space-y-1.5">
        <li v-for="type in filmTypes" :key="type.value">
          <button
            @click="toggleFilmType(type.value)"
            class="text-sm w-full text-left py-1.5 px-2 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-between"
            :class="isSelectedFilmType(type.value) ? 'text-primary-600 font-medium bg-primary-50' : 'text-gray-600'"
          >
            <span>{{ type.label }}</span>
            <CheckIcon v-if="isSelectedFilmType(type.value)" class="w-4 h-4 text-primary-600 flex-shrink-0" />
          </button>
        </li>
      </ul>
    </div>

    <!-- Apply on mobile -->
    <button class="btn-primary w-full lg:hidden" @click="emit('apply')">
      Áp dụng bộ lọc
    </button>
  </div>
</template>

<script setup lang="ts">
import { MagnifyingGlassIcon, XMarkIcon, CheckIcon } from '@heroicons/vue/24/outline'
import type { Category, Brand } from '~/types'

const props = defineProps<{
  categories?: Category[]
  brands?: Brand[]
  selectedCategory?: string
  selectedBrand?: string
  selectedFilmType?: string
  search?: string
}>()

const emit = defineEmits<{
  (e: 'update:selectedCategory', val: string): void
  (e: 'update:selectedBrand', val: string): void
  (e: 'update:selectedFilmType', val: string): void
  (e: 'update:search', val: string): void
  (e: 'apply'): void
}>()

const localSearch = ref(props.search || '')

watch(() => props.search, (val) => {
  localSearch.value = val || ''
})

watch(localSearch, (val) => {
  // debounce: emit after 400ms
  clearTimeout((window as unknown as Record<string, unknown>).__searchTimeout as ReturnType<typeof setTimeout>)
  ;(window as unknown as Record<string, unknown>).__searchTimeout = setTimeout(() => {
    emit('update:search', val)
  }, 400)
})

const filmTypes = [
  { value: 'ceramic', label: 'Phim Ceramic' },
  { value: 'carbon', label: 'Phim Carbon' },
  { value: 'metallic', label: 'Phim Metallic' },
  { value: 'nano', label: 'Phim Nano' },
  { value: 'hybrid', label: 'Phim Hybrid' },
]

const isSelectedCategory = (slug: string) => props.selectedCategory === slug
const isSelectedBrand = (slug: string) => props.selectedBrand === slug
const isSelectedFilmType = (val: string) => props.selectedFilmType === val

const toggleCategory = (slug: string) =>
  emit('update:selectedCategory', isSelectedCategory(slug) ? '' : slug)

const toggleBrand = (slug: string) =>
  emit('update:selectedBrand', isSelectedBrand(slug) ? '' : slug)

const toggleFilmType = (val: string) =>
  emit('update:selectedFilmType', isSelectedFilmType(val) ? '' : val)

const hasActiveFilters = computed(() =>
  !!(props.selectedCategory || props.selectedBrand || props.selectedFilmType || props.search)
)

const clearAll = () => {
  emit('update:selectedCategory', '')
  emit('update:selectedBrand', '')
  emit('update:selectedFilmType', '')
  emit('update:search', '')
  localSearch.value = ''
}
</script>

<template>
  <div>
    <!-- Main image -->
    <div class="card overflow-hidden mb-3 cursor-zoom-in" @click="openLightbox(activeIndex)">
      <div class="relative aspect-square overflow-hidden bg-gray-100">
        <img
          :src="currentImage?.image_url || thumbnail || '/images/placeholder.jpg'"
          :alt="alt"
          class="w-full h-full object-cover transition-opacity duration-300"
          :class="{ 'opacity-0': transitioning }"
        />
        <!-- Zoom icon hint -->
        <div class="absolute top-3 right-3 bg-white/80 rounded-full p-1.5 opacity-0 group-hover:opacity-100 pointer-events-none">
          <MagnifyingGlassPlusIcon class="w-4 h-4 text-gray-500" />
        </div>
        <!-- Nav arrows if multiple images -->
        <template v-if="allImages.length > 1">
          <button
            class="absolute left-2 top-1/2 -translate-y-1/2 w-9 h-9 bg-white/80 hover:bg-white rounded-full flex items-center justify-center shadow transition-colors"
            @click.stop="prev"
          >
            <ChevronLeftIcon class="w-5 h-5 text-gray-700" />
          </button>
          <button
            class="absolute right-2 top-1/2 -translate-y-1/2 w-9 h-9 bg-white/80 hover:bg-white rounded-full flex items-center justify-center shadow transition-colors"
            @click.stop="next"
          >
            <ChevronRightIcon class="w-5 h-5 text-gray-700" />
          </button>
        </template>
      </div>
    </div>

    <!-- Thumbnails -->
    <div v-if="allImages.length > 1" class="grid grid-cols-5 gap-2">
      <button
        v-for="(img, i) in allImages"
        :key="i"
        @click="setActive(i)"
        class="aspect-square rounded-lg overflow-hidden border-2 transition-all"
        :class="activeIndex === i ? 'border-primary-600 ring-2 ring-primary-200' : 'border-transparent hover:border-gray-300'"
      >
        <img
          :src="img.image_url"
          :alt="`${alt} - ảnh ${i + 1}`"
          class="w-full h-full object-cover"
          loading="lazy"
        />
      </button>
    </div>

    <!-- Lightbox overlay -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="lightboxOpen"
          class="fixed inset-0 z-50 bg-black/90 flex items-center justify-center"
          @click.self="lightboxOpen = false"
          @keydown.escape="lightboxOpen = false"
          tabindex="0"
        >
          <!-- Close button -->
          <button
            class="absolute top-4 right-4 text-white/80 hover:text-white transition-colors"
            @click="lightboxOpen = false"
          >
            <XMarkIcon class="w-8 h-8" />
          </button>

          <!-- Counter -->
          <span class="absolute top-4 left-1/2 -translate-x-1/2 text-white/60 text-sm">
            {{ lightboxIndex + 1 }} / {{ allImages.length }}
          </span>

          <!-- Image -->
          <img
            :src="allImages[lightboxIndex]?.image_url"
            :alt="alt"
            class="max-h-[90vh] max-w-[90vw] object-contain rounded-lg select-none"
          />

          <!-- Prev / Next -->
          <button
            v-if="allImages.length > 1"
            class="absolute left-4 top-1/2 -translate-y-1/2 text-white/80 hover:text-white"
            @click="lightboxIndex = (lightboxIndex - 1 + allImages.length) % allImages.length"
          >
            <ChevronLeftIcon class="w-10 h-10" />
          </button>
          <button
            v-if="allImages.length > 1"
            class="absolute right-4 top-1/2 -translate-y-1/2 text-white/80 hover:text-white"
            @click="lightboxIndex = (lightboxIndex + 1) % allImages.length"
          >
            <ChevronRightIcon class="w-10 h-10" />
          </button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  XMarkIcon,
  MagnifyingGlassPlusIcon,
} from '@heroicons/vue/24/outline'
import type { ProductImage } from '~/types'

interface ImageItem {
  image_url: string
}

const props = defineProps<{
  thumbnail?: string
  images?: ProductImage[]
  alt?: string
}>()

// Merge thumbnail + extra images into one array
const allImages = computed<ImageItem[]>(() => {
  const imgs: ImageItem[] = []
  if (props.thumbnail) imgs.push({ image_url: props.thumbnail })
  if (props.images?.length) {
    props.images.forEach((img) => imgs.push({ image_url: img.image_url }))
  }
  return imgs
})

const activeIndex = ref(0)
const transitioning = ref(false)
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

const currentImage = computed(() => allImages.value[activeIndex.value])

watch(allImages, () => {
  activeIndex.value = 0
})

const setActive = (i: number) => {
  if (i === activeIndex.value) return
  transitioning.value = true
  setTimeout(() => {
    activeIndex.value = i
    transitioning.value = false
  }, 150)
}

const prev = () => setActive((activeIndex.value - 1 + allImages.value.length) % allImages.value.length)
const next = () => setActive((activeIndex.value + 1) % allImages.value.length)

const openLightbox = (index: number) => {
  lightboxIndex.value = index
  lightboxOpen.value = true
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

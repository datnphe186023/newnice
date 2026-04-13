<template>
  <picture>
    <source v-if="srcset" type="image/webp" :srcset="srcset" :sizes="sizes" />
    <img
      :src="src"
      :alt="alt"
      :loading="loading"
      :class="imgClass"
      :width="width"
      :height="height"
    />
  </picture>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  src: string
  alt: string
  srcset?: string
  sizes?: string
  loading?: 'lazy' | 'eager'
  imgClass?: string
  width?: number
  height?: number
}>(), {
  srcset: '',
  sizes: '100vw',
  loading: 'lazy',
  imgClass: '',
})
</script>

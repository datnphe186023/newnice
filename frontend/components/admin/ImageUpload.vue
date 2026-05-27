<template>
  <div class="image-upload">
    <!-- Preview area -->
    <div 
      v-if="previewUrl"
      class="relative mb-4"
    >
      <img 
        :src="previewUrl" 
        :alt="alt || 'Preview'"
        class="max-w-full h-auto rounded-lg border border-gray-200"
        :class="previewClass"
      />
      <button
        type="button"
        @click="removeImage"
        class="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
        :disabled="uploading"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>

    <!-- Drop zone -->
    <div
      v-else
      @click="openFilePicker"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      class="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors"
      :class="[
        isDragging 
          ? 'border-blue-500 bg-blue-50' 
          : 'border-gray-300 hover:border-gray-400 bg-gray-50'
      ]"
    >
      <svg 
        class="mx-auto h-12 w-12 text-gray-400" 
        stroke="currentColor" 
        fill="none" 
        viewBox="0 0 48 48"
      >
        <path 
          d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" 
          stroke-width="2" 
          stroke-linecap="round" 
          stroke-linejoin="round" 
        />
      </svg>
      <p class="mt-2 text-sm text-gray-600">
        <span class="font-medium text-blue-600">Click to upload</span>
        or drag and drop
      </p>
      <p class="mt-1 text-xs text-gray-500">
        {{ acceptText }}
      </p>
    </div>

    <!-- Hidden file input -->
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      class="hidden"
      @change="onFileSelected"
    />

    <!-- Upload progress -->
    <div v-if="uploading" class="mt-4">
      <div class="flex items-center justify-between mb-1">
        <span class="text-sm text-gray-600">Uploading...</span>
        <span class="text-sm text-gray-600">{{ uploadProgress }}%</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-blue-600 h-2 rounded-full transition-all duration-300" 
          :style="{ width: `${uploadProgress}%` }"
        />
      </div>
    </div>

    <!-- Error message -->
    <p v-if="error" class="mt-2 text-sm text-red-600">
      {{ error }}
    </p>

    <!-- Optimization stats -->
    <div
      v-if="uploadStats"
      class="mt-3 flex items-center gap-2 text-sm bg-green-50 border border-green-200 rounded-lg px-3 py-2"
    >
      <svg class="w-4 h-4 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
      <span class="text-green-800">
        Tối ưu: {{ (uploadStats.original_size_bytes / 1024 / 1024).toFixed(2) }} MB
        → {{ (uploadStats.webp_size_bytes / 1024).toFixed(0) }} KB
        <strong>(giảm {{ Math.round((1 - uploadStats.webp_size_bytes / uploadStats.original_size_bytes) * 100) }}%)</strong>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'

interface ImageData {
  original: string
  webp?: string
  thumb?: string
  small?: string
  medium?: string
  large?: string
  xlarge?: string
  srcset?: string
  sizes?: string
  filename?: string
  original_size_bytes?: number
  webp_size_bytes?: number
}

const props = withDefaults(defineProps<{
  modelValue?: string | null
  subfolder?: string
  isBanner?: boolean
  generateVariants?: boolean
  accept?: string
  maxSize?: number // in MB
  alt?: string
  previewClass?: string
}>(), {
  modelValue: null,
  subfolder: 'images',
  isBanner: false,
  generateVariants: true,
  accept: 'image/jpeg,image/png,image/webp,image/gif',
  maxSize: 10,
  alt: '',
  previewClass: 'max-h-48 object-cover',
})

const emit = defineEmits<{
  'update:modelValue': [value: string | null]
  'uploaded': [data: ImageData]
  'removed': []
  'error': [message: string]
}>()

const config = useRuntimeConfig()
const authStore = useAuthStore()

const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const error = ref<string | null>(null)
const uploadStats = ref<{ original_size_bytes: number; webp_size_bytes: number } | null>(null)

const acceptText = computed(() => {
  const types = props.accept.split(',').map(t => t.split('/')[1]?.toUpperCase()).filter(Boolean)
  return `${types.join(', ')} up to ${props.maxSize}MB`
})

const previewUrl = computed(() => {
  if (!props.modelValue) return null
  // If it's already a full URL, use it
  if (props.modelValue.startsWith('http')) return props.modelValue
  // Otherwise, prepend the API base URL
  const apiBase = config.public.apiBase || 'http://localhost:8000'
  return `${apiBase}${props.modelValue}`
})

function openFilePicker() {
  fileInput.value?.click()
}

function onDragOver() {
  isDragging.value = true
}

function onDragLeave() {
  isDragging.value = false
}

function onDrop(event: DragEvent) {
  isDragging.value = false
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    handleFile(files[0])
  }
}

function onFileSelected(event: Event) {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files && files.length > 0) {
    handleFile(files[0])
  }
  // Reset input so same file can be selected again
  target.value = ''
}

async function handleFile(file: File) {
  error.value = null

  // Validate file type
  if (!props.accept.includes(file.type)) {
    error.value = `Invalid file type. Allowed: ${acceptText.value}`
    emit('error', error.value)
    return
  }

  // Validate file size
  const maxBytes = props.maxSize * 1024 * 1024
  if (file.size > maxBytes) {
    error.value = `File too large. Maximum size: ${props.maxSize}MB`
    emit('error', error.value)
    return
  }

  // Upload file
  await uploadFile(file)
}

async function uploadFile(file: File) {
  uploading.value = true
  uploadProgress.value = 0
  error.value = null

  const formData = new FormData()
  formData.append('file', file)
  formData.append('subfolder', props.subfolder)
  formData.append('generate_variants', String(props.generateVariants))
  formData.append('is_banner', String(props.isBanner))

  try {
    const apiBase = config.public.apiBase || 'http://localhost:8000'
    
    const response = await fetch(`${apiBase}/admin/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
      body: formData,
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.detail || 'Upload failed')
    }

    const result = await response.json()
    
    if (result.success && result.data) {
      const imageData = result.data as ImageData
      // Use WebP version if available, otherwise original
      const imageUrl = imageData.webp || imageData.original
      emit('update:modelValue', imageUrl)
      emit('uploaded', imageData)
      // Show optimization stats if available
      if (imageData.original_size_bytes != null && imageData.webp_size_bytes != null) {
        uploadStats.value = {
          original_size_bytes: imageData.original_size_bytes,
          webp_size_bytes: imageData.webp_size_bytes,
        }
      }
    } else {
      throw new Error('Invalid response from server')
    }

    uploadProgress.value = 100
  } catch (e: any) {
    error.value = e.message || 'Upload failed'
    emit('error', error.value)
  } finally {
    uploading.value = false
  }
}

async function removeImage() {
  if (!props.modelValue) return

  error.value = null

  try {
    const apiBase = config.public.apiBase || 'http://localhost:8000'
    
    const response = await fetch(`${apiBase}/admin/upload?image_url=${encodeURIComponent(props.modelValue)}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
    })

    // Even if delete fails on server, clear the local value
    emit('update:modelValue', null)
    emit('removed')
    uploadStats.value = null
  } catch (e: any) {
    // Still clear local value
    emit('update:modelValue', null)
    emit('removed')
    uploadStats.value = null
  }
}

// Simulate upload progress (since fetch doesn't support progress natively)
watch(uploading, (isUploading) => {
  if (isUploading) {
    const interval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10
      }
    }, 100)
    
    setTimeout(() => clearInterval(interval), 1000)
  }
})
</script>

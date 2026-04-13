<template>
  <Teleport to="body">
    <Transition name="slide">
      <div 
        v-if="isOpen" 
        class="fixed inset-0 z-50 md:hidden"
      >
        <!-- Backdrop -->
        <div 
          class="absolute inset-0 bg-black/50"
          @click="$emit('close')"
        />
        
        <!-- Menu panel -->
        <div class="absolute left-0 top-0 bottom-0 w-80 max-w-[85vw] bg-white shadow-xl">
          <div class="flex flex-col h-full">
            <!-- Header -->
            <div class="flex items-center justify-between p-4 border-b">
              <NuxtLink to="/" class="text-xl font-bold text-primary-600" @click="$emit('close')">
                Auto<span class="text-accent">Film</span>
              </NuxtLink>
              <button @click="$emit('close')" class="p-2">
                <XMarkIcon class="w-6 h-6" />
              </button>
            </div>
            
            <!-- Search -->
            <div class="p-4 border-b">
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Tìm kiếm..."
                  class="input pr-10"
                  @keyup.enter="handleSearch"
                />
                <button 
                  class="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-500"
                  @click="handleSearch"
                >
                  <MagnifyingGlassIcon class="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <!-- Menu items -->
            <nav class="flex-1 overflow-y-auto py-4">
              <ul>
                <li v-for="item in menuItems" :key="item.href">
                  <NuxtLink 
                    :to="item.href"
                    class="block px-6 py-3 text-gray-800 hover:bg-gray-100 transition-colors"
                    @click="$emit('close')"
                  >
                    {{ item.label }}
                  </NuxtLink>
                </li>
              </ul>
            </nav>
            
            <!-- Footer -->
            <div class="p-4 border-t bg-gray-50">
              <a 
                href="tel:0869418104" 
                class="btn-primary w-full mb-3"
              >
                <PhoneIcon class="w-5 h-5 mr-2" />
                Gọi ngay: 0869 418 104
              </a>
              <NuxtLink 
                to="/bao-gia" 
                class="btn-accent w-full"
                @click="$emit('close')"
              >
                Báo giá nhanh
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { XMarkIcon, MagnifyingGlassIcon, PhoneIcon } from '@heroicons/vue/24/outline'

interface MenuItem {
  label: string
  href: string
}

const props = defineProps<{
  isOpen: boolean
  menuItems: MenuItem[]
}>()

const emit = defineEmits<{
  close: []
}>()

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/san-pham?search=${encodeURIComponent(searchQuery.value)}`)
    emit('close')
  }
}
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
}

.slide-enter-from > div:last-child,
.slide-leave-to > div:last-child {
  transform: translateX(-100%);
}
</style>

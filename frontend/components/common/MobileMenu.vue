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
              <NuxtLink to="/" class="flex items-center gap-0.5" @click="$emit('close')">
                <span class="text-xl font-black tracking-tight text-gray-900 uppercase">New</span>
                <span class="text-xl font-black tracking-tight text-primary-600 uppercase">Nice</span>
              </NuxtLink>
              <button class="p-2" @click="$emit('close')">
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
                <li v-for="item in leadingMenuItems" :key="item.href">
                  <NuxtLink
                    :to="item.href"
                    class="block px-6 py-3 text-gray-800 hover:bg-gray-100 transition-colors"
                    @click="$emit('close')"
                  >
                    {{ item.label }}
                  </NuxtLink>
                </li>

                <li>
                  <button
                    type="button"
                    class="flex w-full items-center justify-between px-6 py-3 text-left text-gray-800 hover:bg-gray-100 transition-colors"
                    @click="isCategoryMenuOpen = !isCategoryMenuOpen"
                  >
                    <span>Danh mục</span>
                    <ChevronDownIcon
                      class="h-5 w-5 transition-transform"
                      :class="{ 'rotate-180': isCategoryMenuOpen }"
                    />
                  </button>
                  <ul v-show="isCategoryMenuOpen" class="bg-gray-50 py-1">
                    <li v-for="category in categoryItems" :key="category.href">
                      <NuxtLink
                        :to="category.href"
                        class="block px-10 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-primary-600"
                        @click="$emit('close')"
                      >
                        {{ category.label }}
                      </NuxtLink>
                    </li>
                    <li v-if="!categoryItems.length" class="px-10 py-2.5 text-sm text-gray-500">
                      Chưa có danh mục
                    </li>
                  </ul>
                </li>

                <li v-for="item in trailingMenuItems" :key="item.href">
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
import {
  XMarkIcon,
  MagnifyingGlassIcon,
  PhoneIcon,
  ChevronDownIcon,
} from '@heroicons/vue/24/outline'

interface MenuItem {
  label: string
  href: string
}

const props = withDefaults(defineProps<{
  isOpen: boolean
  menuItems: MenuItem[]
  categoryItems?: MenuItem[]
}>(), {
  categoryItems: () => [],
})

const emit = defineEmits<{
  close: []
}>()

const router = useRouter()
const searchQuery = ref('')
const isCategoryMenuOpen = ref(false)

const leadingMenuItems = computed(() => props.menuItems.slice(0, 1))
const trailingMenuItems = computed(() => props.menuItems.slice(1))

watch(() => props.isOpen, (isOpen) => {
  if (!isOpen) {
    isCategoryMenuOpen.value = false
  }
})

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

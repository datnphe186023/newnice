<template>
  <div class="fixed bottom-4 right-4 z-40 flex flex-col gap-3">
    <!-- Zalo -->
    <a
      href="https://zalo.me/0901234567"
      target="_blank"
      class="group relative w-14 h-14 bg-blue-500 rounded-full flex items-center justify-center shadow-lg hover:scale-110 transition-transform"
    >
      <span class="font-bold text-white text-sm">Zalo</span>
      <span class="absolute right-full mr-3 px-3 py-1 bg-gray-800 text-white text-sm rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
        Chat Zalo
      </span>
    </a>

    <!-- Messenger -->
    <a
      href="https://m.me/newnice"
      target="_blank"
      class="group relative w-14 h-14 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg hover:scale-110 transition-transform"
    >
      <svg class="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12,2C6.36,2,2,6.13,2,11.7c0,2.91,1.19,5.44,3.14,7.17.16.13.26.35.27.57l.05,1.78c.04.57.61.94,1.13.71l1.98-.87c.17-.08.36-.09.53-.05.91.25,1.87.39,2.9.39,5.64,0,10-4.13,10-9.7S17.64,2,12,2Zm6.12,7.64-2.88,4.89c-.46.78-1.47.97-2.15.4l-2.29-1.84c-.18-.14-.43-.14-.61,0l-3.1,2.5c-.41.33-.95-.21-.68-.68l2.88-4.89c.46-.78,1.47-.97,2.15-.4l2.29,1.84c.18.14.43.14.61,0l3.1-2.5c.41-.33.95.21.68.68Z"/>
      </svg>
      <span class="absolute right-full mr-3 px-3 py-1 bg-gray-800 text-white text-sm rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
        Messenger
      </span>
    </a>

    <!-- Phone -->
    <a
      href="tel:0901234567"
      class="group relative w-14 h-14 bg-green-500 rounded-full flex items-center justify-center shadow-lg hover:scale-110 transition-transform animate-pulse"
    >
      <PhoneIcon class="w-7 h-7 text-white" />
      <span class="absolute right-full mr-3 px-3 py-1 bg-gray-800 text-white text-sm rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
        Gọi ngay
      </span>
    </a>
  </div>
</template>

<script setup lang="ts">
import { PhoneIcon } from '@heroicons/vue/24/solid'
</script>

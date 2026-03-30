<template>
  <div class="min-h-screen flex flex-col">
    <CommonHeader />
    
    <main class="flex-1">
      <slot />
    </main>
    
    <CommonFooter />
    
    <CommonFloatingButtons />
  </div>
</template>

<script setup lang="ts">
// Default layout with header, footer, and floating buttons
</script>

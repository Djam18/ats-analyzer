<script setup lang="ts">
defineProps<{
  size?: 'sm' | 'md' | 'lg'
  variant?: 'dark' | 'light'
}>()
</script>

<template>
  <NuxtLink to="/" class="flex items-center gap-2 no-underline">
    <div
      :class="[
        'flex items-center justify-center rounded-lg font-bold text-white bg-[#1E3A5F] flex-shrink-0',
        size === 'sm' ? 'w-7 h-7 text-sm' : size === 'lg' ? 'w-10 h-10 text-lg' : 'w-8 h-8 text-base',
      ]"
    >
      A
    </div>
    <div class="flex flex-col leading-none">
      <span
        :class="[
          'font-bold tracking-tight',
          variant === 'light' ? 'text-white' : 'text-[#1E3A5F]',
          size === 'sm' ? 'text-sm' : size === 'lg' ? 'text-xl' : 'text-base',
        ]"
      >
        ATS Platform
      </span>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
defineProps<{
  icon?: string
  title: string
  description?: string
  actionLabel?: string
  actionTo?: string
  actionClick?: () => void
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 text-center px-4">
    <div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
      <UIcon :name="icon ?? 'i-lucide-inbox'" class="w-8 h-8 text-gray-400" />
    </div>
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
      {{ title }}
    </h3>
    <p v-if="description" class="text-sm text-gray-500 dark:text-gray-400 max-w-sm mb-6">
      {{ description }}
    </p>
    <UButton
      v-if="actionLabel && actionTo"
      :to="actionTo"
      icon="i-lucide-plus"
    >
      {{ actionLabel }}
    </UButton>
    <UButton
      v-else-if="actionLabel && actionClick"
      icon="i-lucide-plus"
      @click="actionClick"
    >
      {{ actionLabel }}
    </UButton>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description?: string
  confirmLabel?: string
  loading?: boolean
}>()

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()
</script>

<template>
  <UModal>
    <template #header>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        {{ title }}
      </h3>
    </template>

    <p v-if="description" class="text-sm text-gray-500 dark:text-gray-400">
      {{ description }}
    </p>

    <slot />

    <template #footer>
      <div class="flex justify-end gap-3">
        <UButton variant="ghost" color="neutral" @click="emit('cancel')">
          Annuler
        </UButton>
        <UButton color="error" :loading="loading" @click="emit('confirm')">
          {{ confirmLabel ?? 'Confirmer' }}
        </UButton>
      </div>
    </template>
  </UModal>
</template>

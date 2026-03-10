<script setup lang="ts">
import type { CV } from '~/composables/useCV'

const props = defineProps<{
  cvs: CV[]
  selectedId?: string | null
  loading?: boolean
}>()

const emit = defineEmits<{
  select: [id: string]
  delete: [id: string]
  rename: [id: string, name: string]
  upload: []
}>()
</script>

<template>
  <div>
    <div v-if="loading" class="space-y-3">
      <div
        v-for="i in 3"
        :key="i"
        class="h-20 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse"
      />
    </div>

    <SharedEmptyState
      v-else-if="cvs.length === 0"
      icon="i-lucide-file-text"
      title="Aucun CV uploadé"
      description="Uploadez votre premier CV pour commencer à analyser votre compatibilité avec des offres d'emploi."
      action-label="Uploader un CV"
      @action-click="emit('upload')"
    />

    <div v-else class="space-y-3">
      <CvCard
        v-for="cv in cvs"
        :key="cv.id"
        :cv="cv"
        :selected="cv.id === selectedId"
        @select="emit('select', $event)"
        @delete="emit('delete', $event)"
        @rename="emit('rename', $event, $event)"
      />
    </div>
  </div>
</template>

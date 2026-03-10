<script setup lang="ts">
import type { CV } from '~/composables/useCV'

const props = defineProps<{
  cv: CV
  selected?: boolean
}>()

const emit = defineEmits<{
  select: [id: string]
  delete: [id: string]
  rename: [id: string, name: string]
}>()

const { formatFileSize, renameCV } = useCV()

const isEditing = ref(false)
const editName = ref(props.cv.display_name)

async function handleRename() {
  if (!editName.value.trim()) {
    editName.value = props.cv.display_name
    isEditing.value = false
    return
  }
  const ok = await renameCV(props.cv.id, editName.value.trim())
  if (ok) emit('rename', props.cv.id, editName.value.trim())
  isEditing.value = false
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter') handleRename()
  if (e.key === 'Escape') {
    editName.value = props.cv.display_name
    isEditing.value = false
  }
}

const fileIcon = computed(() =>
  props.cv.file_type === 'pdf' ? 'i-lucide-file-text' : 'i-lucide-file'
)

const formattedDate = computed(() =>
  new Date(props.cv.created_at).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
)
</script>

<template>
  <div
    class="border rounded-xl p-4 transition-all duration-200 cursor-pointer"
    :class="selected
      ? 'border-primary bg-primary-50 dark:bg-primary-950'
      : 'border-gray-200 dark:border-gray-700 hover:border-primary hover:shadow-sm'"
    @click="emit('select', cv.id)"
  >
    <div class="flex items-start gap-3">
      <!-- File icon -->
      <div
        class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
        :class="cv.file_type === 'pdf' ? 'bg-red-100 dark:bg-red-950' : 'bg-blue-100 dark:bg-blue-950'"
      >
        <UIcon
          :name="fileIcon"
          class="w-5 h-5"
          :class="cv.file_type === 'pdf' ? 'text-red-600' : 'text-blue-600'"
        />
      </div>

      <!-- Info -->
      <div class="flex-1 min-w-0">
        <!-- Inline rename -->
        <div v-if="isEditing" @click.stop>
          <input
            v-model="editName"
            class="w-full text-sm font-medium border-b border-primary bg-transparent outline-none pb-1"
            maxlength="100"
            autofocus
            @blur="handleRename"
            @keydown="handleKeydown"
          >
        </div>
        <p
          v-else
          class="text-sm font-medium text-gray-900 dark:text-white truncate"
          :title="cv.display_name"
        >
          {{ cv.display_name }}
        </p>

        <div class="flex items-center gap-2 mt-1 flex-wrap">
          <span class="text-xs text-gray-400 uppercase font-medium">{{ cv.file_type }}</span>
          <span class="text-xs text-gray-300">·</span>
          <span class="text-xs text-gray-400">{{ formatFileSize(cv.file_size) }}</span>
          <span v-if="cv.page_count" class="text-xs text-gray-300">·</span>
          <span v-if="cv.page_count" class="text-xs text-gray-400">{{ cv.page_count }} p.</span>
          <span v-if="cv.is_scanned" class="text-xs text-orange-500 font-medium">⚠ Scanné</span>
        </div>
        <p class="text-xs text-gray-400 mt-1">
          {{ formattedDate }}
        </p>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-1 flex-shrink-0" @click.stop>
        <UButton
          variant="ghost"
          color="neutral"
          size="xs"
          icon="i-lucide-pencil"
          :title="'Renommer'"
          @click="isEditing = true"
        />
        <UButton
          variant="ghost"
          color="error"
          size="xs"
          icon="i-lucide-trash-2"
          :title="'Supprimer'"
          @click="emit('delete', cv.id)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{ uploaded: [cvId: string] }>()

const { uploadCV, uploading, uploadProgress } = useCV()
const toast = useToast()

const dragOver = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

async function handleFile(file: File) {
  const result = await uploadCV(file)
  if (result) {
    emit('uploaded', result.id)
  }
}

function onDrop(e: DragEvent) {
  dragOver.value = false
  const file = e.dataTransfer?.files[0]
  if (file) handleFile(file)
}

function onFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) handleFile(file)
}
</script>

<template>
  <div>
    <div
      class="border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200"
      :class="dragOver
        ? 'border-primary bg-primary-50 dark:bg-primary-950 scale-[1.01]'
        : 'border-gray-300 dark:border-gray-700 hover:border-primary hover:bg-gray-50 dark:hover:bg-gray-800'"
      @dragover.prevent="dragOver = true"
      @dragleave="dragOver = false"
      @drop.prevent="onDrop"
      @click="!uploading && fileInput?.click()"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".pdf,.docx"
        class="hidden"
        @change="onFileChange"
      >

      <div v-if="!uploading">
        <UIcon
          name="i-lucide-upload-cloud"
          class="w-12 h-12 mx-auto mb-3 transition-colors"
          :class="dragOver ? 'text-primary' : 'text-gray-400'"
        />
        <p class="font-medium text-gray-700 dark:text-gray-300 mb-1">
          Glissez votre CV ici ou <span class="text-primary">cliquez pour parcourir</span>
        </p>
        <p class="text-sm text-gray-400">
          PDF ou DOCX — max 5 Mo, 10 pages
        </p>
      </div>

      <div v-else class="py-4">
        <UIcon name="i-lucide-loader-2" class="w-10 h-10 animate-spin text-primary mx-auto mb-3" />
        <p class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-3">
          Extraction du texte en cours...
        </p>
        <div class="w-full max-w-xs mx-auto bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            class="bg-primary h-2 rounded-full transition-all duration-300"
            :style="{ width: `${uploadProgress || 10}%` }"
          />
        </div>
        <p class="text-xs text-gray-400 mt-2">
          {{ uploadProgress }}%
        </p>
      </div>
    </div>
  </div>
</template>

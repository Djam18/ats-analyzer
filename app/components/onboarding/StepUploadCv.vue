<script setup lang="ts">
const emit = defineEmits<{ uploaded: [cvId: string] }>()

const toast = useToast()
const loading = ref(false)
const dragOver = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

async function handleFile(file: File) {
  const allowed = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  if (!allowed.includes(file.type)) {
    toast.add({ title: 'Format non supporté', description: 'Uploadez un fichier PDF ou DOCX.', color: 'error' })
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    toast.add({ title: 'Fichier trop volumineux', description: 'La taille maximale est de 5 Mo.', color: 'error' })
    return
  }

  loading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)

    const data = await $fetch<{ id: string }>('/api/cv/upload', {
      method: 'POST',
      body: formData
    })
    toast.add({ title: 'CV uploadé avec succès !', color: 'success' })
    emit('uploaded', data.id)
  }
  catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur lors de l\'upload'
    toast.add({ title: 'Upload échoué', description: message, color: 'error' })
  }
  finally {
    loading.value = false
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
  <div class="py-4">
    <div class="text-center mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
        Uploadez votre CV
      </h2>
      <p class="text-gray-500 dark:text-gray-400 text-sm">
        Format PDF ou DOCX, maximum 5 Mo
      </p>
    </div>

    <div
      class="border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors"
      :class="dragOver
        ? 'border-primary bg-primary-50 dark:bg-primary-950'
        : 'border-gray-300 dark:border-gray-700 hover:border-primary'"
      @dragover.prevent="dragOver = true"
      @dragleave="dragOver = false"
      @drop.prevent="onDrop"
      @click="fileInput?.click()"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".pdf,.docx"
        class="hidden"
        @change="onFileChange"
      >
      <UIcon
        name="i-lucide-upload-cloud"
        class="w-12 h-12 mx-auto mb-4"
        :class="dragOver ? 'text-primary' : 'text-gray-400'"
      />
      <p class="font-medium text-gray-700 dark:text-gray-300 mb-1">
        Glissez votre CV ici ou cliquez pour parcourir
      </p>
      <p class="text-sm text-gray-400">
        PDF, DOCX — max 5 Mo
      </p>
    </div>

    <div v-if="loading" class="mt-6 flex items-center justify-center gap-3 text-primary">
      <UIcon name="i-lucide-loader-2" class="w-5 h-5 animate-spin" />
      <span class="text-sm font-medium">Extraction du texte en cours...</span>
    </div>
  </div>
</template>

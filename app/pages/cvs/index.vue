<script setup lang="ts">
import type { CV } from '~/composables/useCV'

definePageMeta({
  middleware: ['auth', 'onboarding']
})

const { fetchCVs, deleteCV } = useCV()

const cvs = ref<CV[]>([])
const loading = ref(true)
const showUploader = ref(false)
const deleteTarget = ref<string | null>(null)
const showDeleteModal = ref(false)
const deleting = ref(false)

onMounted(async () => {
  cvs.value = await fetchCVs()
  loading.value = false
})

async function handleUploaded(cvId: string) {
  showUploader.value = false
  cvs.value = await fetchCVs()
}

async function handleDelete(id: string) {
  deleteTarget.value = id
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  const ok = await deleteCV(deleteTarget.value)
  if (ok) {
    cvs.value = cvs.value.filter(cv => cv.id !== deleteTarget.value)
  }
  deleteTarget.value = null
  showDeleteModal.value = false
  deleting.value = false
}

function handleRename(id: string, newName: string) {
  const cv = cvs.value.find(c => c.id === id)
  if (cv) cv.display_name = newName
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          Mes CV
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          {{ cvs.length }} CV{{ cvs.length > 1 ? 's' : '' }} uploadé{{ cvs.length > 1 ? 's' : '' }}
        </p>
      </div>
      <UButton icon="i-lucide-upload" @click="showUploader = !showUploader">
        Uploader un CV
      </UButton>
    </div>

    <!-- Uploader panel -->
    <div v-if="showUploader" class="mb-6">
      <UCard>
        <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">
          Uploader un nouveau CV
        </h2>
        <CvUploader @uploaded="handleUploaded" />
      </UCard>
    </div>

    <!-- CV list -->
    <CvList
      :cvs="cvs"
      :loading="loading"
      @delete="handleDelete"
      @rename="handleRename"
      @upload="showUploader = true"
    />

    <!-- Delete confirmation dialog -->
    <UModal v-model:open="showDeleteModal">
      <template #content>
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Supprimer ce CV ?
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
            Le fichier sera définitivement supprimé. Vos analyses associées seront conservées.
          </p>
          <div class="flex justify-end gap-3">
            <UButton variant="ghost" color="neutral" @click="showDeleteModal = false; deleteTarget = null">
              Annuler
            </UButton>
            <UButton color="error" :loading="deleting" @click="confirmDelete">
              Supprimer
            </UButton>
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>

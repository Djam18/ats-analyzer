export interface CV {
  id: string
  display_name: string
  file_name: string
  file_type: 'pdf' | 'docx'
  file_size: number
  is_scanned: boolean
  page_count: number | null
  created_at: string
}

export const useCV = () => {
  const toast = useToast()
  const uploading = ref(false)
  const uploadProgress = ref(0)

  async function uploadCV(file: File): Promise<{ id: string, warning?: string | null } | null> {
    const ALLOWED = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if (!ALLOWED.includes(file.type)) {
      toast.add({ title: 'Format non supporté', description: 'Uploadez un fichier PDF ou DOCX.', color: 'error' })
      return null
    }
    if (file.size > 5 * 1024 * 1024) {
      toast.add({ title: 'Fichier trop volumineux', description: 'La taille maximale est de 5 Mo.', color: 'error' })
      return null
    }

    uploading.value = true
    uploadProgress.value = 0

    try {
      const formData = new FormData()
      formData.append('file', file)

      const data = await $fetch<{ id: string, warning?: string | null }>('/api/cv/upload', {
        method: 'POST',
        body: formData
      })

      if (data.warning) {
        toast.add({ title: 'Attention', description: data.warning, color: 'warning' })
      }
      else {
        toast.add({ title: 'CV uploadé avec succès', color: 'success' })
      }

      return data
    }
    catch (error: unknown) {
      const message = (error as { data?: { message?: string } })?.data?.message ?? 'Erreur lors de l\'upload'
      toast.add({ title: 'Upload échoué', description: message, color: 'error' })
      return null
    }
    finally {
      uploading.value = false
      uploadProgress.value = 0
    }
  }

  async function fetchCVs(): Promise<CV[]> {
    try {
      return await $fetch<CV[]>('/api/cv')
    }
    catch {
      toast.add({ title: 'Erreur', description: 'Impossible de charger vos CV.', color: 'error' })
      return []
    }
  }

  async function deleteCV(id: string): Promise<boolean> {
    try {
      await $fetch(`/api/cv/${id}`, { method: 'DELETE' })
      toast.add({ title: 'CV supprimé', color: 'success' })
      return true
    }
    catch {
      toast.add({ title: 'Erreur', description: 'Impossible de supprimer ce CV.', color: 'error' })
      return false
    }
  }

  async function renameCV(id: string, displayName: string): Promise<boolean> {
    try {
      await $fetch(`/api/cv/${id}`, {
        method: 'PATCH',
        body: { display_name: displayName }
      })
      return true
    }
    catch {
      toast.add({ title: 'Erreur', description: 'Impossible de renommer ce CV.', color: 'error' })
      return false
    }
  }

  function formatFileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} o`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} Ko`
    return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`
  }

  return {
    uploading,
    uploadProgress,
    uploadCV,
    fetchCVs,
    deleteCV,
    renameCV,
    formatFileSize
  }
}

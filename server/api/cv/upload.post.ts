import { serverSupabaseUser } from '#supabase/server'
import { extractTextFromFile } from '../../utils/extract-text'

const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5 MB
const MAX_PAGES = 10
const ALLOWED_MIME_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const formData = await readMultipartFormData(event)
  if (!formData || formData.length === 0) {
    throw createError({ statusCode: 400, message: 'Aucun fichier reçu' })
  }

  const filePart = formData.find(part => part.name === 'file')
  if (!filePart || !filePart.data || !filePart.filename) {
    throw createError({ statusCode: 400, message: 'Champ "file" manquant' })
  }

  const mimeType = filePart.type ?? ''
  if (!ALLOWED_MIME_TYPES.includes(mimeType)) {
    throw createError({
      statusCode: 422,
      message: 'Format non supporté. Uploadez un fichier PDF ou DOCX.'
    })
  }

  if (filePart.data.length > MAX_FILE_SIZE) {
    throw createError({
      statusCode: 422,
      message: 'Fichier trop volumineux. La taille maximale est de 5 Mo.'
    })
  }

  // Extract text
  let extractResult
  try {
    extractResult = await extractTextFromFile(filePart.data, mimeType)
  }
  catch (err: unknown) {
    throw createError({
      statusCode: 422,
      message: err instanceof Error ? err.message : 'Erreur lors de la lecture du fichier'
    })
  }

  if (extractResult.pageCount > MAX_PAGES) {
    throw createError({
      statusCode: 422,
      message: `Le CV ne doit pas dépasser ${MAX_PAGES} pages. Le vôtre en contient ${extractResult.pageCount}.`
    })
  }

  const config = useRuntimeConfig()
  const supabase = useServerSupabase()

  // Upload to Supabase Storage
  const fileExt = mimeType === 'application/pdf' ? 'pdf' : 'docx'
  const fileName = `${Date.now()}.${fileExt}`
  const filePath = `${user.id}/${fileName}`

  const { error: storageError } = await supabase.storage
    .from('cvs')
    .upload(filePath, filePart.data, {
      contentType: mimeType,
      upsert: false
    })

  if (storageError) {
    console.error('Storage upload error:', storageError)
    throw createError({ statusCode: 500, message: 'Erreur lors du stockage du fichier' })
  }

  // Save metadata to DB
  const displayName = filePart.filename.replace(/\.[^.]+$/, '')

  const { data: cv, error: dbError } = await supabase
    .from('cvs')
    .insert({
      user_id: user.id,
      file_name: filePart.filename,
      display_name: displayName,
      file_path: filePath,
      file_size: filePart.data.length,
      file_type: fileExt,
      extracted_text: extractResult.isScanned ? null : extractResult.text,
      is_scanned: extractResult.isScanned,
      page_count: extractResult.pageCount
    })
    .select('id, display_name, file_name, file_type, is_scanned, page_count, created_at')
    .single()

  if (dbError) {
    // Rollback storage upload
    await supabase.storage.from('cvs').remove([filePath])
    throw createError({ statusCode: 500, message: 'Erreur lors de la sauvegarde des métadonnées' })
  }

  return {
    ...cv,
    isScanned: extractResult.isScanned,
    warning: extractResult.isScanned
      ? 'Votre CV semble être une image scannée. L\'analyse sera limitée. Uploadez un PDF avec du texte sélectionnable pour de meilleurs résultats.'
      : null
  }
})

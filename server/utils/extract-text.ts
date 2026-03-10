import pdfParse from 'pdf-parse'
import mammoth from 'mammoth'

const MIN_CHARS_PER_PAGE = 50
const MAX_TEXT_CHARS = 50000

export interface ExtractResult {
  text: string
  pageCount: number
  isScanned: boolean
  wordCount: number
}

export async function extractTextFromFile(
  buffer: Buffer,
  mimeType: string
): Promise<ExtractResult> {
  if (mimeType === 'application/pdf') {
    return extractFromPdf(buffer)
  }

  if (mimeType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
    return extractFromDocx(buffer)
  }

  throw new Error(`Type de fichier non supporté : ${mimeType}`)
}

async function extractFromPdf(buffer: Buffer): Promise<ExtractResult> {
  let data: Awaited<ReturnType<typeof pdfParse>>

  try {
    data = await pdfParse(buffer)
  }
  catch {
    throw new Error('Impossible de lire le fichier PDF. Il est peut-être corrompu ou protégé par un mot de passe.')
  }

  const pageCount = data.numpages
  const rawText = data.text ?? ''
  const text = rawText.slice(0, MAX_TEXT_CHARS).trim()
  const wordCount = text.split(/\s+/).filter(Boolean).length

  const avgCharsPerPage = pageCount > 0 ? rawText.length / pageCount : 0
  const isScanned = avgCharsPerPage < MIN_CHARS_PER_PAGE

  return { text, pageCount, isScanned, wordCount }
}

async function extractFromDocx(buffer: Buffer): Promise<ExtractResult> {
  let result: Awaited<ReturnType<typeof mammoth.extractRawText>>

  try {
    result = await mammoth.extractRawText({ buffer })
  }
  catch {
    throw new Error('Impossible de lire le fichier DOCX. Il est peut-être corrompu.')
  }

  const rawText = result.value ?? ''
  const text = rawText.slice(0, MAX_TEXT_CHARS).trim()
  const wordCount = text.split(/\s+/).filter(Boolean).length

  // DOCX files always contain text if valid
  const isScanned = wordCount < 20

  return { text, pageCount: 1, isScanned, wordCount }
}

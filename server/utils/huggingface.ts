import { HfInference } from '@huggingface/inference'
import { buildAtsPrompt, AtsResultSchema, type AtsResult } from './ats-prompt'

const MODEL = 'mistralai/Mistral-7B-Instruct-v0.3'
const TIMEOUT_MS = 55000

let hfClient: HfInference | null = null

function getClient(): HfInference {
  if (hfClient) return hfClient
  hfClient = new HfInference(process.env.HUGGINGFACE_API_KEY)
  return hfClient
}

export async function analyzeAts(params: {
  cvText: string
  jobTitle: string
  companyName: string | null
  jobDescription: string
}): Promise<AtsResult> {
  const { system, user } = buildAtsPrompt(params)
  const client = getClient()

  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS)

  let rawOutput = ''

  try {
    const stream = client.chatCompletionStream({
      model: MODEL,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: user }
      ],
      temperature: 0.2,
      max_tokens: 2048
    })

    for await (const chunk of stream) {
      if (controller.signal.aborted) break
      rawOutput += chunk.choices[0]?.delta?.content ?? ''
    }
  }
  catch (err: unknown) {
    clearTimeout(timeout)
    if ((err as Error)?.name === 'AbortError') {
      throw new Error('L\'analyse a dépassé le délai maximum. Réessayez.')
    }
    console.error('HuggingFace API error:', (err as Error).message)
    throw new Error('L\'analyse IA a échoué. Réessayez dans quelques instants.')
  }
  finally {
    clearTimeout(timeout)
  }

  // Extract JSON from response (model may wrap it in markdown code blocks)
  const jsonMatch = rawOutput.match(/\{[\s\S]*\}/)
  if (!jsonMatch) {
    throw new Error('Réponse du modèle invalide : aucun JSON trouvé')
  }

  let parsed: unknown
  try {
    parsed = JSON.parse(jsonMatch[0])
  }
  catch {
    throw new Error('Réponse du modèle invalide : JSON malformé')
  }

  const validated = AtsResultSchema.safeParse(parsed)
  if (!validated.success) {
    console.error('ATS schema validation failed:', validated.error.errors)
    throw new Error('Réponse du modèle invalide : structure incorrecte')
  }

  return validated.data
}

import { z } from 'zod'

export const AtsResultSchema = z.object({
  score: z.number().int().min(0).max(100),
  matched_keywords: z.array(z.object({
    keyword: z.string(),
    context: z.string().optional()
  })),
  missing_keywords: z.array(z.object({
    keyword: z.string(),
    importance: z.enum(['high', 'medium', 'low'])
  })),
  sections_analysis: z.object({
    experience: z.object({ score: z.number().int().min(0).max(100), feedback: z.string() }),
    skills: z.object({ score: z.number().int().min(0).max(100), feedback: z.string() }),
    education: z.object({ score: z.number().int().min(0).max(100), feedback: z.string() }),
    formatting: z.object({ score: z.number().int().min(0).max(100), feedback: z.string() })
  }),
  suggestions: z.array(z.object({
    original: z.string(),
    improved: z.string(),
    reason: z.string()
  })).max(5),
  seniority_match: z.object({
    cv_level: z.enum(['junior', 'mid', 'senior', 'executive']),
    job_level: z.enum(['junior', 'mid', 'senior', 'executive']),
    match: z.boolean()
  }),
  summary: z.string()
})

export type AtsResult = z.infer<typeof AtsResultSchema>

export function buildAtsPrompt(params: {
  cvText: string
  jobTitle: string
  companyName: string | null
  jobDescription: string
}): { system: string, user: string } {
  const system = `Tu es un expert en recrutement et en systèmes ATS (Applicant Tracking Systems) avec 15 ans d'expérience.

Analyse la compatibilité entre un CV et une offre d'emploi. Retourne UNIQUEMENT un objet JSON valide avec cette structure exacte :

{
  "score": <entier 0-100>,
  "matched_keywords": [{"keyword": "...", "context": "..."}],
  "missing_keywords": [{"keyword": "...", "importance": "high|medium|low"}],
  "sections_analysis": {
    "experience": {"score": <0-100>, "feedback": "..."},
    "skills": {"score": <0-100>, "feedback": "..."},
    "education": {"score": <0-100>, "feedback": "..."},
    "formatting": {"score": <0-100>, "feedback": "..."}
  },
  "suggestions": [{"original": "...", "improved": "...", "reason": "..."}],
  "seniority_match": {"cv_level": "junior|mid|senior|executive", "job_level": "junior|mid|senior|executive", "match": true|false},
  "summary": "..."
}

Règles de scoring :
- 0-40 : Faible compatibilité (mots-clés manquants, expérience insuffisante)
- 41-70 : Compatibilité moyenne (quelques lacunes importantes)
- 71-100 : Bonne compatibilité (CV bien aligné avec l'offre)

Sois précis, factuel et actionnable. Les suggestions doivent être concrètes.`

  const user = `=== CV DU CANDIDAT ===
${params.cvText}

=== OFFRE D'EMPLOI ===
Titre du poste : ${params.jobTitle}
Entreprise : ${params.companyName ?? 'Non précisée'}
Description :
${params.jobDescription}`

  return { system, user }
}

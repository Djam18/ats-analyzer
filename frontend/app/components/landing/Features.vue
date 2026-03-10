<template>
  <section id="features" class="py-20 bg-[#F8F9FA]">
    <div class="mx-auto max-w-6xl px-6">
      <div class="mb-16 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">Fonctionnalités</p>
        <h2 class="text-3xl font-bold text-[#1A202C] md:text-4xl">Tout ce dont vous avez besoin</h2>
        <p class="mx-auto mt-4 max-w-xl text-[#718096]">
          Six modules complets pour couvrir l'intégralité de votre processus de recrutement.
        </p>
      </div>

      <div class="flex flex-col gap-16">
        <div
          v-for="(feature, i) in features"
          :key="feature.title"
          :class="[
            'grid items-center gap-10 lg:grid-cols-2',
            i % 2 === 1 ? 'lg:flex lg:flex-row-reverse' : '',
          ]"
        >
          <!-- Text -->
          <div :class="i % 2 === 1 ? 'lg:pl-10' : 'lg:pr-10'">
            <div
              class="mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl"
              :style="{ backgroundColor: feature.color + '18' }"
            >
              <component :is="feature.icon" class="h-5 w-5" :style="{ color: feature.color }" />
            </div>
            <h3 class="mb-3 text-xl font-bold text-[#1A202C]">{{ feature.title }}</h3>
            <p class="mb-5 text-[#718096]">{{ feature.desc }}</p>
            <ul class="space-y-2.5">
              <li v-for="point in feature.points" :key="point" class="flex items-start gap-2.5">
                <svg class="mt-0.5 h-4 w-4 flex-shrink-0 text-[#38A169]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-sm text-[#1A202C]">{{ point }}</span>
              </li>
            </ul>
          </div>

          <!-- Visual -->
          <div class="flex justify-center">
            <div
              class="flex h-56 w-full max-w-md items-center justify-center rounded-2xl border border-[#E2E8F0]"
              :style="{ background: `linear-gradient(135deg, ${feature.color}12, ${feature.color}06)` }"
            >
              <component :is="feature.icon" class="h-20 w-20 opacity-20" :style="{ color: feature.color }" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Briefcase, Upload, Star, LayoutDashboard, Mail, BarChart2 } from 'lucide-vue-next'

const features = [
  {
    icon: Briefcase,
    color: '#1E3A5F',
    title: 'Gestion des offres d\'emploi',
    desc: 'Créez et gérez vos offres en quelques clics. Chaque offre génère une URL publique unique pour recevoir directement les candidatures.',
    points: [
      'Statuts : Brouillon, Active, Clôturée, Archivée',
      'Critères pondérés configurables par offre',
      'URL publique générée automatiquement',
    ],
  },
  {
    icon: Upload,
    color: '#2E86AB',
    title: 'Upload & parsing de CVs',
    desc: 'Déposez un CV ou recevez une candidature via le formulaire public. L\'IA extrait toutes les informations en arrière-plan.',
    points: [
      'Formats PDF et DOCX acceptés',
      'Extraction IA : nom, email, compétences, expérience, formation',
      'Traitement asynchrone en moins de 30 secondes',
    ],
  },
  {
    icon: Star,
    color: '#D69E2E',
    title: 'Scoring & matching IA',
    desc: 'Chaque candidat reçoit un score de 0 à 100 calculé en fonction des critères de votre offre. Finis les décisions subjectives.',
    points: [
      'Score calculé sur 4 critères pondérables',
      'Alerte automatique si score dépasse un seuil',
      'Historique des scores par version de pondérations',
    ],
  },
  {
    icon: LayoutDashboard,
    color: '#805AD5',
    title: 'Pipeline Kanban visuel',
    desc: 'Visualisez l\'avancement de chaque candidat dans votre pipeline. Glissez-déposez pour faire avancer les profils.',
    points: [
      'Colonnes : Reçu → Présélection → Entretien RH → Entretien Tech → Offre → Embauché',
      'Notes internes et historique des actions',
      'Filtres par score, compétence ou statut',
    ],
  },
  {
    icon: Mail,
    color: '#38A169',
    title: 'Communication automatisée',
    desc: 'Envoyez les bons emails aux bons moments sans effort manuel. Chaque changement d\'étape peut déclencher un email personnalisé.',
    points: [
      'Templates d\'emails personnalisables',
      'Envoi automatique au changement d\'étape',
      'Variables dynamiques : nom, poste, date d\'entretien',
    ],
  },
  {
    icon: BarChart2,
    color: '#E53E3E',
    title: 'Dashboard & Reporting',
    desc: 'Mesurez l\'efficacité de votre recrutement avec des indicateurs clés. Exportez vos données en CSV.',
    points: [
      'KPIs : taux de conversion, délai moyen par étape',
      'Graphiques des sources et évolution temporelle',
      'Export CSV complet de toutes les données',
    ],
  },
]
</script>

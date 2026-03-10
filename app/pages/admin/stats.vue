<script setup lang="ts">
definePageMeta({ middleware: 'admin', layout: 'default' })

interface Stats {
  totalUsers: number
  totalAnalyses: number
  newUsersWeek: number
  newUsersMonth: number
  paidUsers: number
  conversionRate: number
  planCounts: Record<string, number>
  referralCounts: Record<string, number>
}

const { data: stats, pending, refresh } = await useFetch<Stats>('/api/admin/stats')

const referralLabels: Record<string, string> = {
  word_of_mouth: 'Bouche à oreille',
  linkedin: 'LinkedIn',
  google: 'Google',
  youtube_blog: 'YouTube / Blog',
  twitter: 'X / Twitter',
  other: 'Autre',
  unknown: 'Non renseigné'
}

const referralIcons: Record<string, string> = {
  word_of_mouth: 'i-lucide-users',
  linkedin: 'i-simple-icons-linkedin',
  google: 'i-simple-icons-google',
  youtube_blog: 'i-lucide-play-circle',
  twitter: 'i-simple-icons-x',
  other: 'i-lucide-more-horizontal',
  unknown: 'i-lucide-help-circle'
}

const planColors: Record<string, string> = {
  free: 'bg-gray-400',
  pro: 'bg-primary',
  expert: 'bg-purple-500'
}

const planLabels: Record<string, string> = {
  free: 'Gratuit',
  pro: 'Pro',
  expert: 'Expert'
}

const sortedReferrals = computed(() => {
  if (!stats.value) return []
  return Object.entries(stats.value.referralCounts)
    .sort(([, a], [, b]) => b - a)
})

const totalReferrals = computed(() =>
  sortedReferrals.value.reduce((sum, [, count]) => sum + count, 0)
)

const sortedPlans = computed(() => {
  if (!stats.value) return []
  return Object.entries(stats.value.planCounts)
    .sort(([, a], [, b]) => b - a)
})

const totalPlans = computed(() =>
  sortedPlans.value.reduce((sum, [, count]) => sum + count, 0)
)
</script>

<template>
  <div class="max-w-5xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          Stats Admin
        </h1>
        <p class="text-sm text-gray-500 mt-1">
          Vue d'ensemble de l'acquisition et de la croissance
        </p>
      </div>
      <UButton
        variant="outline"
        color="neutral"
        icon="i-lucide-refresh-cw"
        :loading="pending"
        @click="() => refresh()"
      >
        Actualiser
      </UButton>
    </div>

    <div v-if="pending" class="space-y-4">
      <div class="h-32 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse" />
      <div class="h-64 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse" />
    </div>

    <template v-else-if="stats">
      <!-- KPI cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <UCard>
          <div class="text-center">
            <p class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ stats.totalUsers }}
            </p>
            <p class="text-sm text-gray-500 mt-1">
              Utilisateurs total
            </p>
          </div>
        </UCard>
        <UCard>
          <div class="text-center">
            <p class="text-3xl font-bold text-green-600">
              +{{ stats.newUsersWeek }}
            </p>
            <p class="text-sm text-gray-500 mt-1">
              Nouveaux (7 jours)
            </p>
          </div>
        </UCard>
        <UCard>
          <div class="text-center">
            <p class="text-3xl font-bold text-primary">
              {{ stats.conversionRate }}%
            </p>
            <p class="text-sm text-gray-500 mt-1">
              Taux de conversion
            </p>
          </div>
        </UCard>
        <UCard>
          <div class="text-center">
            <p class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ stats.totalAnalyses }}
            </p>
            <p class="text-sm text-gray-500 mt-1">
              Analyses effectuées
            </p>
          </div>
        </UCard>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Acquisition sources -->
        <UCard>
          <h2 class="font-semibold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <UIcon name="i-lucide-pie-chart" class="w-5 h-5 text-primary" />
            Sources d'acquisition
          </h2>

          <div v-if="totalReferrals === 0" class="text-center py-8 text-gray-400 text-sm">
            Aucune donnée encore
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="([source, count]) in sortedReferrals"
              :key="source"
            >
              <div class="flex items-center justify-between mb-1">
                <div class="flex items-center gap-2">
                  <UIcon :name="referralIcons[source] ?? 'i-lucide-circle'" class="w-4 h-4 text-gray-500" />
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {{ referralLabels[source] ?? source }}
                  </span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-sm font-bold text-gray-900 dark:text-white">
                    {{ count }}
                  </span>
                  <span class="text-xs text-gray-400">
                    ({{ Math.round((count / totalReferrals) * 100) }}%)
                  </span>
                </div>
              </div>
              <div class="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-2">
                <div
                  class="h-2 rounded-full bg-primary transition-all duration-500"
                  :style="{ width: `${Math.round((count / totalReferrals) * 100)}%` }"
                />
              </div>
            </div>
          </div>
        </UCard>

        <!-- Plan distribution -->
        <UCard>
          <h2 class="font-semibold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <UIcon name="i-lucide-bar-chart-2" class="w-5 h-5 text-primary" />
            Répartition des plans
          </h2>

          <div v-if="totalPlans === 0" class="text-center py-8 text-gray-400 text-sm">
            Aucune donnée encore
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="([plan, count]) in sortedPlans"
              :key="plan"
            >
              <div class="flex items-center justify-between mb-1">
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full" :class="planColors[plan] ?? 'bg-gray-400'" />
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
                    {{ planLabels[plan] ?? plan }}
                  </span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-sm font-bold text-gray-900 dark:text-white">
                    {{ count }}
                  </span>
                  <span class="text-xs text-gray-400">
                    ({{ Math.round((count / totalPlans) * 100) }}%)
                  </span>
                </div>
              </div>
              <div class="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-2">
                <div
                  class="h-2 rounded-full transition-all duration-500"
                  :class="planColors[plan] ?? 'bg-gray-400'"
                  :style="{ width: `${Math.round((count / totalPlans) * 100)}%` }"
                />
              </div>
            </div>
          </div>

          <!-- Conversion summary -->
          <div class="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Utilisateurs payants</span>
              <span class="font-semibold text-gray-900 dark:text-white">
                {{ stats.paidUsers }} / {{ stats.totalUsers }}
              </span>
            </div>
            <div class="flex justify-between text-sm mt-1">
              <span class="text-gray-500">Nouveaux ce mois</span>
              <span class="font-semibold text-primary">
                +{{ stats.newUsersMonth }}
              </span>
            </div>
          </div>
        </UCard>
      </div>
    </template>
  </div>
</template>

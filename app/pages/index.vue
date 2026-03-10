<script setup lang="ts">
definePageMeta({ layout: false })

const user = useSupabaseUser()
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-950">
    <!-- Nav -->
    <header class="border-b border-gray-100 dark:border-gray-800">
      <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-file-search" class="w-6 h-6 text-primary" />
          <span class="font-bold text-lg text-gray-900 dark:text-white">ATS Analyzer</span>
        </div>
        <div class="flex items-center gap-3">
          <template v-if="user">
            <UButton to="/dashboard" color="primary">
              Tableau de bord
            </UButton>
          </template>
          <template v-else>
            <UButton to="/login" variant="ghost" color="neutral">
              Connexion
            </UButton>
            <UButton to="/register" color="primary">
              Essayer gratuitement
            </UButton>
          </template>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <section class="max-w-6xl mx-auto px-4 py-24 text-center">
      <UBadge color="primary" variant="subtle" class="mb-6">
        3 analyses gratuites sans carte bancaire
      </UBadge>
      <h1 class="text-5xl font-extrabold text-gray-900 dark:text-white leading-tight mb-6">
        Votre CV passe-t-il<br>
        <span class="text-primary">le filtre ATS ?</span>
      </h1>
      <p class="text-xl text-gray-500 dark:text-gray-400 max-w-2xl mx-auto mb-10">
        Analysez la compatibilité de votre CV avec les offres d'emploi en quelques secondes.
        Obtenez un score, des mots-clés manquants et des suggestions concrètes.
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <UButton
          :to="user ? '/analyses/new' : '/register'"
          size="xl"
          color="primary"
          trailing-icon="i-lucide-arrow-right"
        >
          Analyser mon CV maintenant
        </UButton>
        <UButton
          to="#how-it-works"
          size="xl"
          color="neutral"
          variant="subtle"
        >
          Voir comment ca marche
        </UButton>
      </div>
    </section>

    <!-- Social proof numbers -->
    <section class="bg-gray-50 dark:bg-gray-900 py-12">
      <div class="max-w-6xl mx-auto px-4 grid grid-cols-3 gap-8 text-center">
        <div>
          <p class="text-4xl font-bold text-primary">
            0-100
          </p>
          <p class="text-gray-500 mt-1">
            Score de compatibilité précis
          </p>
        </div>
        <div>
          <p class="text-4xl font-bold text-primary">
            &lt;30s
          </p>
          <p class="text-gray-500 mt-1">
            Temps d'analyse moyen
          </p>
        </div>
        <div>
          <p class="text-4xl font-bold text-primary">
            3
          </p>
          <p class="text-gray-500 mt-1">
            Analyses gratuites à vie
          </p>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section id="how-it-works" class="max-w-6xl mx-auto px-4 py-20">
      <h2 class="text-3xl font-bold text-center text-gray-900 dark:text-white mb-4">
        Simple comme bonjour
      </h2>
      <p class="text-center text-gray-500 mb-16 max-w-xl mx-auto">
        Trois etapes pour savoir si votre candidature a une chance de passer les filtres automatiques.
      </p>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="text-center">
          <div class="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-lucide-upload" class="w-8 h-8 text-primary" />
          </div>
          <div class="text-sm font-semibold text-primary mb-2">
            Etape 1
          </div>
          <h3 class="font-bold text-gray-900 dark:text-white mb-2">
            Importez votre CV
          </h3>
          <p class="text-gray-500 text-sm">
            Glissez-deposez votre CV en PDF ou DOCX. Max 5 Mo, 10 pages.
          </p>
        </div>
        <div class="text-center">
          <div class="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-lucide-clipboard-list" class="w-8 h-8 text-primary" />
          </div>
          <div class="text-sm font-semibold text-primary mb-2">
            Etape 2
          </div>
          <h3 class="font-bold text-gray-900 dark:text-white mb-2">
            Collez l'offre d'emploi
          </h3>
          <p class="text-gray-500 text-sm">
            Copiez la description du poste que vous visez. Plus c'est complet, plus l'analyse est precise.
          </p>
        </div>
        <div class="text-center">
          <div class="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-lucide-bar-chart-2" class="w-8 h-8 text-primary" />
          </div>
          <div class="text-sm font-semibold text-primary mb-2">
            Etape 3
          </div>
          <h3 class="font-bold text-gray-900 dark:text-white mb-2">
            Recevez votre rapport
          </h3>
          <p class="text-gray-500 text-sm">
            Score global, mots-cles manquants, analyse par section et suggestions de reformulation.
          </p>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="bg-gray-50 dark:bg-gray-900 py-20">
      <div class="max-w-6xl mx-auto px-4">
        <h2 class="text-3xl font-bold text-center text-gray-900 dark:text-white mb-4">
          Tout ce dont vous avez besoin
        </h2>
        <p class="text-center text-gray-500 mb-16 max-w-xl mx-auto">
          Une analyse complete pour maximiser vos chances d'obtenir un entretien.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <UCard>
            <div class="flex items-start gap-4">
              <UIcon name="i-lucide-target" class="w-6 h-6 text-primary shrink-0 mt-0.5" />
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white mb-1">
                  Score de compatibilite
                </h3>
                <p class="text-sm text-gray-500">
                  Un score de 0 a 100 qui reflète precisement votre adequation avec le poste.
                </p>
              </div>
            </div>
          </UCard>
          <UCard>
            <div class="flex items-start gap-4">
              <UIcon name="i-lucide-key" class="w-6 h-6 text-primary shrink-0 mt-0.5" />
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white mb-1">
                  Mots-cles manquants
                </h3>
                <p class="text-sm text-gray-500">
                  Identifiez les termes essentiels absents de votre CV, classes par importance.
                </p>
              </div>
            </div>
          </UCard>
          <UCard>
            <div class="flex items-start gap-4">
              <UIcon name="i-lucide-layers" class="w-6 h-6 text-primary shrink-0 mt-0.5" />
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white mb-1">
                  Analyse par section
                </h3>
                <p class="text-sm text-gray-500">
                  Scores detailles pour l'experience, les competences, la formation et le format.
                </p>
              </div>
            </div>
          </UCard>
          <UCard>
            <div class="flex items-start gap-4">
              <UIcon name="i-lucide-pen-line" class="w-6 h-6 text-primary shrink-0 mt-0.5" />
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white mb-1">
                  Suggestions de reformulation
                </h3>
                <p class="text-sm text-gray-500">
                  Des phrases "avant/apres" concretes pour ameliorer votre CV immediatement.
                </p>
              </div>
            </div>
          </UCard>
          <UCard>
            <div class="flex items-start gap-4">
              <UIcon name="i-lucide-users" class="w-6 h-6 text-primary shrink-0 mt-0.5" />
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white mb-1">
                  Correspondance de seniorite
                </h3>
                <p class="text-sm text-gray-500">
                  Verifiez si votre niveau d'experience correspond au poste vise.
                </p>
              </div>
            </div>
          </UCard>
          <UCard>
            <div class="flex items-start gap-4">
              <UIcon name="i-lucide-history" class="w-6 h-6 text-primary shrink-0 mt-0.5" />
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white mb-1">
                  Historique des analyses
                </h3>
                <p class="text-sm text-gray-500">
                  Retrouvez et comparez toutes vos analyses precedentes en un clic.
                </p>
              </div>
            </div>
          </UCard>
        </div>
      </div>
    </section>

    <!-- Pricing -->
    <section class="max-w-6xl mx-auto px-4 py-20">
      <h2 class="text-3xl font-bold text-center text-gray-900 dark:text-white mb-4">
        Tarifs simples et transparents
      </h2>
      <p class="text-center text-gray-500 mb-16">
        Commencez gratuitement. Passez au Pro quand vous en avez besoin.
      </p>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
        <!-- Free -->
        <UCard>
          <div class="text-center p-2">
            <h3 class="font-bold text-lg text-gray-900 dark:text-white mb-2">
              Gratuit
            </h3>
            <p class="text-4xl font-extrabold text-gray-900 dark:text-white mb-1">
              0€
            </p>
            <p class="text-sm text-gray-400 mb-6">
              a vie
            </p>
            <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-2 text-left mb-8">
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                3 analyses a vie
              </li>
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                Score + mots-cles
              </li>
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                Suggestions basiques
              </li>
            </ul>
            <UButton :to="user ? '/dashboard' : '/register'" block color="neutral" variant="outline">
              Commencer
            </UButton>
          </div>
        </UCard>

        <!-- Pro -->
        <UCard class="ring-2 ring-primary">
          <div class="text-center p-2">
            <UBadge color="primary" class="mb-3">
              Populaire
            </UBadge>
            <h3 class="font-bold text-lg text-gray-900 dark:text-white mb-2">
              Pro
            </h3>
            <p class="text-4xl font-extrabold text-gray-900 dark:text-white mb-1">
              9,99€
            </p>
            <p class="text-sm text-gray-400 mb-6">
              par mois
            </p>
            <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-2 text-left mb-8">
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                50 analyses / mois
              </li>
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                Analyse complete
              </li>
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                Historique illimite
              </li>
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                Support email
              </li>
            </ul>
            <UButton :to="user ? '/pricing' : '/register'" block color="primary">
              Essayer Pro
            </UButton>
          </div>
        </UCard>

        <!-- Expert -->
        <UCard>
          <div class="text-center p-2">
            <h3 class="font-bold text-lg text-gray-900 dark:text-white mb-2">
              Expert
            </h3>
            <p class="text-4xl font-extrabold text-gray-900 dark:text-white mb-1">
              19,99€
            </p>
            <p class="text-sm text-gray-400 mb-6">
              par mois
            </p>
            <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-2 text-left mb-8">
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                Analyses illimitees
              </li>
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                Analyse complete
              </li>
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                Historique illimite
              </li>
              <li class="flex items-center gap-2">
                <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 shrink-0" />
                Support prioritaire
              </li>
            </ul>
            <UButton :to="user ? '/pricing' : '/register'" block color="neutral" variant="outline">
              Choisir Expert
            </UButton>
          </div>
        </UCard>
      </div>
    </section>

    <!-- CTA Banner -->
    <section class="bg-primary py-16">
      <div class="max-w-3xl mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold text-white mb-4">
          Pret a decrocher plus d'entretiens ?
        </h2>
        <p class="text-primary-100 mb-8 text-lg">
          Rejoignez les candidats qui optimisent leur CV avec ATS Analyzer.
          Commencez gratuitement, sans carte bancaire.
        </p>
        <UButton
          :to="user ? '/analyses/new' : '/register'"
          size="xl"
          color="neutral"
          variant="solid"
          trailing-icon="i-lucide-arrow-right"
        >
          Analyser mon CV maintenant
        </UButton>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-gray-100 dark:border-gray-800 py-8">
      <div class="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2 text-gray-500">
          <UIcon name="i-lucide-file-search" class="w-4 h-4" />
          <span class="text-sm font-medium">ATS Analyzer</span>
        </div>
        <div class="flex items-center gap-6 text-sm text-gray-400">
          <NuxtLink to="/login" class="hover:text-gray-600 dark:hover:text-gray-300">
            Connexion
          </NuxtLink>
          <NuxtLink to="/register" class="hover:text-gray-600 dark:hover:text-gray-300">
            Inscription
          </NuxtLink>
          <NuxtLink to="/pricing" class="hover:text-gray-600 dark:hover:text-gray-300">
            Tarifs
          </NuxtLink>
        </div>
        <p class="text-xs text-gray-400">
          &copy; 2025 ATS Analyzer. Tous droits reserves.
        </p>
      </div>
    </footer>
  </div>
</template>

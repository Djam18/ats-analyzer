<template>
  <section id="faq" class="py-20 bg-[#F8F9FA]">
    <div class="mx-auto max-w-3xl px-6">
      <div class="mb-12 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">FAQ</p>
        <h2 class="text-3xl font-bold text-[#1A202C] md:text-4xl">Questions fréquentes</h2>
      </div>

      <div class="divide-y divide-[#E2E8F0] rounded-xl border border-[#E2E8F0] bg-white overflow-hidden">
        <div v-for="(item, i) in faqs" :key="item.question">
          <button
            class="flex w-full items-center justify-between gap-4 px-6 py-5 text-left hover:bg-[#F8F9FA] transition-colors"
            @click="open === i ? open = null : open = i"
          >
            <span class="font-semibold text-[#1A202C] text-sm">{{ item.question }}</span>
            <svg
              :class="['h-4 w-4 flex-shrink-0 text-[#718096] transition-transform duration-200', open === i ? 'rotate-180' : '']"
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div v-if="open === i" class="px-6 pb-5">
            <p class="text-sm leading-relaxed text-[#718096]">{{ item.answer }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
const open = ref<number | null>(0)

const faqs = computed(() =>  [
  {
    question: 'Comment fonctionne l\'analyse IA des CVs ?',
    answer: 'Dès qu\'un CV est uploadé (PDF ou DOCX), il est placé dans une file de traitement. Notre IA (Mistral 7B, modèle open source hébergé localement) extrait le nom, l\'email, les compétences, les années d\'expérience, la formation et les langues. Le score est ensuite calculé en comparant ces données aux critères pondérés de votre offre. Tout cela en moins de 30 secondes.',
  },
  {
    question: 'Mes données sont-elles sécurisées ?',
    answer: 'Oui. Toutes les données sont hébergées en France sur des serveurs sécurisés. Les CVs sont stockés avec des URLs signées à durée limitée (1 heure). Notre IA tourne en local, vos CVs ne sont jamais envoyés à un service tiers. Nous sommes conformes RGPD : chaque candidat peut demander l\'accès ou la suppression de ses données.',
  },
  {
    question: 'Puis-je importer mes candidats existants ?',
    answer: 'Oui. Vous pouvez uploader des CVs en lot directement depuis l\'interface. Un fichier CSV d\'import est également disponible pour les plans Pro et Entreprise, permettant de migrer vos données depuis un autre outil.',
  },
  {
    question: 'Combien de temps pour mettre en place la solution ?',
    answer: 'Moins de 10 minutes. Créez votre compte, configurez votre première offre avec vos critères pondérés, et partagez le lien de candidature. L\'IA s\'occupe du reste dès le premier CV reçu. Aucune formation technique requise.',
  },
  {
    question: 'Puis-je annuler mon abonnement à tout moment ?',
    answer: 'Oui, sans engagement. Vous pouvez annuler depuis vos paramètres à tout moment. Votre compte passe automatiquement en plan Découverte. Vos données sont conservées 90 jours après l\'annulation, puis supprimées définitivement sur demande.',
  },
]);
</script>

<template>
  <footer class="bg-[#1A202C] text-white">
    <div class="mx-auto max-w-6xl px-6 py-12">
      <div class="grid gap-8 md:grid-cols-4">
        <!-- Col 1: Brand -->
        <div class="md:col-span-1">
          <SharedLogo size="md" variant="light" />
          <p class="mt-3 text-sm text-white/60 leading-relaxed">
            Recrutement intelligent propulsé par l'IA. Données hébergées en France.
          </p>
          <p class="mt-4 text-xs text-white/40">RGPD · Made in France</p>
        </div>

        <!-- Col 2: Produit -->
        <div>
          <h4 class="mb-4 text-sm font-semibold uppercase tracking-wider text-white/50">Produit</h4>
          <ul class="space-y-2.5">
            <li v-for="link in productLinks" :key="link.label">
              <a :href="link.href" class="text-sm text-white/70 hover:text-white transition-colors">
                {{ link.label }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Col 3: Ressources -->
        <div>
          <h4 class="mb-4 text-sm font-semibold uppercase tracking-wider text-white/50">Ressources</h4>
          <ul class="space-y-2.5">
            <li v-for="link in resourceLinks" :key="link.label">
              <a :href="link.href" class="text-sm text-white/70 hover:text-white transition-colors">
                {{ link.label }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Col 4: Contact -->
        <div>
          <h4 class="mb-4 text-sm font-semibold uppercase tracking-wider text-white/50">Contact</h4>
          <ul class="space-y-2.5">
            <li>
              <a href="mailto:bonjour@ats-platform.fr" class="text-sm text-white/70 hover:text-white transition-colors">
                bonjour@ats-platform.fr
              </a>
            </li>
            <li class="text-sm text-white/40">Paris, France</li>
          </ul>
        </div>
      </div>

      <div class="mt-10 flex flex-col items-center justify-between gap-4 border-t border-white/10 pt-8 md:flex-row">
        <p class="text-xs text-white/40">© 2025 ATS Platform. Tous droits réservés.</p>
        <div class="flex gap-4">
          <a href="#" class="text-xs text-white/40 hover:text-white/70 transition-colors">Mentions légales</a>
          <a href="#" class="text-xs text-white/40 hover:text-white/70 transition-colors">Politique de confidentialité</a>
          <a href="#" class="text-xs text-white/40 hover:text-white/70 transition-colors">CGU</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const productLinks = [
  { label: 'Fonctionnalités', href: '#features' },
  { label: 'Tarifs', href: '#pricing' },
  { label: 'FAQ', href: '#faq' },
  { label: 'Se connecter', href: '/login' },
  { label: 'Créer un compte', href: '/register' },
]

const resourceLinks = [
  { label: 'Documentation', href: '#' },
  { label: 'API REST', href: '#' },
  { label: 'Blog', href: '#' },
  { label: 'Changelog', href: '#' },
]
</script>

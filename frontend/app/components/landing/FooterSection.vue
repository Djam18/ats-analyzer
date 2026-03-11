<template>
  <footer class="bg-[#1A202C] text-white">
    <div class="mx-auto max-w-6xl px-6 py-12">
      <div class="grid gap-8 md:grid-cols-4">
        <!-- Col 1: Brand -->
        <div class="md:col-span-1">
          <SharedLogo size="md" variant="light" />
          <p class="mt-3 text-sm text-white/60 leading-relaxed">
            {{ $t('footer.tagline') }}
          </p>
          <p class="mt-4 text-xs text-white/40">{{ $t('footer.rgpd') }}</p>
        </div>

        <!-- Col 2: Product -->
        <div>
          <h4 class="mb-4 text-sm font-semibold uppercase tracking-wider text-white/50">{{ $t('footer.col_product') }}</h4>
          <ul class="space-y-2.5">
            <li v-for="link in productLinks" :key="link.key">
              <NuxtLink v-if="link.internal" :to="link.href" class="text-sm text-white/70 hover:text-white transition-colors">
                {{ $t(link.key) }}
              </NuxtLink>
              <a v-else :href="link.href" class="text-sm text-white/70 hover:text-white transition-colors">
                {{ $t(link.key) }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Col 3: Ressources -->
        <div>
          <h4 class="mb-4 text-sm font-semibold uppercase tracking-wider text-white/50">{{ $t('footer.col_resources') }}</h4>
          <ul class="space-y-2.5">
            <li v-for="link in resourceLinks" :key="link.key">
              <NuxtLink v-if="link.internal" :to="link.href" class="text-sm text-white/70 hover:text-white transition-colors">
                {{ $t(link.key) }}
              </NuxtLink>
              <a v-else :href="link.href" class="text-sm text-white/70 hover:text-white transition-colors">
                {{ $t(link.key) }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Col 4: Contact -->
        <div>
          <h4 class="mb-4 text-sm font-semibold uppercase tracking-wider text-white/50">{{ $t('footer.col_contact') }}</h4>
          <ul class="space-y-2.5">
            <li>
              <a href="mailto:bonjour@ats-platform.fr" class="text-sm text-white/70 hover:text-white transition-colors">
                bonjour@ats-platform.fr
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="mt-10 flex flex-col items-center justify-between gap-4 border-t border-white/10 pt-8 md:flex-row">
        <p class="text-xs text-white/40">{{ $t('footer.copyright', { year: new Date().getFullYear() }) }}</p>
        <div class="flex gap-4">
          <NuxtLink to="/legal/mentions" class="text-xs text-white/40 hover:text-white/70 transition-colors">{{ $t('footer.legal') }}</NuxtLink>
          <NuxtLink to="/legal/privacy" class="text-xs text-white/40 hover:text-white/70 transition-colors">{{ $t('footer.privacy') }}</NuxtLink>
          <NuxtLink to="/legal/terms" class="text-xs text-white/40 hover:text-white/70 transition-colors">{{ $t('footer.terms') }}</NuxtLink>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const productLinks = [
  { key: 'footer.link_features', href: '#features', internal: false },
  { key: 'footer.link_pricing', href: '#pricing', internal: false },
  { key: 'footer.link_faq', href: '#faq', internal: false },
  { key: 'footer.link_login', href: '/login', internal: true },
  { key: 'footer.link_register', href: '/register', internal: true },
]

const resourceLinks = [
  { key: 'footer.link_docs', href: '/docs', internal: true },
]
</script>

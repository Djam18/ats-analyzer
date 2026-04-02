import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },

  modules: ['@nuxtjs/i18n'],

  runtimeConfig: {
    supabaseServiceKey: process.env.SUPABASE_SERVICE_KEY ?? '',
    stripeSecretKey: process.env.STRIPE_SECRET_KEY ?? '',
    stripeWebhookSecret: process.env.STRIPE_WEBHOOK_SECRET ?? '',
    resendApiKey: process.env.RESEND_API_KEY ?? '',
    public: {
      supabaseUrl: process.env.SUPABASE_URL ?? '',
      supabaseAnonKey: process.env.SUPABASE_KEY ?? '',
      stripePriceBasic: process.env.STRIPE_PRICE_BASIC ?? '',
      stripePricePro: process.env.STRIPE_PRICE_PRO ?? '',
    },
  },

  css: ['~/assets/css/main.css'],
  // Nuxt 4: ~ resolves to the app/ directory

  vite: {
    plugins: [tailwindcss()],
  },

  i18n: {
    locales: [
      { code: 'fr', language: 'fr-FR', name: 'Français', file: 'fr.json' },
      { code: 'en', language: 'en-US', name: 'English', file: 'en.json' },
      { code: 'zh', language: 'zh-CN', name: '中文', file: 'zh.json' },
      { code: 'hi', language: 'hi-IN', name: 'हिन्दी', file: 'hi.json' },
      { code: 'es', language: 'es-ES', name: 'Español', file: 'es.json' },
    ],
    defaultLocale: 'fr',
    strategy: 'no_prefix',
    lazy: true,
    langDir: '../i18n/locales',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'ats-locale',
      redirectOn: 'root',
      fallbackLocale: 'fr',
    },
  },

  app: {
    head: {
      title: 'ATS Platform — Recrutement intelligent avec IA',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'ATS Platform centralise vos CVs, analyse chaque candidat avec l\'IA et gère votre pipeline de recrutement en temps réel.',
        },
        { property: 'og:title', content: 'ATS Platform — Recrutement intelligent avec IA' },
        {
          property: 'og:description',
          content: 'Trouvez le bon profil 3x plus vite grâce à l\'IA. Scoring automatique, pipeline Kanban, emails automatisés.',
        },
        { property: 'og:type', content: 'website' },
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Sans+Devanagari:wght@400;500;700&display=swap',
        },
      ],
    },
  },
})

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@nuxtjs/supabase',
    '@nuxtjs/i18n'
  ],

  devtools: {
    enabled: process.env.NODE_ENV === 'development'
  },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/': { prerender: true }
  },

  compatibilityDate: '2025-01-15',

  runtimeConfig: {
    huggingfaceApiKey: process.env.HUGGINGFACE_API_KEY || '',
    stripeSecretKey: process.env.STRIPE_SECRET_KEY || '',
    stripeWebhookSecret: process.env.STRIPE_WEBHOOK_SECRET || '',
    resendApiKey: process.env.RESEND_API_KEY || '',
    supabaseServiceKey: process.env.SUPABASE_KEY || '',
    adminEmail: process.env.ADMIN_EMAIL || '',
    public: {
      stripePriceProMonthly: process.env.NUXT_PUBLIC_STRIPE_PRICE_PRO_MONTHLY || '',
      stripePriceExpertMonthly: process.env.NUXT_PUBLIC_STRIPE_PRICE_EXPERT_MONTHLY || '',
      appUrl: 'http://localhost:3000'
    }
  },

  supabase: {
    redirect: false
  },

  i18n: {
    locales: [
      { code: 'fr', language: 'fr-FR', name: 'Français', file: 'fr.json' },
      { code: 'en', language: 'en-US', name: 'English', file: 'en.json' }
    ],
    defaultLocale: 'fr',
    strategy: 'no_prefix',
    langDir: 'locales/',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'ats_locale',
      redirectOn: 'root',
      alwaysRedirect: false
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})

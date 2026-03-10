import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },

  css: ['~/assets/css/main.css'],
  // Nuxt 4: ~ resolves to the app/ directory

  vite: {
    plugins: [tailwindcss()],
  },

  app: {
    head: {
      htmlAttrs: { lang: 'fr' },
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
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap',
        },
      ],
    },
  },
})

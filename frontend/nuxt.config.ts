export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/css/tailwind.css'],
  modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss'],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
    },
  },
  typescript: {
    strict: true,
  },
  app: {
    head: {
      title: 'PhotoCut',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Background removal and photo processing SaaS MVP' },
      ],
    },
  },
})

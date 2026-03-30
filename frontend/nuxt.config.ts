// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@vee-validate/nuxt',
  ],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1',
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || 'http://localhost:3000',
      siteName: 'AutoFilm',
      siteDescription: 'Phim cách nhiệt ô tô cao cấp - Dán phim PPF - Phim đổi màu xe chuyên nghiệp',
    }
  },

  app: {
    head: {
      htmlAttrs: {
        lang: 'vi'
      },
      title: 'AutoFilm - Phim Cách Nhiệt Ô Tô Cao Cấp',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'format-detection', content: 'telephone=no' },
        { name: 'robots', content: 'index, follow' },
        { name: 'author', content: 'AutoFilm' },
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: 'AutoFilm' },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' },
      ]
    }
  },

  tailwindcss: {
    cssPath: '~/assets/css/main.css',
  },

  veeValidate: {
    autoImports: true,
  },

  typescript: {
    strict: true
  },

  compatibilityDate: '2024-01-01'
})

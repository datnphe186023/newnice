// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: process.env.NODE_ENV !== 'production' },
  
  modules: [
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@vee-validate/nuxt',
  ],

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1',
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || 'http://localhost:3000',
      siteName: 'Newnice',
      siteDescription: 'Newnice là thương hiệu phim cách nhiệt, PPF bảo vệ bề mặt và giải pháp film nhà kính tại Việt Nam.',
      gaId: process.env.NUXT_PUBLIC_GA_ID || '',                   // GA4 measurement ID e.g. G-XXXXXXXXXX
      gscVerification: process.env.NUXT_PUBLIC_GSC_VERIFICATION || '', // Google Search Console verification token
    }
  },

  app: {
    head: {
      htmlAttrs: {
        lang: 'vi'
      },
      title: 'Newnice - Website chính thức | Phim cách nhiệt, PPF và Film nhà kính',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'format-detection', content: 'telephone=no' },
        { name: 'robots', content: 'index, follow' },
        { name: 'author', content: 'Newnice' },
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: 'Newnice' },
        // Google Search Console verification — set NUXT_PUBLIC_GSC_VERIFICATION in .env
        ...(process.env.NUXT_PUBLIC_GSC_VERIFICATION
          ? [{ name: 'google-site-verification', content: process.env.NUXT_PUBLIC_GSC_VERIFICATION }]
          : []),
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico?v=3' },
        { rel: 'shortcut icon', href: '/favicon.ico?v=3' },
        { rel: 'icon', type: 'image/png', sizes: '512x512', href: '/favicon-512.png?v=3' },
        { rel: 'apple-touch-icon', href: '/favicon-512.png?v=3' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' },
      ]
    }
  },

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },

  veeValidate: {
    autoImports: true,
  },

  typescript: {
    strict: true
  },

  compatibilityDate: '2024-01-01'
})

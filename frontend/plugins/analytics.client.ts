/**
 * Google Analytics 4 plugin.
 * Loads gtag.js on client-side only and exposes $gtag globally.
 * Set NUXT_PUBLIC_GA_ID in .env — leave empty to disable in dev.
 */
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const gaId = config.public.gaId as string

  if (!gaId || import.meta.server) return

  // Inject the gtag script
  useHead({
    script: [
      {
        src: `https://www.googletagmanager.com/gtag/js?id=${gaId}`,
        async: true,
      },
      {
        innerHTML: `
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${gaId}', { send_page_view: false });
        `,
      },
    ],
  })

  // Track page views on route change
  const router = useRouter()
  router.afterEach((to) => {
    if (typeof window !== 'undefined' && (window as any).gtag) {
      ;(window as any).gtag('event', 'page_view', {
        page_path: to.fullPath,
        page_title: document.title,
      })
    }
  })

  return {
    provide: {
      gtag: (...args: any[]) => {
        if (typeof window !== 'undefined' && (window as any).gtag) {
          ;(window as any).gtag(...args)
        }
      },
    },
  }
})

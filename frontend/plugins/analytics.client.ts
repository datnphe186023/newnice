/**
 * Google Analytics 4 plugin.
 * Loads gtag.js on client-side only and exposes $gtag globally.
 * Set NUXT_PUBLIC_GA_ID in .env — leave empty to disable in dev.
 */
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const gaId = config.public.gaId as string

  const trackGtag = (...args: unknown[]) => {
    if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      ;(window as any).gtag(...args)
    }
  }

  if (!gaId || import.meta.server) {
    return {
      provide: {
        gtag: trackGtag,
      },
    }
  }

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
    trackGtag('event', 'page_view', {
      page_path: to.fullPath,
      page_title: document.title,
    })
  })

  return {
    provide: {
      gtag: trackGtag,
    },
  }
})

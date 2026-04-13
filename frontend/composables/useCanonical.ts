/**
 * useCanonical — injects a <link rel="canonical"> tag into the page <head>.
 *
 * Reads `config.public.siteUrl` from runtime config (strips trailing slash),
 * then calls useHead with the absolute canonical URL.
 *
 * Usage:
 *   useCanonical('/san-pham/phim-3m')
 *   useCanonical(useRoute().path)  // for dynamic pages
 *
 * Production: set NUXT_PUBLIC_SITE_URL=https://newnice.vn
 */
export function useCanonical(path: string): void {
  const config = useRuntimeConfig()
  const siteUrl = (config.public.siteUrl as string).replace(/\/$/, '')
  useHead({
    link: [{ rel: 'canonical', href: `${siteUrl}${path}` }],
  })
}

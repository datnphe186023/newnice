/**
 * useJsonLd — injects JSON-LD structured data into the page <head>.
 *
 * Usage:
 *   useJsonLd(buildProductSchema(product))
 *   useJsonLd(buildArticleSchema(post))
 *   useJsonLd(buildOrganizationSchema())
 */

const DEFAULT_SITE_URL = 'https://newnice.net'
const ORG_NAME = 'Newnice'
const ORG_PHONE = '+84869418104'

function getSiteUrl(): string {
  const config = useRuntimeConfig()
  return ((config.public.siteUrl as string) || DEFAULT_SITE_URL).replace(/\/$/, '')
}

function absoluteUrl(url?: string): string | undefined {
  if (!url) return undefined
  if (/^https?:\/\//i.test(url)) return url
  const siteUrl = getSiteUrl()
  return `${siteUrl}${url.startsWith('/') ? url : `/${url}`}`
}
const ORG_ADDRESS = '311 Phúc Diễn, Nam Từ Liêm, Hà Nội, Việt Nam'

// ---------------------------------------------------------------------------
// Core inject helper
// ---------------------------------------------------------------------------

export function useJsonLd(schema: Record<string, unknown> | Record<string, unknown>[]) {
  const schemas = Array.isArray(schema) ? schema : [schema]
  useHead({
    script: schemas.map((s) => ({
      type: 'application/ld+json',
      innerHTML: JSON.stringify(s),
    })),
  })
}

// ---------------------------------------------------------------------------
// Organization (site-wide)
// ---------------------------------------------------------------------------

export function buildOrganizationSchema() {
  const siteUrl = getSiteUrl()
  return {
    '@context': 'https://schema.org',
    '@type': 'AutoRepair',  // More specific than Organization for a car service biz
    name: ORG_NAME,
    url: siteUrl,
    logo: `${siteUrl}/logo.png`,
    telephone: ORG_PHONE,
    address: {
      '@type': 'PostalAddress',
      streetAddress: '311 Phúc Diễn',
      addressLocality: 'Nam Từ Liêm',
      addressRegion: 'Hà Nội',
      addressCountry: 'VN',
    },
    openingHoursSpecification: [
      {
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        opens: '08:00',
        closes: '18:00',
      },
    ],
    sameAs: [
      'https://www.facebook.com/newnicevn',
      'https://zalo.me/0705410751',
    ],
  }
}

// ---------------------------------------------------------------------------
// Product page
// ---------------------------------------------------------------------------

export function buildProductSchema(product: {
  name: string
  slug: string
  short_description?: string
  price_sedan?: string
  price_suv?: string
  is_contact_price?: boolean
  thumbnail?: string
  brand?: { name: string }
  warranty_years?: number
}) {
  const siteUrl = getSiteUrl()
  const url = `${siteUrl}/san-pham/${product.slug}`
  const priceAmount = [product.price_sedan, product.price_suv]
    .filter(Boolean)
    .map((price) => price?.replace(/\D/g, ''))
    .find(Boolean)

  const schema: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    url,
    description: product.short_description,
    image: product.thumbnail ? [absoluteUrl(product.thumbnail)] : undefined,
    brand: product.brand
      ? { '@type': 'Brand', name: product.brand.name }
      : undefined,
    manufacturer: { '@type': 'Organization', name: ORG_NAME },
    offers: {
      '@type': 'Offer',
      url,
      priceCurrency: 'VND',
      availability: 'https://schema.org/InStock',
      seller: { '@type': 'Organization', name: ORG_NAME },
      ...(product.is_contact_price || !priceAmount
        ? { price: '0', priceSpecification: { '@type': 'UnitPriceSpecification', name: 'Liên hệ báo giá' } }
        : { price: priceAmount }),
    },
    ...(product.warranty_years
      ? { warranty: { '@type': 'WarrantyPromise', durationOfWarranty: { '@type': 'QuantitativeValue', value: product.warranty_years, unitCode: 'ANN' } } }
      : {}),
  }
  return schema
}

// ---------------------------------------------------------------------------
// Blog article page
// ---------------------------------------------------------------------------

export function buildArticleSchema(post: {
  title: string
  slug: string
  excerpt?: string
  thumbnail?: string
  published_at?: string
  created_at: string
  updated_at: string
}) {
  const siteUrl = getSiteUrl()
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: post.thumbnail ? [absoluteUrl(post.thumbnail)] : undefined,
    url: `${siteUrl}/tin-tuc/${post.slug}`,
    datePublished: post.published_at || post.created_at,
    dateModified: post.updated_at,
    author: { '@type': 'Organization', name: ORG_NAME, url: siteUrl },
    publisher: {
      '@type': 'Organization',
      name: ORG_NAME,
      logo: { '@type': 'ImageObject', url: `${siteUrl}/logo.png` },
    },
  }
}

// ---------------------------------------------------------------------------
// Breadcrumb
// ---------------------------------------------------------------------------

export function buildBreadcrumbSchema(items: Array<{ name: string; url: string }>) {
  const siteUrl = getSiteUrl()
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: `${siteUrl}${item.url}`,
    })),
  }
}

// ---------------------------------------------------------------------------
// Local Business (for contact/about page)
// ---------------------------------------------------------------------------

export function buildLocalBusinessSchema() {
  const siteUrl = getSiteUrl()
  return {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    name: ORG_NAME,
    image: `${siteUrl}/logo.png`,
    url: siteUrl,
    telephone: ORG_PHONE,
    address: {
      '@type': 'PostalAddress',
      streetAddress: ORG_ADDRESS,
      addressCountry: 'VN',
    },
    geo: {
      '@type': 'GeoCoordinates',
      latitude: 21.0285,
      longitude: 105.7469,
    },
    priceRange: '$$',
    openingHours: 'Mo-Su 08:00-18:00',
  }
}

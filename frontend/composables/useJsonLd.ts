/**
 * useJsonLd — injects JSON-LD structured data into the page <head>.
 *
 * Usage:
 *   useJsonLd(buildProductSchema(product))
 *   useJsonLd(buildArticleSchema(post))
 *   useJsonLd(buildOrganizationSchema())
 */

type SchemaObject = Record<string, unknown>

const DEFAULT_SITE_URL = 'https://newnice.net'
const ORG_NAME = 'Newnice'
const ORG_PHONE = '+84869418104'
const ORG_EMAIL = 'newnicefilm@gmail.com'
const ORG_LOGO_PATH = '/logo.png'
const ORG_DESCRIPTION =
  'Newnice là thương hiệu cung cấp phim cách nhiệt ô tô, phim cách nhiệt nhà kính, PPF bảo vệ bề mặt và các giải pháp bảo vệ kính/bề mặt tại Việt Nam. Newnice tập trung vào sản phẩm rõ phân khúc, tư vấn đúng nhu cầu, thi công chỉn chu và chính sách bảo hành minh bạch.'
const FACEBOOK_URL = 'https://facebook.com/newnicevn'
const ZALO_URL = 'https://zalo.me/0869418104'
const GOOGLE_MAPS_URL = 'https://maps.app.goo.gl/fHQ8vCRVPCXhySnP9'
const ORG_ADDRESS = {
  streetAddress: '311 Phúc Diễn',
  addressLocality: 'Nam Từ Liêm',
  addressRegion: 'Hà Nội',
  addressCountry: 'VN',
}
const AREA_SERVED = [
  { '@type': 'AdministrativeArea', name: 'Hà Nội' },
  { '@type': 'Country', name: 'Việt Nam' },
]

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

function stripHtml(value?: string): string | undefined {
  const text = value
    ?.replace(/<[^>]*>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
  return text || undefined
}

function compactSchema<T>(value: T): T {
  if (Array.isArray(value)) {
    return value
      .map((item) => compactSchema(item))
      .filter((item) => {
        if (item === undefined || item === null || item === '') return false
        if (Array.isArray(item) && item.length === 0) return false
        if (typeof item === 'object' && Object.keys(item).length === 0) return false
        return true
      }) as T
  }

  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value as SchemaObject)
        .map(([key, item]) => [key, compactSchema(item)])
        .filter(([, item]) => {
          if (item === undefined || item === null || item === '') return false
          if (Array.isArray(item) && item.length === 0) return false
          if (typeof item === 'object' && Object.keys(item).length === 0) return false
          return true
        }),
    ) as T
  }

  return value
}

function parseVndAmount(value: unknown): number | undefined {
  const text = String(value ?? '').trim()
  if (!text) return undefined

  const candidates = text.match(/\d[\d.,\s]*/g) || []
  const amount = candidates
    .map((candidate) => candidate.replace(/\D/g, ''))
    .find((digits) => digits.length >= 4)

  return amount ? Number(amount) : undefined
}

function productImageUrls(product: {
  thumbnail?: string
  images?: Array<{ image_url?: string; thumbnail_url?: string }>
}) {
  const urls = [
    product.thumbnail,
    ...(product.images || []).flatMap((image) => [image.image_url, image.thumbnail_url]),
  ]
    .map((url) => absoluteUrl(url))
    .filter(Boolean) as string[]

  return [...new Set(urls)]
}

function organizationReference() {
  return {
    '@type': 'Organization',
    '@id': `${getSiteUrl()}/#organization`,
    name: ORG_NAME,
    url: getSiteUrl(),
  }
}

function postalAddress() {
  return {
    '@type': 'PostalAddress',
    ...ORG_ADDRESS,
  }
}

// ---------------------------------------------------------------------------
// Core inject helper
// ---------------------------------------------------------------------------

export function useJsonLd(schema: SchemaObject | SchemaObject[]) {
  const schemas = Array.isArray(schema) ? schema : [schema]
  useHead({
    script: schemas.map((s) => ({
      type: 'application/ld+json',
      innerHTML: JSON.stringify(compactSchema(s)),
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
    '@type': 'Organization',
    '@id': `${siteUrl}/#organization`,
    name: ORG_NAME,
    url: siteUrl,
    logo: {
      '@type': 'ImageObject',
      url: `${siteUrl}${ORG_LOGO_PATH}`,
    },
    description: ORG_DESCRIPTION,
    telephone: ORG_PHONE,
    email: ORG_EMAIL,
    address: postalAddress(),
    contactPoint: [
      {
        '@type': 'ContactPoint',
        telephone: ORG_PHONE,
        contactType: 'customer service',
        areaServed: 'VN',
        availableLanguage: ['vi'],
      },
    ],
    sameAs: [FACEBOOK_URL, ZALO_URL],
  }
}

// ---------------------------------------------------------------------------
// Product page
// ---------------------------------------------------------------------------

export function buildProductSchema(product: {
  name: string
  slug: string
  sku?: string
  film_code?: string
  short_description?: string
  description?: string
  meta_description?: string
  price_sedan?: string | number | null
  price_suv?: string | number | null
  is_contact_price?: boolean
  thumbnail?: string
  images?: Array<{ image_url?: string; thumbnail_url?: string }>
  brand?: { name: string }
  warranty_years?: number
}) {
  const siteUrl = getSiteUrl()
  const url = `${siteUrl}/san-pham/${product.slug}`
  const priceLines = [
    { label: 'Sedan', value: product.price_sedan },
    { label: 'SUV', value: product.price_suv },
  ]
    .map((price) => ({ ...price, amount: parseVndAmount(price.value) }))
    .filter((price): price is { label: string; value: string | number; amount: number } => Boolean(price.amount))
  const amounts = priceLines.map((price) => price.amount)
  const offers =
    amounts.length > 1
      ? {
          '@type': 'AggregateOffer',
          url,
          priceCurrency: 'VND',
          lowPrice: Math.min(...amounts),
          highPrice: Math.max(...amounts),
          offerCount: amounts.length,
          availability: 'https://schema.org/InStock',
          seller: organizationReference(),
          offers: priceLines.map((price) => ({
            '@type': 'Offer',
            name: price.label,
            url,
            priceCurrency: 'VND',
            price: price.amount,
            availability: 'https://schema.org/InStock',
            seller: organizationReference(),
          })),
        }
      : amounts.length === 1
        ? {
            '@type': 'Offer',
            url,
            priceCurrency: 'VND',
            price: amounts[0],
            availability: 'https://schema.org/InStock',
            seller: organizationReference(),
          }
        : {
            '@type': 'Offer',
            name: product.is_contact_price ? 'Liên hệ báo giá' : undefined,
            url,
            availability: 'https://schema.org/InStock',
            seller: organizationReference(),
          }

  const schema: SchemaObject = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    url,
    sku: product.sku,
    mpn: product.film_code,
    description: stripHtml(product.short_description || product.meta_description || product.description),
    image: productImageUrls(product),
    brand: product.brand
      ? { '@type': 'Brand', name: product.brand.name }
      : undefined,
    manufacturer: organizationReference(),
    offers,
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
      logo: { '@type': 'ImageObject', url: `${siteUrl}${ORG_LOGO_PATH}` },
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
      item: absoluteUrl(item.url) || `${siteUrl}${item.url}`,
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
    '@id': `${siteUrl}/#localbusiness`,
    name: ORG_NAME,
    image: `${siteUrl}${ORG_LOGO_PATH}`,
    url: siteUrl,
    telephone: ORG_PHONE,
    email: ORG_EMAIL,
    description: ORG_DESCRIPTION,
    address: postalAddress(),
    geo: {
      '@type': 'GeoCoordinates',
      latitude: 21.0285,
      longitude: 105.7469,
    },
    hasMap: GOOGLE_MAPS_URL,
    areaServed: AREA_SERVED,
    sameAs: [FACEBOOK_URL, ZALO_URL],
    branchOf: organizationReference(),
  }
}

// ---------------------------------------------------------------------------
// Service pages
// ---------------------------------------------------------------------------

const SERVICE_SCHEMAS: Record<string, { name: string; description: string; serviceType: string }> = {
  'phim-cach-nhiet-newnice': {
    name: 'Dán phim cách nhiệt ô tô',
    serviceType: 'Auto window tinting service',
    description:
      'Dịch vụ tư vấn và thi công phim cách nhiệt ô tô, hỗ trợ giảm nóng, chống tia UV, tăng sự thoải mái khi lái xe và bảo vệ nội thất.',
  },
  'phim-cach-nhiet-o-to': {
    name: 'Dán phim cách nhiệt ô tô',
    serviceType: 'Auto window tinting service',
    description:
      'Dịch vụ tư vấn và thi công phim cách nhiệt ô tô, hỗ trợ giảm nóng, chống tia UV, tăng sự thoải mái khi lái xe và bảo vệ nội thất.',
  },
  'film-cach-nhiet-nha-kinh': {
    name: 'Dán phim cách nhiệt nhà kính',
    serviceType: 'Window tinting service',
    description:
      'Dịch vụ dán phim cách nhiệt cho nhà ở, văn phòng, showroom và công trình kính, giúp giảm nóng, giảm chói và hỗ trợ tiết kiệm điện điều hòa.',
  },
  'phim-cach-nhiet-nha-kinh': {
    name: 'Dán phim cách nhiệt nhà kính',
    serviceType: 'Window tinting service',
    description:
      'Dịch vụ dán phim cách nhiệt cho nhà ở, văn phòng, showroom và công trình kính, giúp giảm nóng, giảm chói và hỗ trợ tiết kiệm điện điều hòa.',
  },
  'ppf-newnice': {
    name: 'Dán PPF bảo vệ bề mặt',
    serviceType: 'Paint protection film installation',
    description:
      'Dịch vụ dán PPF trong suốt giúp bảo vệ sơn xe, bề mặt nội thất, mặt bếp đá và các khu vực dễ trầy xước trong quá trình sử dụng.',
  },
  'phim-ppf': {
    name: 'Dán PPF bảo vệ bề mặt',
    serviceType: 'Paint protection film installation',
    description:
      'Dịch vụ dán PPF trong suốt giúp bảo vệ sơn xe, bề mặt nội thất, mặt bếp đá và các khu vực dễ trầy xước trong quá trình sử dụng.',
  },
  'phim-doi-mau-xe': {
    name: 'Dán phim đổi màu xe',
    serviceType: 'Vehicle wrap service',
    description:
      'Dịch vụ dán film đổi màu xe giúp thay đổi diện mạo xe theo phong cách riêng, đồng thời hỗ trợ bảo vệ bề mặt sơn zin.',
  },
}

export function buildServiceSchemaForCategorySlug(slug: string, path: string) {
  const service = SERVICE_SCHEMAS[slug]
  if (!service) return undefined

  const url = absoluteUrl(path)
  return {
    '@context': 'https://schema.org',
    '@type': 'Service',
    name: service.name,
    description: service.description,
    serviceType: service.serviceType,
    provider: organizationReference(),
    areaServed: AREA_SERVED,
    url,
  }
}

// ---------------------------------------------------------------------------
// FAQ
// ---------------------------------------------------------------------------

export function buildFAQPageSchema(items: Array<{ question: string; answer: string }>) {
  const mainEntity = items
    .map((item) => ({
      '@type': 'Question',
      name: stripHtml(item.question),
      acceptedAnswer: {
        '@type': 'Answer',
        text: stripHtml(item.answer),
      },
    }))
    .filter((item) => item.name && item.acceptedAnswer.text)

  if (!mainEntity.length) return undefined

  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity,
  }
}

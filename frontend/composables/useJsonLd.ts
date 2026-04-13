/**
 * useJsonLd — injects JSON-LD structured data into the page <head>.
 *
 * Usage:
 *   useJsonLd(buildProductSchema(product))
 *   useJsonLd(buildArticleSchema(post))
 *   useJsonLd(buildOrganizationSchema())
 */

const SITE_URL = 'https://newnice.vn'
const ORG_NAME = 'Newnice'
const ORG_PHONE = '+84901234567'
const ORG_ADDRESS = '123 Nguyễn Văn Linh, Quận 7, Thành phố Hồ Chí Minh, Việt Nam'

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
  return {
    '@context': 'https://schema.org',
    '@type': 'AutoRepair',  // More specific than Organization for a car service biz
    name: ORG_NAME,
    url: SITE_URL,
    logo: `${SITE_URL}/logo.png`,
    telephone: ORG_PHONE,
    address: {
      '@type': 'PostalAddress',
      streetAddress: '123 Nguyễn Văn Linh',
      addressLocality: 'Quận 7',
      addressRegion: 'Thành phố Hồ Chí Minh',
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
      'https://www.facebook.com/newnice.vn',
      'https://zalo.me/newnice',
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
  price?: number
  is_contact_price?: boolean
  thumbnail?: string
  brand?: { name: string }
  warranty_years?: number
}) {
  const url = `${SITE_URL}/san-pham/${product.slug}`
  const schema: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    url,
    description: product.short_description,
    image: product.thumbnail ? [product.thumbnail] : undefined,
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
      ...(product.is_contact_price || !product.price
        ? { price: '0', priceSpecification: { '@type': 'UnitPriceSpecification', name: 'Liên hệ báo giá' } }
        : { price: String(product.price) }),
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
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: post.thumbnail ? [post.thumbnail] : undefined,
    url: `${SITE_URL}/tin-tuc/${post.slug}`,
    datePublished: post.published_at || post.created_at,
    dateModified: post.updated_at,
    author: { '@type': 'Organization', name: ORG_NAME, url: SITE_URL },
    publisher: {
      '@type': 'Organization',
      name: ORG_NAME,
      logo: { '@type': 'ImageObject', url: `${SITE_URL}/logo.png` },
    },
  }
}

// ---------------------------------------------------------------------------
// Breadcrumb
// ---------------------------------------------------------------------------

export function buildBreadcrumbSchema(items: Array<{ name: string; url: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: `${SITE_URL}${item.url}`,
    })),
  }
}

// ---------------------------------------------------------------------------
// Local Business (for contact/about page)
// ---------------------------------------------------------------------------

export function buildLocalBusinessSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    name: ORG_NAME,
    image: `${SITE_URL}/logo.png`,
    url: SITE_URL,
    telephone: ORG_PHONE,
    address: {
      '@type': 'PostalAddress',
      streetAddress: ORG_ADDRESS,
      addressCountry: 'VN',
    },
    geo: {
      '@type': 'GeoCoordinates',
      latitude: 10.73,
      longitude: 106.7,
    },
    priceRange: '$$',
    openingHours: 'Mo-Su 08:00-18:00',
  }
}

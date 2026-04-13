# Implementation Plan: SEO & Performance Optimization

## Overview

Wire the existing SEO composables and analytics plugin into all remaining pages, build the `OptimizedImage.vue` component, add the `useCanonical` and `usePhoneTracking` composables, extend the image upload service with size metadata, surface optimization stats in the admin UI, create `robots.txt`, and add property-based tests for all correctness properties.

## Tasks

- [x] 1. Extend backend image service with size metadata
  - [x] 1.1 Add `original_size_bytes` and `webp_size_bytes` to `save_upload()` response
    - In `backend/app/services/image_service.py`, after writing the original file set `result["original_size_bytes"] = len(content)`
    - After `convert_to_webp` on the root image set `result["webp_size_bytes"] = webp_path.stat().st_size`
    - Both fields should only be set when `generate_variants=True`
    - _Requirements: FR-3 (admin upload feedback)_
  - [x] 1.2 Add `original_size_bytes` and `webp_size_bytes` optional fields to `ImageData` interface in `frontend/components/admin/ImageUpload.vue`
    - Extend the local `ImageData` interface with `original_size_bytes?: number` and `webp_size_bytes?: number`
    - _Requirements: FR-3_

- [x] 2. Create `useCanonical` composable
  - [x] 2.1 Create `frontend/composables/useCanonical.ts`
    - Read `config.public.siteUrl` (strip trailing slash), call `useHead({ link: [{ rel: 'canonical', href: \`\${siteUrl}\${path}\` }] })`
    - Export a single `useCanonical(path: string)` function
    - _Requirements: NFR-2 (canonical URLs)_
  - [ ]* 2.2 Write property test for `useCanonical` absolute URL format
    - **Property 4: Canonical URL is always an absolute URL containing the path**
    - Generate random path strings starting with `/`; assert injected `href` starts with `https://` and ends with the exact path
    - Tag: `// Feature: seo-performance-optimization, Property 4: useCanonical absolute URL`
    - **Validates: Requirements NFR-2**

- [x] 3. Create `usePhoneTracking` composable
  - [x] 3.1 Create `frontend/composables/usePhoneTracking.ts`
    - Use `useNuxtApp().$gtag` to fire `phone_click` event with `{ phone_number }` parameter
    - Export `usePhoneTracking()` returning `{ trackPhoneClick(phoneNumber: string): void }`
    - Guard the call with `typeof window !== 'undefined'` consistent with the analytics plugin
    - _Requirements: FR-4 (phone click tracking)_

- [x] 4. Create `OptimizedImage.vue` component
  - [x] 4.1 Create `frontend/components/common/OptimizedImage.vue`
    - Props: `src` (required), `srcset` (default `''`), `sizes` (default `'100vw'`), `alt` (required), `loading` (default `'lazy'`), `class` (default `''`), `width`, `height`
    - Render `<picture>` with a `<source type="image/webp" :srcset :sizes>` (only when `srcset` is non-empty) and a fallback `<img>`
    - Forward `width`, `height`, `loading`, `class` to the `<img>` element to prevent CLS
    - _Requirements: FR-3 (responsive images, WebP delivery)_

- [x] 5. Create `frontend/public/robots.txt`
  - [x] 5.1 Write the static `robots.txt` file
    - Content: `User-agent: *`, `Allow: /`, `Disallow: /admin/`, `Disallow: /api/`, `Sitemap: https://newnice.vn/sitemap.xml`
    - File path: `frontend/public/robots.txt` (served at `/robots.txt` by Nuxt)
    - _Requirements: FR-1 (sitemap pointer), NFR-2_

- [ ] 6. Checkpoint — ensure backend and new composables are wired correctly
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Wire JSON-LD, canonical, and seoMeta on remaining pages
  - [x] 7.1 Update `frontend/pages/index.vue`
    - Add `useJsonLd(buildOrganizationSchema())` and `useCanonical('/')` in `<script setup>`
    - Import `buildOrganizationSchema` from `~/composables/useJsonLd` and `useCanonical` from `~/composables/useCanonical`
    - _Requirements: FR-2 (organization structured data), NFR-2_
  - [x] 7.2 Update `frontend/pages/gioi-thieu.vue`
    - Add `buildOrganizationSchema()` via `useJsonLd`, `useCanonical('/gioi-thieu')`, and `useSeoMeta` with Vietnamese title/description if not already present
    - _Requirements: FR-2, NFR-2_
  - [x] 7.3 Update `frontend/pages/lien-he.vue`
    - Add `useJsonLd(buildLocalBusinessSchema())`, `useCanonical('/lien-he')`, and `useSeoMeta` with title `Liên hệ Newnice — Tư vấn phim cách nhiệt ô tô tại TP.HCM` and matching description
    - _Requirements: FR-2 (LocalBusiness schema), NFR-2_
  - [x] 7.4 Update `frontend/pages/bao-gia.vue`
    - Add `useCanonical('/bao-gia')` and `useSeoMeta` with title `Báo giá phim cách nhiệt ô tô — Newnice` and matching description
    - _Requirements: NFR-2_
  - [x] 7.5 Update `frontend/pages/danh-muc/[slug].vue`
    - Add `buildBreadcrumbSchema([{ name: 'Trang chủ', url: '/' }, { name: 'Sản phẩm', url: '/san-pham' }, { name: category.value.name, url: \`/danh-muc/\${category.value.slug}\` }])` via `useJsonLd` (guard with `if (category.value)`)
    - Add `useCanonical(route.path)` and `useSeoMeta` using category `meta_title` / `meta_description` with fallbacks
    - _Requirements: FR-2 (breadcrumb schema), NFR-2_
  - [x] 7.6 Update `frontend/pages/san-pham/index.vue`
    - Add `useJsonLd(buildBreadcrumbSchema([{ name: 'Trang chủ', url: '/' }, { name: 'Sản phẩm', url: '/san-pham' }]))` and `useCanonical('/san-pham')`
    - Add `useSeoMeta` with a descriptive Vietnamese title and description for the products listing page
    - _Requirements: FR-2, NFR-2_
  - [x] 7.7 Update `frontend/pages/tin-tuc/index.vue`
    - Add `useJsonLd(buildBreadcrumbSchema([{ name: 'Trang chủ', url: '/' }, { name: 'Tin tức', url: '/tin-tuc' }]))` and `useCanonical('/tin-tuc')`
    - Add `useSeoMeta` with a descriptive Vietnamese title and description for the blog listing page
    - _Requirements: FR-2, NFR-2_

- [x] 8. Wire GA4 conversion events
  - [x] 8.1 Add `view_item` event to `frontend/pages/san-pham/[slug].vue`
    - In `onMounted`, call `$gtag('event', 'view_item', { item_id: String(product.value.id), item_name: product.value.name, item_category: product.value.category?.name, item_brand: product.value.brand?.name })` guarded by `if (product.value)`
    - Use `const { $gtag } = useNuxtApp()`
    - _Requirements: FR-4 (product view tracking)_
  - [x] 8.2 Add `generate_lead` event to `frontend/components/forms/QuoteForm.vue`
    - After a successful form submit (API returns success), call `$gtag('event', 'generate_lead', { form_type: 'quote' })`
    - _Requirements: FR-4 (quote request tracking)_
  - [x] 8.3 Add `contact` event to `frontend/components/forms/ContactForm.vue`
    - After a successful form submit, call `$gtag('event', 'contact', { form_type: 'contact' })`
    - _Requirements: FR-4 (contact form tracking)_
  - [x] 8.4 Wire `usePhoneTracking` on `tel:` links in `frontend/pages/san-pham/[slug].vue`
    - Replace the bare `<a href="tel:...">` with a click handler that calls `trackPhoneClick('0901234567')` before navigating
    - Import `usePhoneTracking` and destructure `trackPhoneClick`
    - _Requirements: FR-4 (phone click tracking)_
  - [x] 8.5 Wire `usePhoneTracking` on `tel:` links in `frontend/pages/index.vue`
    - Add click handler on the `<a href="tel:...">` CTA that calls `trackPhoneClick`
    - _Requirements: FR-4_

- [ ]* 8.6 Write property test for `view_item` GA4 payload correctness
  - **Property 7: view_item event payload matches product data**
  - Generate random product objects; mock `$gtag`; assert `item_id === String(product.id)` and `item_name === product.name`
  - Tag: `// Feature: seo-performance-optimization, Property 7: view_item payload`
  - **Validates: Requirements FR-4**

- [x] 9. Extend `ImageUpload.vue` with optimization stats panel
  - [x] 9.1 Add optimization stats display to `frontend/components/admin/ImageUpload.vue`
    - Add a reactive `uploadStats` ref typed as `{ original_size_bytes: number; webp_size_bytes: number } | null`
    - In the `uploaded` event handler, populate `uploadStats` from `imageData.original_size_bytes` and `imageData.webp_size_bytes`
    - Render a stats panel below the preview (only when `uploadStats` is non-null and both fields are present): show original size in MB, WebP size in KB, and reduction percentage computed as `Math.round((1 - webp / original) * 100)`
    - Clear `uploadStats` when `removeImage()` is called
    - _Requirements: FR-3 (admin upload feedback)_
  - [ ]* 9.2 Write property test for upload reduction percentage math
    - **Property 6: Upload optimization reduction percentage is correct**
    - Generate pairs `(original_size_bytes, webp_size_bytes)` where both are positive integers and `webp <= original`; assert displayed percentage equals `Math.round((1 - webp / original) * 100)` and is in `[0, 100]`
    - Tag: `// Feature: seo-performance-optimization, Property 6: upload reduction percentage`
    - **Validates: Requirements FR-3**

- [ ] 10. Write property-based tests for JSON-LD builder functions
  - [ ]* 10.1 Write property test for `buildProductSchema` completeness
    - **Property 1: Product schema contains required fields**
    - Use fast-check to generate arbitrary product objects (random names, slugs, optional price/brand/warranty); assert `@type === 'Product'`, `name` is non-empty, `url` contains the slug, `offers.priceCurrency === 'VND'`, `offers.availability` is a valid URL
    - Tag: `// Feature: seo-performance-optimization, Property 1: buildProductSchema completeness`
    - **Validates: Requirements FR-2**
  - [ ]* 10.2 Write property test for `buildArticleSchema` completeness
    - **Property 2: Article schema contains required fields**
    - Generate arbitrary post objects (random titles, slugs, ISO date strings); assert `@type === 'Article'`, `headline` is non-empty, `datePublished` is present, `author['@type'] === 'Organization'`
    - Tag: `// Feature: seo-performance-optimization, Property 2: buildArticleSchema completeness`
    - **Validates: Requirements FR-2**
  - [ ]* 10.3 Write property test for `buildBreadcrumbSchema` sequential positions
    - **Property 3: Breadcrumb positions are sequential and complete**
    - Generate arrays of 1–10 items with random names and `/`-prefixed URL paths; assert `itemListElement.length === input.length`, positions are `[1, 2, ..., n]`, and each `item` contains the corresponding input URL
    - Tag: `// Feature: seo-performance-optimization, Property 3: buildBreadcrumbSchema sequential positions`
    - **Validates: Requirements FR-2**

- [x] 11. Final checkpoint — ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Property tests use [fast-check](https://fast-check.io/) with Vitest (`fc.assert(fc.property(...), { numRuns: 100 })`)
- `useCanonical` reads `config.public.siteUrl` — ensure `NUXT_PUBLIC_SITE_URL=https://newnice.vn` is set in production
- All JSON-LD calls on dynamic pages are guarded with `if (data.value)` to match the existing pattern in `san-pham/[slug].vue` and `tin-tuc/[slug].vue`
- `$gtag` calls are client-side only; guard with `if (import.meta.client)` or inside `onMounted` to avoid SSR errors

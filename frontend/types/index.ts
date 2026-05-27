// Product types
export interface Product {
  id: number
  name: string
  slug: string
  sku?: string
  film_code?: string
  short_description?: string
  description?: string
  price_sedan?: string
  price_suv?: string
  is_contact_price: boolean
  thumbnail?: string
  vlt?: number
  uv_rejection?: number
  ir_rejection?: number
  heat_rejection?: number
  thickness?: string
  warranty_years?: number
  is_featured: boolean
  is_active: boolean
  meta_title?: string
  meta_description?: string
  created_at: string
  updated_at: string
  category?: Category
  brand?: Brand
  images?: ProductImage[]
}

export interface ProductImage {
  id: number
  image_url: string
  thumbnail_url?: string
  alt_text?: string
  sort_order: number
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
  image?: string
  banner_image?: string
  parent_id?: number
  sort_order: number
  is_active: boolean
  meta_title?: string
  meta_description?: string
  created_at: string
  updated_at: string
  children?: Category[]
}

export interface Brand {
  id: number
  name: string
  slug: string
  logo?: string
  description?: string
  country?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

// API response types
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface MessageResponse {
  message: string
  success: boolean
}

// Quote types
export interface QuoteRequest {
  customer_name: string
  phone: string
  email?: string
  car_brand?: string
  car_model?: string
  car_year?: number
  film_type_preference?: string
  service_type?: string
  message?: string
}

export interface Contact {
  name: string
  phone?: string
  email: string
  subject?: string
  message: string
}

// Post/Blog types
export interface Post {
  id: number
  title: string
  slug: string
  excerpt?: string
  content?: string
  thumbnail?: string
  is_published: boolean
  published_at?: string
  meta_title?: string
  meta_description?: string
  created_at: string
  updated_at: string
}

export interface PostList {
  id: number
  title: string
  slug: string
  excerpt?: string
  thumbnail?: string
  published_at?: string
  created_at: string
}

import type { Product, PaginatedResponse } from '~/types'

export const useProducts = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  const getProducts = async (params?: {
    page?: number
    page_size?: number
    category_slug?: string
    brand_slug?: string
    film_type?: string
    is_featured?: boolean
    search?: string
  }) => {
    const query = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          query.append(key, String(value))
        }
      })
    }
    
    const { data, error } = await useFetch<PaginatedResponse<Product>>(
      `${apiBase}/products?${query.toString()}`
    )
    
    if (error.value) {
      throw new Error(error.value.message)
    }
    
    return data.value
  }

  const getFeaturedProducts = async (limit = 8) => {
    const { data, error } = await useFetch<Product[]>(
      `${apiBase}/products/featured?limit=${limit}`
    )
    
    if (error.value) {
      throw new Error(error.value.message)
    }
    
    return data.value
  }

  const getProduct = async (slug: string) => {
    const { data, error } = await useFetch<Product>(
      `${apiBase}/products/${slug}`
    )
    
    if (error.value) {
      throw new Error(error.value.message)
    }
    
    return data.value
  }

  return {
    getProducts,
    getFeaturedProducts,
    getProduct,
  }
}

import type { Category } from '~/types'

export const useCategories = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  const getCategories = async () => {
    const { data, error } = await useFetch<Category[]>(`${apiBase}/categories`)
    
    if (error.value) {
      throw new Error(error.value.message)
    }
    
    return data.value
  }

  const getCategory = async (slug: string) => {
    const { data, error } = await useFetch<Category>(`${apiBase}/categories/${slug}`)
    
    if (error.value) {
      throw new Error(error.value.message)
    }
    
    return data.value
  }

  return {
    getCategories,
    getCategory,
  }
}

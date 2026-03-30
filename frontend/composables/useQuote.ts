import type { QuoteRequest, Contact, MessageResponse } from '~/types'

export const useQuote = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase
  
  const isSubmitting = ref(false)
  const error = ref<string | null>(null)

  const submitQuote = async (data: QuoteRequest): Promise<boolean> => {
    isSubmitting.value = true
    error.value = null
    
    try {
      const response = await $fetch<QuoteRequest>(`${apiBase}/quotes`, {
        method: 'POST',
        body: data,
      })
      return true
    } catch (e: any) {
      error.value = e.data?.detail || 'Có lỗi xảy ra. Vui lòng thử lại.'
      return false
    } finally {
      isSubmitting.value = false
    }
  }

  const submitContact = async (data: Contact): Promise<MessageResponse | null> => {
    isSubmitting.value = true
    error.value = null
    
    try {
      const response = await $fetch<MessageResponse>(`${apiBase}/contact`, {
        method: 'POST',
        body: data,
      })
      return response
    } catch (e: any) {
      error.value = e.data?.detail || 'Có lỗi xảy ra. Vui lòng thử lại.'
      return null
    } finally {
      isSubmitting.value = false
    }
  }

  return {
    isSubmitting: readonly(isSubmitting),
    error: readonly(error),
    submitQuote,
    submitContact,
  }
}

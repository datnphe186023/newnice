/**
 * Composable for tracking phone number clicks via GA4.
 * Fires a `phone_click` event with the dialed number as a parameter.
 */
export function usePhoneTracking() {
  const { $gtag } = useNuxtApp()

  return {
    trackPhoneClick(phoneNumber: string): void {
      if (typeof window !== 'undefined' && typeof $gtag === 'function') {
        $gtag('event', 'phone_click', { phone_number: phoneNumber })
      }
    },
  }
}

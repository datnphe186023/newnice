<template>
  <div class="min-h-screen bg-zinc-950 text-white">
    <main class="mx-auto flex min-h-screen w-full max-w-3xl flex-col px-4 py-6 sm:px-6">
      <header class="flex items-center justify-between border-b border-white/10 pb-5">
        <img src="/logo.png" alt="Newnice" class="h-10 w-auto" />
        <span class="rounded-full border border-white/15 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-zinc-300">
          Bảo hành
        </span>
      </header>

      <section class="flex flex-1 flex-col justify-center py-8">
        <div v-if="pending" class="rounded-lg border border-white/10 bg-white/[0.03] p-6">
          <div class="h-4 w-36 animate-pulse rounded bg-white/10" />
          <div class="mt-6 h-10 w-3/4 animate-pulse rounded bg-white/10" />
          <div class="mt-3 h-4 w-full animate-pulse rounded bg-white/10" />
        </div>

        <div v-else-if="loadError" class="rounded-lg border border-red-400/30 bg-red-500/10 p-6">
          <p class="text-sm font-semibold uppercase tracking-wide text-red-200">Serial không hợp lệ</p>
          <h1 class="mt-3 text-2xl font-bold">Không tìm thấy tem bảo hành</h1>
          <p class="mt-3 text-zinc-300">Vui lòng kiểm tra lại QR hoặc liên hệ hotline hỗ trợ.</p>
          <a href="tel:0869418104" class="mt-6 inline-flex w-full items-center justify-center rounded-lg bg-white px-4 py-3 font-semibold text-zinc-950 sm:w-auto">
            Gọi hotline
          </a>
        </div>

        <div v-else-if="lookup?.status === 'activated' && lookup.warranty" class="space-y-5">
          <div class="rounded-lg border border-emerald-400/30 bg-emerald-500/10 p-6">
            <div class="flex items-center gap-3">
              <span class="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-400 text-zinc-950">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
              </span>
              <div>
                <p class="text-sm font-semibold uppercase tracking-wide text-emerald-100">Bảo hành chính hãng</p>
                <h1 class="text-2xl font-bold">Đã kích hoạt</h1>
              </div>
            </div>
            <p class="mt-5 text-sm text-zinc-300">Serial: {{ lookup.serial }}</p>
          </div>

          <div class="rounded-lg border border-white/10 bg-white p-5 text-zinc-950 shadow-2xl">
            <dl class="grid gap-4">
              <div v-for="item in warrantyRows" :key="item.label" class="border-b border-zinc-100 pb-4 last:border-0 last:pb-0">
                <dt class="text-xs font-semibold uppercase tracking-wide text-zinc-500">{{ item.label }}</dt>
                <dd class="mt-1 text-base font-semibold text-zinc-950">{{ item.value }}</dd>
              </div>
            </dl>
          </div>

          <div class="rounded-lg border border-white/10 bg-white p-5 text-zinc-950 shadow-2xl">
            <div class="flex flex-col gap-5 sm:flex-row sm:items-center">
              <div class="mx-auto flex h-44 w-44 flex-shrink-0 items-center justify-center rounded-lg border border-zinc-200 bg-white p-3 sm:mx-0">
                <img :src="qrPreviewSrc" :alt="`QR thông tin bảo hành ${lookup.serial}`" class="h-full w-full" />
              </div>
              <div class="min-w-0 flex-1">
                <p class="text-xs font-semibold uppercase tracking-wide text-zinc-500">QR thông tin bảo hành</p>
                <h2 class="mt-1 text-xl font-bold text-zinc-950">Tải ảnh QR cho khách hàng</h2>
                <p class="mt-2 break-all text-sm text-zinc-600">{{ warrantyInfoUrl }}</p>
                <button
                  type="button"
                  class="mt-4 inline-flex w-full items-center justify-center rounded-lg bg-zinc-950 px-4 py-3 font-semibold text-white transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
                  :disabled="!qrPngUrl"
                  @click="downloadWarrantyQr"
                >
                  Tải ảnh QR
                </button>
                <p v-if="qrError" class="mt-3 text-sm font-medium text-red-600">{{ qrError }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <a href="tel:0869418104" class="rounded-lg bg-white px-4 py-3 text-center font-semibold text-zinc-950">
              Hotline
            </a>
            <a href="https://zalo.me/0869418104" target="_blank" class="rounded-lg border border-white/20 px-4 py-3 text-center font-semibold text-white">
              Zalo
            </a>
          </div>
        </div>

        <div v-else-if="lookup?.status === 'unused'" class="space-y-5">
          <div class="rounded-lg border border-amber-300/30 bg-amber-300/10 p-6">
            <p class="text-sm font-semibold uppercase tracking-wide text-amber-100">Serial: {{ lookup.serial }}</p>
            <h1 class="mt-3 text-2xl font-bold">Bảo hành chưa được kích hoạt</h1>
          </div>

          <form class="rounded-lg border border-white/10 bg-white p-5 text-zinc-950 shadow-2xl" @submit.prevent="activate">
            <div class="grid gap-4">
              <div>
                <label class="label-dark" for="vehicle_plate">Biển số xe</label>
                <input id="vehicle_plate" v-model="form.vehicle_plate" required class="input-dark uppercase" autocomplete="off" />
              </div>

              <div>
                <label class="label-dark" for="vehicle_model">Mẫu xe</label>
                <input id="vehicle_model" v-model="form.vehicle_model" required class="input-dark" autocomplete="off" />
              </div>

              <div class="grid gap-4 sm:grid-cols-2">
                <div>
                  <label class="label-dark" for="customer_name">Tên khách hàng</label>
                  <input id="customer_name" v-model="form.customer_name" required class="input-dark" autocomplete="name" />
                </div>
                <div>
                  <label class="label-dark" for="customer_phone">SĐT khách hàng</label>
                  <input id="customer_phone" v-model="form.customer_phone" required class="input-dark" inputmode="tel" autocomplete="tel" />
                </div>
              </div>

              <div>
                <label class="label-dark" for="film_package_id">Gói film dán</label>
                <select id="film_package_id" v-model="form.film_package_id" required class="input-dark">
                  <option value="" disabled>Chọn gói film</option>
                  <option v-for="pkg in lookup.film_packages" :key="pkg.id" :value="pkg.id">
                    {{ pkg.package_name }} - {{ Math.round(pkg.warranty_duration_months / 12) }} năm
                  </option>
                </select>
              </div>

              <div class="grid gap-4 sm:grid-cols-3">
                <div>
                  <label class="label-dark" for="front">Mã film kính lái</label>
                  <input id="front" v-model="form.front_windshield_film_code" required class="input-dark" autocomplete="off" />
                </div>
                <div>
                  <label class="label-dark" for="rear">Mã film kính hậu</label>
                  <input id="rear" v-model="form.rear_windshield_film_code" required class="input-dark" autocomplete="off" />
                </div>
                <div>
                  <label class="label-dark" for="side">Mã film kính sườn</label>
                  <input id="side" v-model="form.side_window_film_code" required class="input-dark" autocomplete="off" />
                </div>
              </div>

              <div class="grid gap-4 sm:grid-cols-2">
                <div>
                  <label class="label-dark" for="install_date">Ngày dán</label>
                  <input id="install_date" v-model="form.install_date" required type="date" class="input-dark" />
                </div>
                <div>
                  <label class="label-dark" for="activation_code">Mã kích hoạt đại lý</label>
                  <input id="activation_code" v-model="form.activation_code" required class="input-dark" autocomplete="off" />
                </div>
              </div>
            </div>

            <p v-if="submitError" class="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
              {{ submitError }}
            </p>

            <button type="submit" :disabled="submitting" class="mt-5 flex w-full items-center justify-center rounded-lg bg-zinc-950 px-4 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60">
              {{ submitting ? 'Đang kích hoạt...' : 'Kích hoạt bảo hành' }}
            </button>
          </form>
        </div>

        <div v-else class="rounded-lg border border-white/10 bg-white/[0.03] p-6">
          <p class="text-sm font-semibold uppercase tracking-wide text-zinc-300">Serial: {{ lookup?.serial }}</p>
          <h1 class="mt-3 text-2xl font-bold">Tem không khả dụng</h1>
          <p class="mt-3 text-zinc-300">Trạng thái hiện tại: {{ statusLabel(lookup?.status) }}</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { encode, renderSVG } from 'uqr'

definePageMeta({
  layout: false,
})

interface FilmPackage {
  id: string
  package_name: string
  warranty_duration_months: number
  status: string
}

interface WarrantyInfo {
  customer_name: string
  customer_phone: string
  vehicle_plate: string
  vehicle_model: string
  film_package: string
  install_date: string
  warranty_expiry: string
}

interface WarrantyLookup {
  serial: string
  status: string
  warranty?: WarrantyInfo
  film_packages: FilmPackage[]
}

const route = useRoute()
const config = useRuntimeConfig()
const serial = computed(() => String(route.params.serial || '').toUpperCase())

useSeoMeta({
  title: () => `Bảo hành ${serial.value} | Newnice`,
  robots: 'noindex, nofollow',
})

const today = new Date().toISOString().slice(0, 10)
const submitting = ref(false)
const submitError = ref('')
const loadError = ref(false)
const lookup = ref<WarrantyLookup | null>(null)
const qrPngUrl = ref('')
const qrError = ref('')

const form = reactive({
  vehicle_plate: '',
  vehicle_model: '',
  customer_phone: '',
  customer_name: '',
  film_package_id: '',
  front_windshield_film_code: '',
  rear_windshield_film_code: '',
  side_window_film_code: '',
  install_date: today,
  activation_code: '',
})

const syncLookup = (data: WarrantyLookup | null | undefined) => {
  lookup.value = data || null
  loadError.value = !data

  if (data?.status === 'unused' && data.film_packages.length && !form.film_package_id) {
    form.film_package_id = data.film_packages[0].id
  }
}

const { data: lookupData, pending, refresh } = await useAsyncData<WarrantyLookup | null>(
  `warranty-${serial.value}`,
  async () => {
    try {
      return await $fetch<WarrantyLookup>(`${config.public.apiBase}/warranties/${serial.value}`)
    } catch (err) {
      return null
    }
  },
)

watch(lookupData, syncLookup, { immediate: true })

const warrantyRows = computed(() => {
  if (!lookup.value?.warranty) return []
  const warranty = lookup.value.warranty
  return [
    { label: 'Tên khách hàng', value: warranty.customer_name },
    { label: 'SĐT khách hàng', value: warranty.customer_phone },
    { label: 'Biển số xe', value: warranty.vehicle_plate },
    { label: 'Mẫu xe', value: warranty.vehicle_model },
    { label: 'Gói film dán', value: warranty.film_package },
    { label: 'Ngày dán', value: formatDate(warranty.install_date) },
    { label: 'Hạn bảo hành', value: formatDate(warranty.warranty_expiry) },
  ]
})

const siteUrl = computed(() => {
  const configuredUrl = String(config.public.siteUrl || '').replace(/\/$/, '')
  if (configuredUrl) return configuredUrl
  if (process.client) return window.location.origin
  return 'https://newnice.net'
})

const warrantyInfoUrl = computed(() => `${siteUrl.value}/w/${encodeURIComponent(serial.value)}`)

const qrSvg = computed(() =>
  renderSVG(warrantyInfoUrl.value, {
    ecc: 'M',
    border: 2,
    pixelSize: 10,
    blackColor: '#09090b',
    whiteColor: '#ffffff',
  }),
)

const qrPreviewSrc = computed(() => `data:image/svg+xml;charset=utf-8,${encodeURIComponent(qrSvg.value)}`)

const activate = async () => {
  submitError.value = ''
  submitting.value = true

  try {
    lookup.value = await $fetch<WarrantyLookup>(`${config.public.apiBase}/warranties/${serial.value}/activate`, {
      method: 'POST',
      body: form,
    })
    await refresh()
    await generateWarrantyQrImage()
  } catch (err: any) {
    submitError.value = warrantyErrorMessage(err)
  } finally {
    submitting.value = false
  }
}

const warrantyErrorMessage = (err: any) => {
  const detail = err?.data?.detail
  const fallback = 'Không thể kích hoạt bảo hành. Vui lòng kiểm tra lại thông tin.'

  if (Array.isArray(detail)) {
    return 'Thông tin nhập chưa hợp lệ. Vui lòng kiểm tra lại các trường bắt buộc.'
  }

  const messages: Record<string, string> = {
    'Serial not found': 'Không tìm thấy serial bảo hành.',
    'Serial has already been used': 'Serial này đã được kích hoạt trước đó.',
    'Invalid dealer activation code': 'Mã kích hoạt đại lý không hợp lệ.',
    'Invalid film package': 'Gói film đã chọn không hợp lệ.',
    'Warranty data is incomplete': 'Thông tin bảo hành chưa đầy đủ. Vui lòng liên hệ hotline để được hỗ trợ.',
  }

  return typeof detail === 'string' ? messages[detail] || detail || fallback : fallback
}

const generateWarrantyQrImage = async () => {
  if (!process.client || lookup.value?.status !== 'activated') return

  qrError.value = ''

  try {
    if (qrPngUrl.value) {
      if (qrPngUrl.value.startsWith('blob:')) {
        URL.revokeObjectURL(qrPngUrl.value)
      }
      qrPngUrl.value = ''
    }

    const canvas = document.createElement('canvas')
    const width = 900
    const height = 1100
    const qrSize = 560
    const context = canvas.getContext('2d')

    if (!context) {
      throw new Error('Canvas is not supported')
    }

    canvas.width = width
    canvas.height = height

    context.fillStyle = '#ffffff'
    context.fillRect(0, 0, width, height)

    context.fillStyle = '#09090b'
    context.textAlign = 'center'
    context.font = '700 58px Arial, sans-serif'
    context.fillText('Newnice', width / 2, 120)

    context.font = '600 32px Arial, sans-serif'
    context.fillText('Thông tin bảo hành điện tử', width / 2, 178)

    context.fillStyle = '#f4f4f5'
    roundRect(context, 120, 235, 660, 660, 28)
    context.fill()

    drawQrToCanvas(context, warrantyInfoUrl.value, (width - qrSize) / 2, 285, qrSize)

    context.fillStyle = '#18181b'
    context.font = '700 34px Arial, sans-serif'
    context.fillText(`Serial: ${serial.value}`, width / 2, 950)

    context.fillStyle = '#52525b'
    context.font = '24px Arial, sans-serif'
    wrapText(context, warrantyInfoUrl.value, width / 2, 1000, 760, 32)

    qrPngUrl.value = await exportCanvasImage(canvas)
  } catch (err) {
    qrError.value = 'Không thể tạo ảnh QR. Vui lòng tải lại trang và thử lại.'
  }
}

const drawQrToCanvas = (
  context: CanvasRenderingContext2D,
  value: string,
  x: number,
  y: number,
  maxSize: number,
) => {
  const qr = encode(value, { ecc: 'M', border: 2 })
  const moduleSize = Math.max(1, Math.floor(maxSize / qr.size))
  const drawSize = moduleSize * qr.size
  const offsetX = x + Math.floor((maxSize - drawSize) / 2)
  const offsetY = y + Math.floor((maxSize - drawSize) / 2)

  context.fillStyle = '#ffffff'
  context.fillRect(x, y, maxSize, maxSize)
  context.fillStyle = '#09090b'

  for (let row = 0; row < qr.size; row += 1) {
    for (let col = 0; col < qr.size; col += 1) {
      if (qr.data[row]?.[col]) {
        context.fillRect(offsetX + col * moduleSize, offsetY + row * moduleSize, moduleSize, moduleSize)
      }
    }
  }
}

const exportCanvasImage = (canvas: HTMLCanvasElement) =>
  new Promise<string>((resolve, reject) => {
    if (!canvas.toBlob) {
      resolve(canvas.toDataURL('image/png'))
      return
    }

    canvas.toBlob((result) => {
      if (result) {
        resolve(URL.createObjectURL(result))
        return
      }

      try {
        resolve(canvas.toDataURL('image/png'))
      } catch (err) {
        reject(new Error('Cannot export QR image'))
      }
    }, 'image/png')
  })

const roundRect = (
  context: CanvasRenderingContext2D,
  x: number,
  y: number,
  width: number,
  height: number,
  radius: number,
) => {
  context.beginPath()
  context.moveTo(x + radius, y)
  context.arcTo(x + width, y, x + width, y + height, radius)
  context.arcTo(x + width, y + height, x, y + height, radius)
  context.arcTo(x, y + height, x, y, radius)
  context.arcTo(x, y, x + width, y, radius)
  context.closePath()
}

const wrapText = (
  context: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  maxWidth: number,
  lineHeight: number,
) => {
  const words = text.split('')
  let line = ''
  let currentY = y

  for (const char of words) {
    const nextLine = `${line}${char}`
    if (context.measureText(nextLine).width > maxWidth && line) {
      context.fillText(line, x, currentY)
      line = char
      currentY += lineHeight
    } else {
      line = nextLine
    }
  }

  if (line) context.fillText(line, x, currentY)
}

const downloadWarrantyQr = () => {
  if (!process.client || !qrPngUrl.value) return

  const link = document.createElement('a')
  link.href = qrPngUrl.value
  link.download = `newnice-bao-hanh-${serial.value}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const formatDate = (value: string) => new Date(value).toLocaleDateString('vi-VN')

const statusLabel = (status?: string) => {
  const labels: Record<string, string> = {
    expired: 'Hết hạn',
    void: 'Đã vô hiệu',
    unused: 'Chưa kích hoạt',
    activated: 'Đã kích hoạt',
  }
  return status ? labels[status] || status : '-'
}

watch(
  () => lookup.value?.status,
  () => {
    if (lookup.value?.status === 'activated') {
      generateWarrantyQrImage()
    }
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  if (qrPngUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(qrPngUrl.value)
  }
})
</script>

<style scoped>
.label-dark {
  @apply mb-1 block text-sm font-semibold text-zinc-700;
}

.input-dark {
  @apply w-full rounded-lg border border-zinc-300 bg-white px-3 py-3 text-base text-zinc-950 outline-none transition focus:border-zinc-950 focus:ring-2 focus:ring-zinc-950/10;
}
</style>

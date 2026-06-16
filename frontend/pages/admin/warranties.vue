<template>
  <div>
    <div class="mb-8 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Bảo hành điện tử</h1>
        <p class="mt-1 text-sm text-gray-500">Quản lý QR serial, kích hoạt bảo hành, đại lý và gói film.</p>
      </div>
      <button @click="exportSerials" class="inline-flex items-center justify-center rounded-lg bg-gray-900 px-4 py-2 font-semibold text-white hover:bg-gray-800">
        Export QR CSV
      </button>
    </div>

    <div class="mb-6 flex flex-wrap gap-2">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        class="rounded-lg px-4 py-2 text-sm font-semibold transition-colors"
        :class="activeTab === tab.key ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'"
      >
        {{ tab.label }}
      </button>
    </div>

    <p v-if="notice" class="mb-4 rounded-lg bg-green-50 px-4 py-3 text-sm font-medium text-green-700">{{ notice }}</p>
    <p v-if="errorMessage" class="mb-4 rounded-lg bg-red-50 px-4 py-3 text-sm font-medium text-red-700">{{ errorMessage }}</p>

    <section v-if="activeTab === 'warranties'" class="space-y-6">
      <div class="bg-white p-4 shadow-sm sm:rounded-lg">
        <div class="flex flex-col gap-3 md:flex-row">
          <input
            v-model="search"
            type="text"
            placeholder="Tìm serial, biển số, SĐT..."
            class="min-w-0 flex-1 rounded-lg border px-4 py-2 focus:border-primary-500 focus:ring-2 focus:ring-primary-500"
          />
          <select v-model="statusFilter" class="rounded-lg border px-4 py-2 focus:border-primary-500 focus:ring-2 focus:ring-primary-500">
            <option value="">Tất cả trạng thái</option>
            <option value="unused">Chưa kích hoạt</option>
            <option value="activated">Đã kích hoạt</option>
            <option value="expired">Hết hạn</option>
            <option value="void">Vô hiệu</option>
          </select>
        </div>
      </div>

      <div class="overflow-hidden bg-white shadow-sm sm:rounded-lg">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="border-b bg-gray-50">
              <tr>
                <th class="p-4 text-left text-sm font-semibold text-gray-600">Serial</th>
                <th class="p-4 text-left text-sm font-semibold text-gray-600">Loại</th>
                <th class="p-4 text-left text-sm font-semibold text-gray-600">Đại lý</th>
                <th class="p-4 text-left text-sm font-semibold text-gray-600">Khách hàng</th>
                <th class="p-4 text-left text-sm font-semibold text-gray-600">Xe</th>
                <th class="p-4 text-left text-sm font-semibold text-gray-600">Gói film</th>
                <th class="p-4 text-left text-sm font-semibold text-gray-600">Trạng thái</th>
                <th class="p-4 text-right text-sm font-semibold text-gray-600">Thao tác</th>
              </tr>
            </thead>
            <tbody class="divide-y">
              <tr v-for="item in warranties?.items" :key="item.id" class="hover:bg-gray-50">
                <td class="p-4">
                  <p class="font-mono text-sm font-semibold text-gray-900">{{ item.serial }}</p>
                  <p class="text-xs text-gray-500">{{ item.qr_url }}</p>
                </td>
                <td class="p-4 text-sm font-semibold text-gray-700">
                  {{ warrantyTypeLabel(item.warranty_type) }}
                </td>
                <td class="p-4 text-sm text-gray-600">
                  {{ item.dealer_name || '-' }}
                </td>
                <td class="p-4 text-sm">
                  <p class="font-medium text-gray-900">{{ item.customer_name || '-' }}</p>
                  <p class="text-gray-500">{{ item.customer_phone || '-' }}</p>
                </td>
                <td class="p-4 text-sm text-gray-600">
                  <template v-if="isVehicleWarranty(item)">
                    <p>{{ item.vehicle_plate || '-' }}</p>
                    <p>{{ item.vehicle_model || '-' }}</p>
                  </template>
                  <template v-else>
                    <p>{{ item.film_code || '-' }}</p>
                    <p>{{ item.area_m2 ? `${item.area_m2} m2` : '-' }}</p>
                  </template>
                </td>
                <td class="p-4 text-sm text-gray-600">
                  <p>{{ item.film_package_name || '-' }}</p>
                  <p v-if="item.warranty_expiry" class="text-xs text-gray-500">Hạn: {{ formatDate(item.warranty_expiry) }}</p>
                </td>
                <td class="p-4">
                  <span class="rounded-full px-3 py-1 text-xs font-semibold" :class="statusClass(item.status)">
                    {{ statusLabel(item.status) }}
                  </span>
                </td>
                <td class="p-4 text-right">
                  <button @click="openWarranty(item)" class="rounded-lg px-3 py-2 text-sm font-semibold text-primary-700 hover:bg-primary-50">
                    Sửa
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="!warranties?.items?.length" class="p-10 text-center text-gray-500">
          Chưa có serial phù hợp
        </div>

        <div v-if="warranties && warranties.total_pages > 1" class="flex justify-center gap-2 border-t p-4">
          <button
            v-for="p in warranties.total_pages"
            :key="p"
            @click="currentPage = p"
            class="h-10 w-10 rounded-lg font-medium transition-colors"
            :class="currentPage === p ? 'bg-primary-600 text-white' : 'bg-gray-100 hover:bg-gray-200'"
          >
            {{ p }}
          </button>
        </div>
      </div>
    </section>

    <section v-if="activeTab === 'serials'" class="grid gap-6 lg:grid-cols-[360px_1fr]">
      <form class="bg-white p-5 shadow-sm sm:rounded-lg" @submit.prevent="generateSerials">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">Tạo serial hàng loạt</h2>
        <div class="space-y-4">
          <div>
            <label class="label">Số lượng</label>
            <input v-model.number="generateForm.count" min="1" max="1000" type="number" class="input" />
          </div>
          <div>
            <label class="label">Đại lý nhận serial</label>
            <select v-model="generateForm.dealer_id" required class="input">
              <option value="">Chọn đại lý</option>
              <option v-for="dealer in activeDealers" :key="dealer.id" :value="dealer.id">{{ dealer.dealer_name }}</option>
            </select>
          </div>
          <div>
            <label class="label">Loại bảo hành</label>
            <select v-model="generateForm.warranty_type" required class="input">
              <option v-for="type in warrantyTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
            </select>
          </div>
          <div>
            <label class="label">Prefix</label>
            <input v-model="generateForm.prefix" class="input uppercase" />
          </div>
          <div>
            <label class="label">QR base URL</label>
            <input v-model="generateForm.qr_base_url" class="input" />
          </div>
        </div>
        <button type="submit" :disabled="busy" class="mt-5 w-full rounded-lg bg-primary-600 px-4 py-3 font-semibold text-white hover:bg-primary-700 disabled:opacity-60">
          {{ busy ? 'Đang tạo...' : 'Tạo serial' }}
        </button>
      </form>

      <div class="bg-white p-5 shadow-sm sm:rounded-lg">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">Serial vừa tạo</h2>
        <div class="grid gap-3 md:grid-cols-2">
          <div v-for="item in generatedSerials" :key="item.id" class="rounded-lg border p-3">
            <p class="font-mono text-sm font-semibold">{{ item.serial }}</p>
            <p class="mt-1 text-xs text-gray-600">Đại lý: {{ item.dealer_name || '-' }}</p>
            <p class="mt-1 text-xs text-gray-600">Loại: {{ warrantyTypeLabel(item.warranty_type) }}</p>
            <p class="mt-1 break-all text-xs text-gray-500">{{ item.qr_url }}</p>
          </div>
        </div>
        <p v-if="!generatedSerials.length" class="text-sm text-gray-500">Chưa có lô serial mới trong phiên này.</p>
      </div>
    </section>

    <section v-if="activeTab === 'dealers'" class="grid gap-6 lg:grid-cols-[360px_1fr]">
      <form class="bg-white p-5 shadow-sm sm:rounded-lg" @submit.prevent="createDealer">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">Thêm đại lý</h2>
        <div class="space-y-4">
          <div>
            <label class="label">Đại lý / showroom</label>
            <input v-model="dealerForm.dealer_name" required class="input" />
          </div>
          <div>
            <label class="label">Mã kích hoạt</label>
            <input v-model="dealerForm.activation_code" required class="input" />
          </div>
        </div>
        <button type="submit" class="mt-5 w-full rounded-lg bg-primary-600 px-4 py-3 font-semibold text-white hover:bg-primary-700">
          Lưu đại lý
        </button>
      </form>

      <div class="overflow-hidden bg-white shadow-sm sm:rounded-lg">
        <div v-if="dealersPending" class="p-8 text-center text-sm text-gray-500">
          Đang tải danh sách đại lý...
        </div>
        <div v-else-if="dealersLoadError" class="p-8 text-center">
          <p class="text-sm font-medium text-red-600">Không thể tải danh sách đại lý.</p>
          <button type="button" class="mt-3 rounded-lg bg-gray-900 px-4 py-2 text-sm font-semibold text-white" @click="refreshDealers">
            Tải lại
          </button>
        </div>
        <table v-else-if="dealers.length" class="w-full">
          <thead class="border-b bg-gray-50">
            <tr>
              <th class="p-4 text-left text-sm font-semibold text-gray-600">Đại lý</th>
              <th class="p-4 text-left text-sm font-semibold text-gray-600">Mã kích hoạt</th>
              <th class="p-4 text-left text-sm font-semibold text-gray-600">Serial đã gán</th>
              <th class="p-4 text-left text-sm font-semibold text-gray-600">Trạng thái</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="dealer in dealers" :key="dealer.id">
              <td class="p-4">
                <input v-model="dealer.dealer_name" class="w-full rounded-lg border px-3 py-2" @change="updateDealer(dealer)" />
              </td>
              <td class="p-4">
                <input v-model="dealer.activation_code" class="w-full rounded-lg border px-3 py-2" @change="updateDealer(dealer)" />
              </td>
              <td class="p-4 text-sm font-semibold text-gray-700">
                {{ dealer.serial_count || 0 }}
              </td>
              <td class="p-4">
                <select v-model="dealer.status" class="rounded-lg border px-3 py-2" @change="updateDealer(dealer)">
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="p-8 text-center text-sm text-gray-500">
          Chưa có đại lý nào. Thêm đại lý mới ở form bên trái.
        </div>
      </div>
    </section>

    <section v-if="activeTab === 'packages'" class="grid gap-6 lg:grid-cols-[360px_1fr]">
      <form class="bg-white p-5 shadow-sm sm:rounded-lg" @submit.prevent="createPackage">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">Thêm gói film</h2>
        <div class="space-y-4">
          <div>
            <label class="label">Tên gói</label>
            <input v-model="packageForm.package_name" required class="input" />
          </div>
          <div>
            <label class="label">Thời hạn bảo hành (tháng)</label>
            <input v-model.number="packageForm.warranty_duration_months" required min="1" type="number" class="input" />
          </div>
        </div>
        <button type="submit" class="mt-5 w-full rounded-lg bg-primary-600 px-4 py-3 font-semibold text-white hover:bg-primary-700">
          Lưu gói film
        </button>
      </form>

      <div class="overflow-hidden bg-white shadow-sm sm:rounded-lg">
        <table class="w-full">
          <thead class="border-b bg-gray-50">
            <tr>
              <th class="p-4 text-left text-sm font-semibold text-gray-600">Gói film</th>
              <th class="p-4 text-left text-sm font-semibold text-gray-600">Tháng BH</th>
              <th class="p-4 text-left text-sm font-semibold text-gray-600">Trạng thái</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="pkg in packages" :key="pkg.id">
              <td class="p-4">
                <input v-model="pkg.package_name" class="w-full rounded-lg border px-3 py-2" @change="updatePackage(pkg)" />
              </td>
              <td class="p-4">
                <input v-model.number="pkg.warranty_duration_months" type="number" min="1" class="w-28 rounded-lg border px-3 py-2" @change="updatePackage(pkg)" />
              </td>
              <td class="p-4">
                <select v-model="pkg.status" class="rounded-lg border px-3 py-2" @change="updatePackage(pkg)">
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <div v-if="selectedWarranty" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="selectedWarranty = null">
      <form class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-lg bg-white p-6" @submit.prevent="saveWarranty">
        <div class="mb-5 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Sửa bảo hành</h2>
            <p class="font-mono text-sm text-gray-500">{{ selectedWarranty.serial }}</p>
          </div>
          <button type="button" @click="selectedWarranty = null" class="rounded-lg p-2 text-gray-500 hover:bg-gray-100">Đóng</button>
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <div>
            <label class="label">Trạng thái</label>
            <select v-model="editForm.status" class="input">
              <option value="unused">Chưa kích hoạt</option>
              <option value="activated">Đã kích hoạt</option>
              <option value="expired">Hết hạn</option>
              <option value="void">Vô hiệu</option>
            </select>
          </div>
          <div>
            <label class="label">Đại lý</label>
            <select v-model="editForm.dealer_id" class="input">
              <option value="">-</option>
              <option v-for="dealer in dealers" :key="dealer.id" :value="dealer.id">{{ dealer.dealer_name }}</option>
            </select>
          </div>
          <div>
            <label class="label">Loại bảo hành</label>
            <select v-model="editForm.warranty_type" class="input">
              <option v-for="type in warrantyTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
            </select>
          </div>
          <div>
            <label class="label">Tên khách hàng</label>
            <input v-model="editForm.customer_name" class="input" />
          </div>
          <div>
            <label class="label">SĐT khách hàng</label>
            <input v-model="editForm.customer_phone" class="input" />
          </div>
          <div>
            <label class="label">Biển số xe</label>
            <input v-model="editForm.vehicle_plate" class="input uppercase" />
          </div>
          <div>
            <label class="label">Mẫu xe</label>
            <input v-model="editForm.vehicle_model" class="input" />
          </div>
          <div>
            <label class="label">Gói film</label>
            <select v-model="editForm.film_package_id" class="input">
              <option value="">-</option>
              <option v-for="pkg in packages" :key="pkg.id" :value="pkg.id">{{ pkg.package_name }}</option>
            </select>
          </div>
          <div>
            <label class="label">Ngày dán</label>
            <input v-model="editForm.install_date" type="date" class="input" />
          </div>
          <div>
            <label class="label">Hạn bảo hành</label>
            <input v-model="editForm.warranty_expiry" type="date" class="input" />
          </div>
          <div>
            <label class="label">Mã film kính lái</label>
            <input v-model="editForm.front_windshield_film_code" class="input" />
          </div>
          <div>
            <label class="label">Mã film kính hậu</label>
            <input v-model="editForm.rear_windshield_film_code" class="input" />
          </div>
          <div>
            <label class="label">Mã film kính sườn</label>
            <input v-model="editForm.side_window_film_code" class="input" />
          </div>
          <div>
            <label class="label">Mã film</label>
            <input v-model="editForm.film_code" class="input" />
          </div>
          <div>
            <label class="label">Số mét vuông</label>
            <input v-model="editForm.area_m2" min="0" step="0.1" type="number" class="input" />
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button type="button" @click="selectedWarranty = null" class="rounded-lg bg-gray-100 px-4 py-2 font-semibold text-gray-700 hover:bg-gray-200">
            Hủy
          </button>
          <button type="submit" class="rounded-lg bg-primary-600 px-4 py-2 font-semibold text-white hover:bg-primary-700">
            Lưu thay đổi
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  layout: 'admin',
})

useSeoMeta({
  title: 'Bảo hành điện tử | Newnice Admin',
  robots: 'noindex, nofollow',
})

interface Paginated<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

type WarrantyType = 'auto_film' | 'auto_ppf' | 'building_film' | 'kitchen_ppf'

interface Warranty {
  id: string
  serial: string
  qr_url?: string
  warranty_type: WarrantyType
  status: string
  dealer_id?: string
  dealer_name?: string
  customer_name?: string
  customer_phone?: string
  vehicle_plate?: string
  vehicle_model?: string
  film_package_id?: string
  film_package_name?: string
  front_windshield_film_code?: string
  rear_windshield_film_code?: string
  side_window_film_code?: string
  film_code?: string
  area_m2?: number
  install_date?: string
  warranty_expiry?: string
}

interface Dealer {
  id: string
  dealer_name: string
  activation_code: string
  serial_count?: number
  status: string
}

interface FilmPackage {
  id: string
  package_name: string
  warranty_duration_months: number
  status: string
}

const config = useRuntimeConfig()
const authStore = useAuthStore()
const authHeaders = computed(() => authStore.token ? { Authorization: `Bearer ${authStore.token}` } : {})

const tabs = [
  { key: 'warranties', label: 'Bảo hành' },
  { key: 'serials', label: 'Tạo serial' },
  { key: 'dealers', label: 'Đại lý' },
  { key: 'packages', label: 'Gói film' },
]

const activeTab = ref('warranties')
const currentPage = ref(1)
const search = ref('')
const statusFilter = ref('')
const busy = ref(false)
const notice = ref('')
const errorMessage = ref('')
const generatedSerials = ref<Warranty[]>([])
const selectedWarranty = ref<Warranty | null>(null)

const warrantyTypes: { value: WarrantyType, label: string }[] = [
  { value: 'auto_film', label: 'Film ô tô' },
  { value: 'auto_ppf', label: 'PPF xe' },
  { value: 'building_film', label: 'Film nhà kính' },
  { value: 'kitchen_ppf', label: 'PPF bếp' },
]

const vehicleWarrantyTypes: WarrantyType[] = ['auto_film', 'auto_ppf']

const generateForm = reactive({
  count: 20,
  prefix: 'DLA',
  dealer_id: '',
  warranty_type: 'auto_film' as WarrantyType,
  qr_base_url: config.public.siteUrl,
})

const dealerForm = reactive({
  dealer_name: '',
  activation_code: '',
  status: 'active',
})

const packageForm = reactive({
  package_name: '',
  warranty_duration_months: 36,
  status: 'active',
})

const editForm = reactive<Record<string, string>>({})

const queryParams = computed(() => {
  const params = new URLSearchParams()
  params.append('page', String(currentPage.value))
  params.append('page_size', '10')
  if (search.value.trim()) params.append('search', search.value.trim())
  if (statusFilter.value) params.append('status', statusFilter.value)
  return params.toString()
})

const { data: warranties, refresh: refreshWarranties } = await useFetch<Paginated<Warranty>>(
  () => `${config.public.apiBase}/admin/warranties?${queryParams.value}`,
  { headers: authHeaders },
)

const { data: dealersData, pending: dealersPending, error: dealersLoadError, refresh: refreshDealers } = await useFetch<Dealer[]>(
  () => `${config.public.apiBase}/admin/dealers`,
  { headers: authHeaders },
)

const { data: packagesData, refresh: refreshPackages } = await useFetch<FilmPackage[]>(
  () => `${config.public.apiBase}/admin/film-packages`,
  { headers: authHeaders },
)

const dealers = computed(() => dealersData.value || [])
const activeDealers = computed(() => dealers.value.filter((dealer) => dealer.status === 'active'))
const packages = computed(() => packagesData.value || [])

const warrantyTypeLabel = (type?: WarrantyType) => warrantyTypes.find((item) => item.value === type)?.label || type || '-'
const isVehicleWarranty = (item: Warranty) => vehicleWarrantyTypes.includes(item.warranty_type || 'auto_film')

watch([statusFilter, currentPage], () => refreshWarranties())
watch(search, () => {
  currentPage.value = 1
  refreshWarranties()
})
watch(activeTab, (tab) => {
  if (tab === 'dealers' || tab === 'serials') refreshDealers()
  if (tab === 'packages') refreshPackages()
  if (tab === 'warranties') refreshWarranties()
})

const apiFetch = async <T>(path: string, options: any = {}) => {
  errorMessage.value = ''
  return await $fetch<T>(`${config.public.apiBase}${path}`, {
    ...options,
    headers: {
      ...authHeaders.value,
      ...(options.headers || {}),
    },
  })
}

const generateSerials = async () => {
  if (!generateForm.dealer_id) {
    errorMessage.value = 'Vui lòng chọn đại lý nhận serial.'
    return
  }
  busy.value = true
  notice.value = ''
  try {
    const response = await apiFetch<{ items: Warranty[] }>('/admin/warranty-serials/generate', {
      method: 'POST',
      body: generateForm,
    })
    generatedSerials.value = response.items
    notice.value = `Đã tạo ${response.items.length} serial mới.`
    refreshWarranties()
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'Không thể tạo serial.'
  } finally {
    busy.value = false
  }
}

const exportSerials = async () => {
  try {
    const blob = await $fetch<Blob>(`${config.public.apiBase}/admin/warranty-serials/export`, {
      headers: authHeaders.value,
      responseType: 'blob',
    })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'warranty-serials.csv'
    link.click()
    URL.revokeObjectURL(url)
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'Không thể export CSV.'
  }
}

const createDealer = async () => {
  try {
    await apiFetch<Dealer>('/admin/dealers', { method: 'POST', body: dealerForm })
    dealerForm.dealer_name = ''
    dealerForm.activation_code = ''
    notice.value = 'Đã thêm đại lý.'
    refreshDealers()
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'Không thể lưu đại lý.'
  }
}

const updateDealer = async (dealer: Dealer) => {
  try {
    await apiFetch<Dealer>(`/admin/dealers/${dealer.id}`, { method: 'PATCH', body: dealer })
    notice.value = 'Đã cập nhật đại lý.'
    refreshDealers()
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'Không thể cập nhật đại lý.'
  }
}

const createPackage = async () => {
  try {
    await apiFetch<FilmPackage>('/admin/film-packages', { method: 'POST', body: packageForm })
    packageForm.package_name = ''
    packageForm.warranty_duration_months = 36
    notice.value = 'Đã thêm gói film.'
    refreshPackages()
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'Không thể lưu gói film.'
  }
}

const updatePackage = async (pkg: FilmPackage) => {
  try {
    await apiFetch<FilmPackage>(`/admin/film-packages/${pkg.id}`, { method: 'PATCH', body: pkg })
    notice.value = 'Đã cập nhật gói film.'
    refreshPackages()
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'Không thể cập nhật gói film.'
  }
}

const openWarranty = (item: Warranty) => {
  selectedWarranty.value = item
  Object.assign(editForm, {
    status: item.status || 'unused',
    warranty_type: item.warranty_type || 'auto_film',
    dealer_id: item.dealer_id || '',
    customer_name: item.customer_name || '',
    customer_phone: item.customer_phone || '',
    vehicle_plate: item.vehicle_plate || '',
    vehicle_model: item.vehicle_model || '',
    film_package_id: item.film_package_id || '',
    install_date: item.install_date || '',
    warranty_expiry: item.warranty_expiry || '',
    front_windshield_film_code: item.front_windshield_film_code || '',
    rear_windshield_film_code: item.rear_windshield_film_code || '',
    side_window_film_code: item.side_window_film_code || '',
    film_code: item.film_code || '',
    area_m2: item.area_m2 ? String(item.area_m2) : '',
  })
}

const saveWarranty = async () => {
  if (!selectedWarranty.value) return
  const body = Object.fromEntries(
    Object.entries(editForm).map(([key, value]) => [key, value === '' ? null : value]),
  )
  try {
    await apiFetch<Warranty>(`/admin/warranties/${selectedWarranty.value.id}`, {
      method: 'PATCH',
      body,
    })
    selectedWarranty.value = null
    notice.value = 'Đã cập nhật bảo hành.'
    refreshWarranties()
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'Không thể cập nhật bảo hành.'
  }
}

const formatDate = (dateStr: string) => new Date(dateStr).toLocaleDateString('vi-VN')

const statusLabel = (status: string) => {
  const labels: Record<string, string> = {
    unused: 'Chưa kích hoạt',
    activated: 'Đã kích hoạt',
    expired: 'Hết hạn',
    void: 'Vô hiệu',
  }
  return labels[status] || status
}

const statusClass = (status: string) => {
  const classes: Record<string, string> = {
    unused: 'bg-amber-50 text-amber-700',
    activated: 'bg-green-50 text-green-700',
    expired: 'bg-gray-100 text-gray-700',
    void: 'bg-red-50 text-red-700',
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}
</script>

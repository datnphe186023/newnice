<template>
  <div class="bg-gray-50 rounded-2xl p-6">
    <h3 class="font-semibold text-lg mb-5">Thông Số Kỹ Thuật</h3>
    <div class="divide-y divide-gray-200">
      <div
        v-for="spec in visibleSpecs"
        :key="spec.key"
        class="flex items-center justify-between py-3 first:pt-0 last:pb-0"
      >
        <span class="text-sm text-gray-500">{{ spec.label }}</span>
        <div class="flex items-center gap-2">
          <!-- Progress bar for percentage values -->
          <template v-if="spec.isPercent">
            <div class="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                class="h-full rounded-full transition-all duration-700"
                :class="spec.barColor"
                :style="{ width: `${spec.value}%` }"
              />
            </div>
          </template>
          <span class="text-sm font-semibold text-gray-900 min-w-[3rem] text-right">
            {{ spec.formatted }}
          </span>
        </div>
      </div>

      <!-- Empty state -->
      <p v-if="!visibleSpecs.length" class="text-sm text-gray-400 text-center py-4">
        Chưa có thông số kỹ thuật
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface SpecRow {
  key: string
  label: string
  value: number | string
  formatted: string
  isPercent: boolean
  barColor: string
}

const props = defineProps<{
  vlt?: number
  uvRejection?: number
  irRejection?: number
  heatRejection?: number
  thickness?: string
  warrantyYears?: number
  filmType?: string
}>()

const filmTypeLabels: Record<string, string> = {
  ceramic: 'Ceramic',
  carbon: 'Carbon',
  metallic: 'Metallic',
  dyed: 'Dyed',
  hybrid: 'Hybrid',
  nano: 'Nano',
}

const visibleSpecs = computed<SpecRow[]>(() => {
  const rows: SpecRow[] = []

  if (props.filmType) {
    rows.push({
      key: 'filmType',
      label: 'Loại phim',
      value: props.filmType,
      formatted: filmTypeLabels[props.filmType] || props.filmType,
      isPercent: false,
      barColor: '',
    })
  }
  if (props.vlt != null) {
    rows.push({
      key: 'vlt',
      label: 'Độ trong suốt (VLT)',
      value: props.vlt,
      formatted: `${props.vlt}%`,
      isPercent: true,
      barColor: 'bg-blue-400',
    })
  }
  if (props.uvRejection != null) {
    rows.push({
      key: 'uv',
      label: 'Chặn tia UV',
      value: props.uvRejection,
      formatted: `${props.uvRejection}%`,
      isPercent: true,
      barColor: 'bg-violet-500',
    })
  }
  if (props.irRejection != null) {
    rows.push({
      key: 'ir',
      label: 'Chặn hồng ngoại (IR)',
      value: props.irRejection,
      formatted: `${props.irRejection}%`,
      isPercent: true,
      barColor: 'bg-orange-400',
    })
  }
  if (props.heatRejection != null) {
    rows.push({
      key: 'heat',
      label: 'Giảm nhiệt',
      value: props.heatRejection,
      formatted: `${props.heatRejection}%`,
      isPercent: true,
      barColor: 'bg-red-400',
    })
  }
  if (props.thickness) {
    rows.push({
      key: 'thickness',
      label: 'Độ dày',
      value: props.thickness,
      formatted: props.thickness,
      isPercent: false,
      barColor: '',
    })
  }
  if (props.warrantyYears != null) {
    rows.push({
      key: 'warranty',
      label: 'Bảo hành',
      value: props.warrantyYears,
      formatted: `${props.warrantyYears} năm`,
      isPercent: false,
      barColor: '',
    })
  }

  return rows
})
</script>

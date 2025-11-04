<template>
  <div class="rounded-lg border p-8 transition-colors" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
    <h3 class="text-sm font-medium uppercase tracking-wide mb-6 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-500'">Estado das Embarcações</h3>

    <div v-if="vessels.length === 0" class="text-center py-12 text-sm transition-colors" :class="isDark ? 'text-slate-500' : 'text-gray-400'">
      Aguardando eventos...
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="vessel in vessels"
        :key="vessel.id"
        class="flex items-center justify-between p-4 rounded-lg border transition-all"
        :class="getVesselBorderClass(vessel, isDark)"
      >
        <!-- Info da Embarcação -->
        <div class="flex items-center space-x-4">
          <div class="text-3xl">{{ getVesselIcon(vessel) }}</div>
          <div>
            <div class="text-sm font-semibold transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">Embarcação {{ vessel.displayNumber }}</div>
            <div class="text-xs mt-0.5 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-500'">{{ getVesselStatusText(vessel) }}</div>
          </div>
        </div>

        <!-- Capacidade -->
        <div class="flex items-center space-x-4">
          <div>
            <div class="text-xs mb-1 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-500'">Capacidade</div>
            <div class="text-lg font-semibold" :class="getCapacityTextClass(vessel.capacity, isDark)">
              {{ vessel.capacity }}/50
            </div>
          </div>

          <!-- Barra visual -->
          <div class="w-32 h-2 rounded-full overflow-hidden transition-colors" :class="isDark ? 'bg-slate-700' : 'bg-gray-200'">
            <div
              class="h-full transition-all duration-500 rounded-full"
              :class="getCapacityBarClass(vessel.capacity)"
              :style="{ width: `${(vessel.capacity / 50) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Legenda simples -->
    <div class="mt-6 pt-4 border-t transition-colors" :class="isDark ? 'border-slate-700' : 'border-gray-200'">
      <div class="flex items-center justify-center space-x-6 text-xs transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-500'">
        <div class="flex items-center space-x-1.5">
          <span>⚓</span>
          <span>Disponível no porto</span>
        </div>
        <div class="flex items-center space-x-1.5">
          <span>📦</span>
          <span>Embarcando veículos</span>
        </div>
        <div class="flex items-center space-x-1.5">
          <span>🚢</span>
          <span>Em travessia</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  events: {
    type: Array,
    required: true
  },
  totalVessels: {
    type: Number,
    required: true
  },
  isDark: {
    type: Boolean,
    default: false
  }
})

const vessels = computed(() => {
  const vesselMap = new Map()

  for (let i = 0; i < props.totalVessels; i++) {
    const backendId = String(i)
    vesselMap.set(backendId, {
      id: backendId,
      displayNumber: i + 1,
      status: 'idle',
      capacity: 0,
      lastEventTime: null
    })
  }

  props.events.forEach(event => {
    if (!event.vessel_name) return

    const backendId = event.vessel_name

    if (!vesselMap.has(backendId)) return

    const vessel = vesselMap.get(backendId)
    vessel.lastEventTime = event.t

    switch (event.event_type) {
      case 'boarding':
        vessel.status = 'boarding'
        vessel.capacity = event.vessel_used_capacity || 0
        break
      case 'departure':
        vessel.status = 'crossing'
        vessel.capacity = event.vessel_used_capacity || 0
        break
      case 'return':
        vessel.status = 'idle'
        vessel.capacity = 0
        break
    }

    vesselMap.set(backendId, vessel)
  })

  return Array.from(vesselMap.values()).sort((a, b) => a.displayNumber - b.displayNumber)
})

function getVesselIcon(vessel) {
  switch (vessel.status) {
    case 'idle': return '⚓'
    case 'boarding': return '📦'
    case 'crossing': return '🚢'
    default: return '⚓'
  }
}

function getVesselStatusText(vessel) {
  switch (vessel.status) {
    case 'idle': return 'Disponível no porto'
    case 'boarding': return 'Embarcando veículos'
    case 'crossing': return 'Em travessia'
    default: return 'Aguardando'
  }
}

function getVesselBorderClass(vessel, isDark) {
  switch (vessel.status) {
    case 'idle':
      return isDark
        ? 'border-slate-600 bg-slate-700/50'
        : 'border-gray-300 bg-gray-50'
    case 'boarding':
      return isDark
        ? 'border-yellow-600 bg-yellow-900/20'
        : 'border-yellow-400 bg-yellow-50'
    case 'crossing':
      return isDark
        ? 'border-blue-600 bg-blue-900/20'
        : 'border-blue-400 bg-blue-50'
    default:
      return isDark
        ? 'border-slate-600'
        : 'border-gray-300'
  }
}

function getCapacityTextClass(capacity, isDark) {
  const percentage = (capacity / 50) * 100
  if (percentage >= 90) {
    return isDark ? 'text-red-400' : 'text-red-600'
  }
  if (percentage >= 70) {
    return isDark ? 'text-orange-400' : 'text-orange-600'
  }
  if (percentage >= 40) {
    return isDark ? 'text-blue-400' : 'text-blue-600'
  }
  return isDark ? 'text-slate-300' : 'text-gray-600'
}

function getCapacityBarClass(capacity) {
  const percentage = (capacity / 50) * 100
  if (percentage >= 90) return 'bg-red-500'
  if (percentage >= 70) return 'bg-orange-500'
  if (percentage >= 40) return 'bg-blue-500'
  return 'bg-gray-400'
}
</script>

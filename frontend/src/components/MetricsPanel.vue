<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
    <!-- Total de Veículos -->
    <div class="rounded-lg border p-5 transition-colors" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
      <p class="text-xs font-medium uppercase tracking-wide mb-2 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-500'">Total de Veículos</p>
      <p class="text-3xl font-semibold transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">{{ metrics.totalVehicles }}</p>
      <p class="text-xs mt-1 transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-400'">chegadas registradas</p>
    </div>

    <!-- Veículos Aguardando -->
    <div class="rounded-lg border p-5 transition-colors" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
      <p class="text-xs font-medium uppercase tracking-wide mb-2 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-500'">Veículos Aguardando</p>
      <p class="text-3xl font-semibold transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">{{ metrics.currentQueueSize }}</p>
      <div class="flex items-center space-x-1.5 mt-1">
        <component :is="queueTrendIcon" :size="14" :class="queueTrendColor" />
        <p class="text-xs transition-colors" :class="queueTrendColor">{{ queueTrendText }}</p>
      </div>
    </div>

    <!-- Utilização Média -->
    <div class="rounded-lg border p-5 transition-colors" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
      <p class="text-xs font-medium uppercase tracking-wide mb-2 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-500'">Utilização Média das Embarcações</p>
      <p class="text-3xl font-semibold transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">{{ metrics.avgUtilization }}%</p>
    </div>

    <!-- Status -->
    <div class="rounded-lg border p-5 transition-colors" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
      <p class="text-xs font-medium uppercase tracking-wide mb-2 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-500'">Status</p>
      <p
        class="text-2xl font-semibold transition-colors"
        :class="isComplete ? (isDark ? 'text-green-400' : 'text-green-600') : (isDark ? 'text-blue-400' : 'text-blue-600')"
      >
        {{ simulationStatus }}
      </p>
      <p class="text-xs mt-1 transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-400'">{{ progressText }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ArrowUp, ArrowDown, ArrowRight } from 'lucide-vue-next'

const props = defineProps({
  events: {
    type: Array,
    required: true
  },
  totalEvents: {
    type: Number,
    required: true
  },
  isComplete: {
    type: Boolean,
    default: false
  },
  isDark: {
    type: Boolean,
    default: false
  }
})

const metrics = computed(() => {
  const arrivals = props.events.filter(e => e.event_type === 'arrival')

  // Fila
  const queueSizes = props.events
    .filter(e => 'queue_size' in e)
    .map(e => e.queue_size)

  // Fila atual (último valor registrado)
  const currentQueueSize = queueSizes.length > 0
    ? queueSizes[queueSizes.length - 1]
    : 0

  // Tendência da fila (comparar com média dos últimos valores)
  let queueTrend = 'stable'
  if (queueSizes.length >= 5) {
    const recentAvg = queueSizes.slice(-5, -1).reduce((a, b) => a + b, 0) / 4
    if (currentQueueSize > recentAvg + 1) {
      queueTrend = 'increasing'
    } else if (currentQueueSize < recentAvg - 1) {
      queueTrend = 'decreasing'
    }
  }

  // Utilização em tempo real - estado atual de cada embarcação
  const vesselCapacities = new Map()

  props.events.forEach(event => {
    if (!event.vessel_name) return

    const vesselId = event.vessel_name

    if (event.event_type === 'boarding' || event.event_type === 'departure') {
      // Atualizar capacidade da embarcação
      vesselCapacities.set(vesselId, event.vessel_used_capacity || 0)
    } else if (event.event_type === 'return') {
      // Embarcação voltou vazia
      vesselCapacities.set(vesselId, 0)
    }
  })

  // Calcular utilização média de todas as embarcações no estado atual
  const currentCapacities = Array.from(vesselCapacities.values())
  const avgUtilization = currentCapacities.length > 0
    ? Math.round((currentCapacities.reduce((a, b) => a + b, 0) / currentCapacities.length / 50) * 100)
    : 0

  return {
    totalVehicles: arrivals.length,
    currentQueueSize,
    queueTrend,
    avgUtilization
  }
})

const queueTrendIcon = computed(() => {
  switch (metrics.value.queueTrend) {
    case 'increasing': return ArrowUp
    case 'decreasing': return ArrowDown
    default: return ArrowRight
  }
})

const queueTrendText = computed(() => {
  switch (metrics.value.queueTrend) {
    case 'increasing': return 'aumentando'
    case 'decreasing': return 'diminuindo'
    default: return 'estável'
  }
})

const queueTrendColor = computed(() => {
  if (props.isDark) {
    switch (metrics.value.queueTrend) {
      case 'increasing': return 'text-red-400'
      case 'decreasing': return 'text-green-400'
      default: return 'text-slate-400'
    }
  } else {
    switch (metrics.value.queueTrend) {
      case 'increasing': return 'text-red-600'
      case 'decreasing': return 'text-green-600'
      default: return 'text-gray-500'
    }
  }
})

const simulationStatus = computed(() => {
  return props.isComplete ? 'Completa' : 'Em Progresso'
})

const progressText = computed(() => {
  const percentage = Math.round((props.events.length / props.totalEvents) * 100)
  return props.isComplete
    ? 'simulação finalizada'
    : `${percentage}% processado`
})
</script>

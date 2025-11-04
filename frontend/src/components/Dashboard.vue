<template>
  <div class="space-y-8">
    <!-- Controles de Replay -->
    <div class="rounded-lg border p-6 transition-colors" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4">
        <div>
          <h3 class="text-base font-semibold transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">Controles</h3>
          <p class="text-sm mt-1 transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-500'">
            {{ formatTime(replayState.currentTime) }} / {{ formatTime(maxTime) }}
          </p>
        </div>

        <div class="flex items-center space-x-3">
          <button
            @click="togglePlay"
            class="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium text-sm"
          >
            {{ replayState.isPlaying ? '⏸ Pausar' : '▶ Reproduzir' }}
          </button>

          <button
            @click="emit('reset')"
            class="px-5 py-2 rounded-lg transition-colors font-medium text-sm"
            :class="isDark ? 'bg-slate-700 text-slate-200 hover:bg-slate-600' : 'bg-gray-600 text-white hover:bg-gray-700'"
          >
            Nova Simulação
          </button>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="mb-4">
        <div class="h-1.5 rounded-full overflow-hidden transition-colors" :class="isDark ? 'bg-slate-700' : 'bg-gray-200'">
          <div
            class="h-full bg-blue-600 transition-all duration-300"
            :style="{ width: `${progressPercentage}%` }"
          ></div>
        </div>
      </div>

      <!-- Speed Controls -->
      <div class="flex items-center space-x-2">
        <span class="text-sm font-medium transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-600'">Velocidade:</span>
        <button
          v-for="speed in [0.5, 1, 3, 5, 10]"
          :key="speed"
          @click="changeSpeed(speed)"
          class="px-3 py-1 rounded-lg transition-all text-xs font-medium"
          :class="replayState.speed === speed
            ? 'bg-blue-600 text-white'
            : (isDark ? 'bg-slate-700 text-slate-300 hover:bg-slate-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200')"
        >
          {{ speed }}x
        </button>
        <span class="text-xs ml-2 transition-colors" :class="isDark ? 'text-slate-500' : 'text-gray-400'">
          (1x = 1min/seg)
        </span>
      </div>
    </div>

    <!-- Métricas Essenciais -->
    <MetricsPanel
      :events="replayState.processedEvents"
      :total-events="simulationData.events.length"
      :is-complete="!replayState.isPlaying && progressPercentage >= 99"
      :is-dark="isDark"
    />

    <!-- Gráfico de Fila - PROTAGONISTA -->
    <QueueChart :events="replayState.processedEvents" :is-dark="isDark" />

    <!-- Visualização de Embarcações -->
    <VesselsVisualization
      :events="replayState.processedEvents"
      :total-vessels="simulationData.initial_parameters.vessels_number"
      :is-dark="isDark"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import MetricsPanel from './MetricsPanel.vue'
import QueueChart from './QueueChart.vue'
import VesselsVisualization from './VesselsVisualization.vue'

const props = defineProps({
  simulationData: {
    type: Object,
    required: true
  },
  replayState: {
    type: Object,
    required: true
  },
  isDark: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['reset'])

const maxTime = computed(() => {
  if (!props.simulationData.events || props.simulationData.events.length === 0) {
    return 960
  }
  return props.simulationData.events[props.simulationData.events.length - 1].t
})

const progressPercentage = computed(() => {
  return Math.min(100, (props.replayState.currentTime / maxTime.value) * 100)
})

function togglePlay() {
  props.replayState.isPlaying = !props.replayState.isPlaying

  if (props.replayState.isPlaying && progressPercentage.value >= 99) {
    props.replayState.currentTime = 0
    props.replayState.currentEventIndex = 0
    props.replayState.processedEvents = []
  }

  if (props.replayState.isPlaying) {
    startReplay()
  }
}

function changeSpeed(speed) {
  props.replayState.speed = speed
}

function startReplay() {
  if (!props.simulationData || !props.simulationData.events) return

  if (props.replayState.intervalId) {
    clearInterval(props.replayState.intervalId)
  }

  const events = props.simulationData.events
  const updateInterval = 100
  const timeStep = 0.1

  props.replayState.intervalId = setInterval(() => {
    if (!props.replayState.isPlaying) {
      clearInterval(props.replayState.intervalId)
      props.replayState.intervalId = null
      return
    }

    props.replayState.currentTime += timeStep * props.replayState.speed

    while (
      props.replayState.currentEventIndex < events.length &&
      events[props.replayState.currentEventIndex].t <= props.replayState.currentTime
    ) {
      props.replayState.processedEvents.push(events[props.replayState.currentEventIndex])
      props.replayState.currentEventIndex++
    }

    if (props.replayState.currentTime >= maxTime.value) {
      props.replayState.currentTime = maxTime.value
      props.replayState.isPlaying = false
      clearInterval(props.replayState.intervalId)
      props.replayState.intervalId = null
    }
  }, updateInterval)
}

function formatTime(minutes) {
  const hours = Math.floor(minutes / 60)
  const mins = Math.round(minutes % 60)
  return `${hours}h ${mins}m`
}
</script>

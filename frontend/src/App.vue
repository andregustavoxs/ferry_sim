<template>
  <div class="min-h-screen transition-colors duration-200" :class="isDark ? 'bg-slate-900' : 'bg-gray-50'">
    <!-- Header -->
    <header class="border-b transition-colors duration-200" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
      <div class="max-w-5xl mx-auto px-6 py-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-semibold transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">Simulação Ferry Boat</h1>
            <p class="mt-1 text-sm transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-500'">Sistema de monitoramento em tempo real</p>
          </div>
          <div class="flex items-center space-x-4">
            <!-- Toggle Dark/Light -->
            <button
              @click="toggleTheme"
              class="flex items-center space-x-2 px-3 py-2 rounded-lg transition-all"
              :class="isDark ? 'bg-slate-700 hover:bg-slate-600 text-slate-300' : 'bg-gray-100 hover:bg-gray-200 text-gray-700'"
            >
              <span class="text-lg">{{ isDark ? '☀️' : '🌙' }}</span>
              <span class="text-xs font-medium">{{ isDark ? 'Claro' : 'Escuro' }}</span>
            </button>

            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              <span class="text-xs transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-500'">Online</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 py-10">
      <!-- Formulário de Simulação -->
      <SimulationForm
        v-if="!isSimulating && !simulationData"
        :is-dark="isDark"
        @start-simulation="startSimulation"
      />

      <!-- Dashboard da Simulação -->
      <Dashboard
        v-if="simulationData"
        :simulation-data="simulationData"
        :replay-state="replayState"
        :is-dark="isDark"
        @reset="resetSimulation"
      />

      <!-- Loading State -->
      <div v-if="isSimulating && !simulationData" class="flex flex-col items-center justify-center py-20">
        <div class="relative">
          <div class="w-20 h-20 border-4 rounded-full animate-spin transition-colors" :class="isDark ? 'border-slate-700 border-t-ocean-500' : 'border-ocean-200 border-t-ocean-600'"></div>
        </div>
        <p class="mt-6 text-lg font-medium transition-colors" :class="isDark ? 'text-white' : 'text-gray-700'">Executando simulação...</p>
        <p class="mt-2 text-sm transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-500'">Aguarde enquanto processamos os dados</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import axios from 'axios'
import SimulationForm from './components/SimulationForm.vue'
import Dashboard from './components/Dashboard.vue'

const isDark = ref(false)
const isSimulating = ref(false)
const simulationData = ref(null)
const replayState = reactive({
  currentTime: 0,
  isPlaying: false,
  speed: 1, // Velocidade padrão 1x (1 min simulado = 1 seg real)
  currentEventIndex: 0,
  processedEvents: [],
  intervalId: null
})

// Watchers para debug
watch(isSimulating, (newVal, oldVal) => {
  console.log('🔄 isSimulating mudou:', oldVal, '->', newVal)
})

watch(simulationData, (newVal, oldVal) => {
  console.log('🔄 simulationData mudou:', oldVal, '->', newVal)
  console.log('📊 simulationData tem eventos?', !!newVal?.events)
})

function toggleTheme() {
  isDark.value = !isDark.value
}

async function startSimulation(params) {
  console.log('🚀 Iniciando simulação com params:', params)
  isSimulating.value = true
  simulationData.value = null

  try {
    console.log('📡 Fazendo requisição para o backend...')
    const response = await axios.get('http://localhost:8080/simulate', {
      params: {
        vessels_number: params.vesselsNumber,
        each_vessel_departure_period: params.departurePeriod
      }
    })

    console.log('✅ Resposta recebida:', response)
    console.log('📊 Dados da simulação:', response.data)
    console.log('📝 Eventos:', response.data?.events?.length, 'eventos')
    console.log('⚙️ Initial parameters:', response.data?.initial_parameters)

    simulationData.value = response.data
    console.log('💾 simulationData.value setado:', simulationData.value)

    isSimulating.value = false
    console.log('⏸️ isSimulating setado como false')

    // Inicializar replay
    replayState.currentTime = 0
    replayState.currentEventIndex = 0
    replayState.processedEvents = []
    replayState.isPlaying = true

    console.log('▶️ Iniciando replay...')
    // Iniciar replay automático
    startReplay()
  } catch (error) {
    console.error('❌ Erro ao executar simulação:', error)
    alert('Erro ao executar simulação. Verifique se o servidor está rodando.')
    isSimulating.value = false
  }
}

function startReplay() {
  console.log('🎬 startReplay chamado')
  console.log('📊 simulationData.value:', simulationData.value)
  console.log('📝 simulationData.value.events:', simulationData.value?.events)

  if (!simulationData.value || !simulationData.value.events) {
    console.log('⚠️ startReplay retornando early - sem dados ou eventos')
    return
  }

  // Limpar intervalo anterior se existir
  if (replayState.intervalId) {
    console.log('🧹 Limpando intervalo anterior')
    clearInterval(replayState.intervalId)
  }

  const events = simulationData.value.events
  const maxTime = events[events.length - 1]?.t || 960

  console.log('📈 Total de eventos:', events.length)
  console.log('⏱️ Tempo máximo:', maxTime)

  // Tempo real: 1 minuto simulado = 1 segundo real (em velocidade 1x)
  // Atualiza a cada 100ms, então incrementa 0.1 minutos por vez
  const updateInterval = 100 // ms
  const timeStep = 0.1 // minutos simulados por update (= 100ms em tempo real)

  replayState.intervalId = setInterval(() => {
    if (!replayState.isPlaying) {
      clearInterval(replayState.intervalId)
      replayState.intervalId = null
      return
    }

    replayState.currentTime += timeStep * replayState.speed

    // Processar eventos até o tempo atual
    while (
      replayState.currentEventIndex < events.length &&
      events[replayState.currentEventIndex].t <= replayState.currentTime
    ) {
      replayState.processedEvents.push(events[replayState.currentEventIndex])
      replayState.currentEventIndex++
    }

    // Parar quando terminar
    if (replayState.currentTime >= maxTime) {
      replayState.currentTime = maxTime
      replayState.isPlaying = false
      clearInterval(replayState.intervalId)
      replayState.intervalId = null
    }
  }, updateInterval)
}

function resetSimulation() {
  // Limpar intervalo se estiver rodando
  if (replayState.intervalId) {
    clearInterval(replayState.intervalId)
    replayState.intervalId = null
  }

  simulationData.value = null
  isSimulating.value = false
  replayState.currentTime = 0
  replayState.isPlaying = false
  replayState.currentEventIndex = 0
  replayState.processedEvents = []
}
</script>

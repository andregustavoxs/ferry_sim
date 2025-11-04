<template>
  <div class="max-w-2xl mx-auto">
    <div class="rounded-lg shadow-lg border overflow-hidden transition-colors" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
      <!-- Header do Card -->
      <div class="bg-gradient-to-r from-ocean-500 to-ocean-600 px-6 py-5">
        <h2 class="text-2xl font-bold text-white">Configurar Simulação</h2>
        <p class="mt-1 text-ocean-100 text-sm">Defina os parâmetros para iniciar a simulação</p>
      </div>

      <!-- Formulário -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
        <!-- Número de Embarcações -->
        <div>
          <label for="vesselsNumber" class="block text-sm font-medium mb-2 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-700'">
            Número de Embarcações
          </label>
          <input
            id="vesselsNumber"
            v-model.number="form.vesselsNumber"
            type="number"
            min="1"
            max="10"
            required
            class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-ocean-500 focus:border-transparent transition-all"
            :class="isDark ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400' : 'bg-white border-gray-300 text-gray-900 placeholder-gray-400'"
            placeholder="Ex: 3"
          />
          <p class="mt-2 text-xs transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-500'">
            Quantidade de embarcações disponíveis para o sistema (1-10)
          </p>
        </div>

        <!-- Período de Partida -->
        <div>
          <label for="departurePeriod" class="block text-sm font-medium mb-2 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-700'">
            Período de Partida (minutos)
          </label>
          <input
            id="departurePeriod"
            v-model.number="form.departurePeriod"
            type="number"
            min="10"
            max="180"
            required
            class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-ocean-500 focus:border-transparent transition-all"
            :class="isDark ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400' : 'bg-white border-gray-300 text-gray-900 placeholder-gray-400'"
            placeholder="Ex: 60"
          />
          <p class="mt-2 text-xs transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-500'">
            Intervalo de tempo entre partidas de cada embarcação (10-180 minutos)
          </p>
        </div>

        <!-- Informações da Simulação -->
        <div class="border rounded-lg p-4 transition-colors" :class="isDark ? 'bg-slate-700/50 border-slate-600' : 'bg-blue-50 border-blue-200'">
          <h3 class="text-sm font-semibold mb-2 transition-colors" :class="isDark ? 'text-blue-400' : 'text-blue-900'">ℹ️ Informações da Simulação</h3>
          <ul class="text-xs space-y-1 transition-colors" :class="isDark ? 'text-slate-300' : 'text-blue-800'">
            <li>• Duração: 960 minutos (16 horas)</li>
            <li>• Capacidade por embarcação: 50 veículos</li>
            <li>• Tempo médio de travessia: 80 minutos</li>
            <li>• Veículos diários: 1200 (40% em horários de pico)</li>
          </ul>
        </div>

        <!-- Botão de Submit -->
        <button
          type="submit"
          class="w-full bg-gradient-to-r from-ocean-500 to-ocean-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-ocean-600 hover:to-ocean-700 focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:ring-offset-2 transition-all transform hover:scale-[1.02] active:scale-[0.98]"
        >
          🚀 Iniciar Simulação
        </button>
      </form>
    </div>

    <!-- Exemplos de Configuração -->
    <div class="mt-6 rounded-lg shadow border p-5 transition-colors" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
      <h3 class="text-sm font-semibold mb-3 transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">💡 Configurações Sugeridas</h3>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <button
          @click="applyPreset(3, 60)"
          class="text-left p-3 border rounded-lg transition-all"
          :class="isDark ? 'border-slate-600 hover:border-ocean-400 hover:bg-slate-700' : 'border-gray-200 hover:border-ocean-400 hover:bg-ocean-50'"
        >
          <div class="font-medium text-sm transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">Padrão</div>
          <div class="text-xs mt-1 transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-500'">3 embarcações, 60 min</div>
        </button>
        <button
          @click="applyPreset(2, 90)"
          class="text-left p-3 border rounded-lg transition-all"
          :class="isDark ? 'border-slate-600 hover:border-ocean-400 hover:bg-slate-700' : 'border-gray-200 hover:border-ocean-400 hover:bg-ocean-50'"
        >
          <div class="font-medium text-sm transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">Baixa Frequência</div>
          <div class="text-xs mt-1 transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-500'">2 embarcações, 90 min</div>
        </button>
        <button
          @click="applyPreset(5, 40)"
          class="text-left p-3 border rounded-lg transition-all"
          :class="isDark ? 'border-slate-600 hover:border-ocean-400 hover:bg-slate-700' : 'border-gray-200 hover:border-ocean-400 hover:bg-ocean-50'"
        >
          <div class="font-medium text-sm transition-colors" :class="isDark ? 'text-white' : 'text-gray-900'">Alta Frequência</div>
          <div class="text-xs mt-1 transition-colors" :class="isDark ? 'text-slate-400' : 'text-gray-500'">5 embarcações, 40 min</div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  isDark: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['start-simulation'])

const form = reactive({
  vesselsNumber: 3,
  departurePeriod: 60
})

function handleSubmit() {
  emit('start-simulation', {
    vesselsNumber: form.vesselsNumber,
    departurePeriod: form.departurePeriod
  })
}

function applyPreset(vessels, period) {
  form.vesselsNumber = vessels
  form.departurePeriod = period
}
</script>

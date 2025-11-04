<template>
  <div class="rounded-lg border p-8 transition-colors" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'">
    <h3 class="text-sm font-medium uppercase tracking-wide mb-6 transition-colors" :class="isDark ? 'text-slate-300' : 'text-gray-500'">Fila de Veículos</h3>
    <div class="relative" style="height: 400px;">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

// Registrar componentes do Chart.js
Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  events: {
    type: Array,
    required: true
  },
  isDark: {
    type: Boolean,
    default: false
  }
})

const chartCanvas = ref(null)
let chartInstance = null

function updateChart() {
  if (!chartCanvas.value) return

  // Extrair dados de fila dos eventos
  const queueData = props.events
    .filter(event => 'queue_size' in event)
    .map(event => ({
      time: Math.round(event.t),
      queueSize: event.queue_size
    }))

  // Remover duplicatas e ordenar
  const uniqueData = Array.from(
    new Map(queueData.map(item => [item.time, item])).values()
  ).sort((a, b) => a.time - b.time)

  const labels = uniqueData.map(d => `${d.time}min`)
  const data = uniqueData.map(d => d.queueSize)

  // Cores dinâmicas baseadas no tema
  const textColor = props.isDark ? 'rgb(203, 213, 225)' : 'rgb(75, 85, 99)' // slate-300 : gray-600
  const gridColor = props.isDark ? 'rgba(71, 85, 105, 0.3)' : 'rgba(0, 0, 0, 0.05)' // slate-600/30 : black/5

  if (chartInstance) {
    chartInstance.data.labels = labels
    chartInstance.data.datasets[0].data = data

    // Atualizar cores do tema
    chartInstance.options.scales.x.ticks.color = textColor
    chartInstance.options.scales.x.title.color = textColor
    chartInstance.options.scales.y.ticks.color = textColor
    chartInstance.options.scales.y.title.color = textColor
    chartInstance.options.scales.y.grid.color = gridColor

    chartInstance.update('none') // Update sem animação para performance
  } else {
    chartInstance = new Chart(chartCanvas.value, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Veículos na Fila',
          data,
          borderColor: 'rgb(14, 165, 233)',
          backgroundColor: 'rgba(14, 165, 233, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 4,
          pointHoverBackgroundColor: 'rgb(14, 165, 233)',
          pointHoverBorderColor: 'white',
          pointHoverBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: 'index'
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            cornerRadius: 8,
            titleColor: 'white',
            bodyColor: 'white',
            callbacks: {
              label: function(context) {
                return `Fila: ${context.parsed.y} veículos`
              }
            }
          }
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Tempo (minutos)',
              color: textColor,
              font: {
                size: 12,
                weight: 'bold'
              }
            },
            ticks: {
              maxTicksLimit: 10,
              color: textColor,
              font: {
                size: 10
              }
            },
            grid: {
              display: false
            }
          },
          y: {
            display: true,
            beginAtZero: true,
            title: {
              display: true,
              text: 'Veículos na Fila',
              color: textColor,
              font: {
                size: 12,
                weight: 'bold'
              }
            },
            ticks: {
              precision: 0,
              color: textColor,
              font: {
                size: 10
              }
            },
            grid: {
              color: gridColor
            }
          }
        }
      }
    })
  }
}

watch(() => props.events, updateChart, { deep: true })
watch(() => props.isDark, updateChart)

onMounted(() => {
  updateChart()
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>

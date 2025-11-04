# Ferry Simulation Dashboard

Dashboard profissional para visualização em tempo real da simulação de sistema de travessia de ferry.

## Estrutura do Projeto

```
ferry_sim/
├── src/                    # Backend (Python/Flask)
│   ├── main/
│   │   ├── server/        # Servidor Flask
│   │   └── routes/        # Rotas da API
│   ├── entities/          # Entidades da simulação
│   ├── use_cases/         # Casos de uso
│   └── settings/          # Configurações
├── frontend/              # Frontend (Vue.js)
│   ├── src/
│   │   ├── components/    # Componentes Vue
│   │   ├── App.vue        # Componente principal
│   │   └── main.js        # Ponto de entrada
│   └── package.json
└── requirements.txt       # Dependências Python
```

## Tecnologias Utilizadas

### Backend
- **Flask**: Framework web Python
- **SimPy**: Biblioteca de simulação de eventos discretos
- **Flask-CORS**: Habilitação de CORS para API

### Frontend
- **Vue 3**: Framework JavaScript (Composition API)
- **Vite**: Build tool e dev server
- **Chart.js**: Visualização de gráficos
- **Tailwind CSS**: Framework CSS para estilização
- **Axios**: Cliente HTTP

## Instalação e Execução

### Pré-requisitos
- Python 3.8+
- Node.js 18+
- npm ou yarn

### Backend (Flask)

1. Criar ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Executar servidor:
```bash
python3 app.py
```

O backend estará disponível em `http://localhost:8080`

### Frontend (Vue.js)

1. Navegar para a pasta frontend:
```bash
cd frontend
```

2. Instalar dependências:
```bash
npm install
```

3. Executar em modo desenvolvimento:
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

4. Build para produção:
```bash
npm run build
```

## Como Usar

1. **Abra o navegador** em `http://localhost:3000`

2. **Configure os parâmetros da simulação:**
   - **Número de Embarcações**: Quantidade de ferries disponíveis (1-10)
   - **Período de Partida**: Intervalo entre partidas em minutos (10-180)

3. **Inicie a simulação** clicando em "Iniciar Simulação"

4. **Visualize os dados em tempo real:**
   - 📊 **Gráfico de Fila**: Mostra o tamanho da fila ao longo do tempo
   - 🚢 **Estado das Embarcações**: Visualização do status de cada ferry
   - 📈 **Métricas**: KPIs como veículos processados, utilização média, etc.
   - 📋 **Eventos Recentes**: Log dos últimos eventos da simulação

5. **Controles de Replay:**
   - ▶️ **Play/Pause**: Controlar a reprodução
   - **Velocidade**: Ajustar velocidade (1x, 2x, 5x, 10x)
   - 🔄 **Reset**: Iniciar nova simulação

## Parâmetros da Simulação

### Configuráveis
- `vessels_number`: Número de embarcações (padrão: 3)
- `each_vessel_departure_period`: Período de partida em minutos (padrão: 60)

### Fixos (definidos em `src/settings/params.json`)
- **Capacidade por embarcação**: 50 veículos
- **Duração da simulação**: 960 minutos (16 horas)
- **Veículos diários**: 1200 (40% em horários de pico)
- **Horários de pico**:
  - Manhã: 60-180 min (1h-3h)
  - Tarde: 660-780 min (11h-13h)
- **Tempo médio de travessia**: 80 minutos
- **Tempo médio de embarque**: 15 minutos
- **Tempo médio de desembarque**: 0.25 minutos

## API Endpoints

### GET /simulate
Executa a simulação e retorna todos os eventos.

**Parâmetros Query:**
- `vessels_number` (int): Número de embarcações
- `each_vessel_departure_period` (int): Período de partida em minutos

**Resposta:**
```json
{
  "initial_parameters": {
    "vessels_number": 3,
    "each_vessel_departure_period": 60
  },
  "metrics": {},
  "events": [
    {
      "t": 12.5,
      "event_type": "arrival",
      "queue_size": 1
    },
    {
      "t": 15.2,
      "event_type": "boarding",
      "vessel_name": "Embarcação 1",
      "queue_size": 0,
      "vessel_used_capacity": 1
    }
  ]
}
```

**Tipos de Eventos:**
- `arrival`: Veículo chega à fila
- `boarding`: Veículo embarca em um ferry
- `departure`: Ferry parte com veículos
- `return`: Ferry retorna vazio ao porto

## Funcionalidades do Dashboard

### 1. Formulário de Configuração
- Interface intuitiva para definir parâmetros
- Validação de entrada
- Presets de configuração (Padrão, Baixa Frequência, Alta Frequência)

### 2. Métricas em Tempo Real
- Total de veículos processados
- Veículos embarcados (com percentual)
- Tamanho médio e máximo da fila
- Utilização média das embarcações
- Total de viagens realizadas
- Tempo simulado
- Contador de eventos

### 3. Visualizações
- **Gráfico de Linha**: Evolução da fila ao longo do tempo
- **Cards de Embarcações**: Status visual de cada ferry
  - ⚓ Disponível
  - 📦 Embarcando
  - 🚢 Navegando
  - 🔄 Retornando
- **Barra de Capacidade**: Indicador visual de lotação

### 4. Sistema de Replay
- Reprodução animada dos eventos
- Controles de play/pause
- Ajuste de velocidade
- Barra de progresso
- Reinício da simulação

### 5. Log de Eventos
- Tabela com últimos 20 eventos
- Informações detalhadas: tempo, tipo, embarcação, fila, capacidade
- Badges coloridos por tipo de evento

## Estrutura de Componentes Vue

### App.vue
Componente raiz que gerencia:
- Estado da simulação
- Chamada à API
- Sistema de replay
- Navegação entre formulário e dashboard

### SimulationForm.vue
Formulário de configuração com:
- Validação de campos
- Presets de configuração
- Informações sobre a simulação

### Dashboard.vue
Container principal que integra:
- Controles de replay
- Todos os componentes de visualização

### QueueChart.vue
Gráfico de linha mostrando evolução da fila usando Chart.js

### VesselsVisualization.vue
Visualização visual das embarcações com:
- Status em tempo real
- Barra de capacidade
- Indicadores coloridos

### MetricsPanel.vue
Grid de cards com métricas calculadas em tempo real

## Design e UX

- **Tema**: Light mode clean e profissional
- **Cores**: Paleta ocean (azuis suaves) para tema marítimo
- **Tipografia**: System fonts para melhor legibilidade
- **Responsivo**: Layout adaptável para desktop e mobile
- **Animações**: Transições suaves e indicadores visuais

## Troubleshooting

### Erro de CORS
Se encontrar erros de CORS, verifique:
1. Flask-CORS está instalado: `pip install Flask-CORS`
2. Backend está rodando na porta 8080
3. Frontend está configurado para fazer proxy para localhost:8080

### Gráficos não aparecem
1. Verifique se Chart.js foi instalado: `npm list chart.js`
2. Confirme que eventos estão sendo processados
3. Abra o console do navegador para ver erros

### Simulação não inicia
1. Verifique se backend está rodando
2. Confirme parâmetros estão dentro dos limites
3. Veja logs do Flask no terminal

## Performance

- **Replay otimizado**: Atualiza a cada 100ms
- **Gráficos eficientes**: Sem animação em updates para melhor performance
- **Eventos limitados**: Tabela mostra apenas últimos 20 eventos

## Próximas Melhorias

- [ ] Adicionar WebSocket para streaming real-time
- [ ] Gráfico de utilização de embarcações ao longo do tempo
- [ ] Exportar dados da simulação (CSV, JSON)
- [ ] Comparação entre múltiplas simulações
- [ ] Testes automatizados (Jest + Testing Library)
- [ ] Deploy em produção

## Licença

Projeto acadêmico - Universidade Federal

## Autor

Trabalho de Simulação de Software
Backend: Desenvolvido pelo colega
Frontend: Desenvolvido com Vue.js e Tailwind CSS

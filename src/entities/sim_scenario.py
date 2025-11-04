import simpy


import random
from typing import Dict


from src.entities.vessel import Vessel
from src.settings.config import PARAMS


class SimScenario:

    def __init__(self, entry_params: Dict[str, str]) -> None:

        self.log_events = {
            "initial_parameters": entry_params,
            "metrics": {},
            "events": []
        }

        self.env = simpy.Environment()

        self.vehicles_total = 0

        PEAK_TOTAL_TIME = sum([end - start for start, end in PARAMS.get("peak_times")])
        NORMAL_TOTAL_TIME = PARAMS.get("simulation_time") - PEAK_TOTAL_TIME

        PERCENT_PEAK_DAILY_ARRIVING_VEHICLES = PARAMS.get("percent_peak_daily_arriving_vehicles")
        PERCENT_NORMAL_DAILY_ARRIVING_VEHICLES = 1 - PERCENT_PEAK_DAILY_ARRIVING_VEHICLES

        DAILY_ARRIVING_VEHICLES = PARAMS.get("daily_arriving_vehicles")

        self.medium_vessel_capacity = PARAMS.get("medium_vessel_capacity")

        self.simulation_time = PARAMS.get("simulation_time")

        self.peak_times = PARAMS.get("peak_times")

        self.average_crossing_time = PARAMS.get("average_crossing_time")

        self.average_normal_arrival_time = NORMAL_TOTAL_TIME / (DAILY_ARRIVING_VEHICLES * PERCENT_NORMAL_DAILY_ARRIVING_VEHICLES)
        self.average_peak_arrival_time =  PEAK_TOTAL_TIME / (DAILY_ARRIVING_VEHICLES * PERCENT_PEAK_DAILY_ARRIVING_VEHICLES)

        # Tempo de serviço é apenas de embarque
        self.average_service_time = PARAMS.get("average_embark_time")

        self.average_disembark_time = PARAMS.get("average_disembark_time")

        # Parâmetros de entrada
        self.initial_vessels_number = int(entry_params.get("vessels_number"))
        self.each_vessel_departure_period = int(entry_params.get("each_vessel_departure_period"))

        self.vehicles = simpy.Store(self.env)
        self.available_vessels = simpy.FilterStore(self.env)

        for i in range(0, self.initial_vessels_number):

            self.available_vessels.put(
                Vessel(str(i))
            )
            
        
    
    def arrive_vehicle(self):

        """Processo de chegada de um veículo"""

        while True:

            arrival_time = random.expovariate(1 / self.average_normal_arrival_time)

            for start, end in self.peak_times:

                if self.env.now >= start and self.env.now <= end:
                
                    arrival_time = random.expovariate(1 / self.average_peak_arrival_time)
                    break
        
            yield self.env.timeout(arrival_time)

            yield self.vehicles.put("vehicle")

            self.vehicles_total += 1

            #print(f"Veiculo chegou em {self.env.now}")
            self.log_events["events"].append(
                {
                    "t": self.env.now,
                    "event_type": "arrival",
                    "queue_size": len(self.vehicles.items),
                }
            )

            self.env.process(self.embark_vehicle())
    
    def embark_vehicle(self):

        """Processo de embarque de um veículo"""

        # Seleciona um tempo de embarque aleatório baseado no tempo médio de embarque
        service_time = random.expovariate(1 / self.average_service_time)

        # Solicita um recurso (Embarcação)

        # O critério de seleção da embarcação é não estar lotado
        disponible_vessels = list(
            filter(
                lambda x: x.used_capacity < self.medium_vessel_capacity, 
                self.available_vessels.items
            )
        )

        if len(disponible_vessels) > 0:

            # O veiculo embarca em uma embarcação aleatória que não seja a com maior capacidade usada
            vessel = random.choice(disponible_vessels)

            # Reserva o espaço imediatamente para evitar sobrecarga
            vessel.used_capacity += 1

            # Simula o tempo de embarque
            yield self.env.timeout(service_time)

            # Remove veiculo da fila de veículos
            yield self.vehicles.get()

            #print(f"Embarcou um veículo no Ferry {vessel.name} em {self.env.now}")
            self.log_events["events"].append(
                    {
                        "t": self.env.now,
                        "event_type": "boarding",
                        "vessel_name": vessel.name,
                        "queue_size": len(self.vehicles.items),
                        "vessel_used_capacity": vessel.used_capacity,
                    }
                )

    
    def depart_vessel(self):

        """Processo de partida de uma embarcação"""

        while True:
            
            # Seleciona um tempo de travessia aleatório
            crossing_time = random.normalvariate(self.average_crossing_time, 10)

            # Simula o tempo do período de saída de cada embarcação
            yield self.env.timeout(
                self.each_vessel_departure_period
            )

            time = self.env.now

            # Embarcação que parte deve ter o máximo de veículos
            vessel = yield self.available_vessels.get(lambda x: x.used_capacity == max([vessel.used_capacity for vessel in self.available_vessels.items]))

            #print(f"Ferry {vessel.name} sai do porto em {self.env.now}, com {vessel.used_capacity} veiculos")
            self.log_events["events"].append(
                {
                    "t": time,
                    "event_type": "departure",
                    "vessel_name": vessel.name,
                    "queue_size": len(self.vehicles.items),
                    "vessel_used_capacity": vessel.used_capacity,
                }
            )

            vehicles_number = vessel.used_capacity
            vessel.used_capacity = 0

            idle_time = 2 * crossing_time + sum([random.expovariate(1 / self.average_disembark_time) for _ in range(vehicles_number)])

            self.env.process(self.return_vessel(vessel, idle_time))
        
    def return_vessel(self, vessel: Vessel, return_time: float):

        """Processo de retorno de uma embarcação
        """

        yield self.env.timeout(return_time)

        #print(f"Ferry {vessel.name} retornou em {self.env.now}")
        self.log_events["events"].append(
                {
                    "t": self.env.now,
                    "event_type": "return",
                    "vessel_name": vessel.name,
                    "queue_size": len(self.vehicles.items),
                }
            )

        yield self.available_vessels.put(vessel)
    
    def simulate(self) -> None:

        """Simula o cenário"""

        self.env.process(self.arrive_vehicle())
        self.env.process(self.depart_vessel())

        self.env.run(until=self.simulation_time)
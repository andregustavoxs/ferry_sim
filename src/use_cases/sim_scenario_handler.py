from src.entities.sim_scenario import SimScenario
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse

class SimScenarioHandler:

    def __init__(self):

        pass

    def execute(self, http_request: HttpRequest) -> HttpResponse:

        params = http_request.params

        sim_scenario = SimScenario(params)

        print(sim_scenario.available_vessels.items)

        sim_scenario.simulate()

        return HttpResponse(
            sim_scenario.log_events,
            200
        )


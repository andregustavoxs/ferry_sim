from flask import jsonify, request, Blueprint


from src.http_types.http_request import HttpRequest
from src.use_cases.sim_scenario_handler import SimScenarioHandler


sim_scenario_route_bp = Blueprint("sim_scenario_route", __name__)

@sim_scenario_route_bp.route("/simulate", methods=["GET"])
def simulate_scenario():

    sim_scenario_handler = SimScenarioHandler()

    http_request = HttpRequest(
        params=request.args
    )

    http_response = sim_scenario_handler.execute(http_request)

    return jsonify(http_response.body), http_response.status_code


from flask import Flask
from flask_cors import CORS

from src.main.routes.sim_scenario_routes import sim_scenario_route_bp

APP = Flask(__name__)
CORS(APP)

APP.register_blueprint(sim_scenario_route_bp)
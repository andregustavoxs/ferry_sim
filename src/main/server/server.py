from flask import Flask

from src.main.routes.sim_scenario_routes import sim_scenario_route_bp

APP = Flask(__name__)

APP.register_blueprint(sim_scenario_route_bp)
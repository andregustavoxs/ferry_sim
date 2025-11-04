import json
import os

SETTINGS_DIRPATH = os.path.dirname(
    os.path.abspath(__file__)
)

PARAMS_FILEPATH = os.path.join(
    SETTINGS_DIRPATH,
    "params.json"
)

PARAMS = json.load(
    open(PARAMS_FILEPATH, 'r')
)
import os
import requests
import pandas as pd
import logging
import json
import base64
from urllib.parse import urlparse
logging.basicConfig(level=logging.INFO)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_app_name(url):

    app_name = url.split("/")[-1]

    return app_name


def save_scenario_check(save_scenario_data: dict, payload: dict) -> dict:
    """
    Updates the payload with the information about saving a scenario. If any of the parameters for saving a scenario was not passed, it will be filled with the default value.

    Parameters:
    save_scenario_data (dict): A dictionary with the parameters for saving a scenario:
        - saveScenario (True/False), False by default
        - overwriteScenario (True/False), False by default
        - workspaceId (id of an existing workspace)
        - scenarioName 
    payload (dict): A dictionaty with the data that should be calculated

    Returns:
    dict: A dictionary containing input data and the information about saving a scenario.
    """
    save_scenario_parameters = ['saveScenario','overwriteScenario', 'workspaceId', 'scenarioName']
    save_scenario_default_values = {
        'saveScenario' : False,
        'overwriteScenario': False,
        'workspaceId': "",
        'scenarioName': ""
    }
    payload['saveScenarioParameters']  = {}
    for par in save_scenario_parameters:
        payload['saveScenarioParameters'].update({par: save_scenario_data.get(par, save_scenario_default_values[par])})
        if par == 'scenarioName' and payload['saveScenarioParameters']['scenarioName'] == '':
            payload['saveScenarioParameters'].update({par: save_scenario_default_values[par]})

    return payload

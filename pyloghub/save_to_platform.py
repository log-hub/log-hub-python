import logging
import os
logging.basicConfig(level=logging.INFO)
import webbrowser
from IPython.display import display, HTML
import ipywidgets as widgets
from pyloghub.sending_requests import get_workspace_entities

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_app_name(url):

    app_name = url.split("/")[-1]

    return app_name


def save_scenario_check(save_scenario_data: dict, payload: dict, application_name = "") -> dict:
    """
    Updates the payload with the information about saving a scenario. If any of the parameters for saving a scenario was not passed, it will be filled with the default value.

    Parameters:
    save_scenario_data (dict): A dictionary with the parameters for saving a scenario:
        - saveScenario (boolean): False by default
        - overwriteScenario (boolean): False by default
        - mergeWithExistingScenario (boolean): False by default
        - workspaceId (str): Id of an existing workspace
        - scenarioName (str): Scenario name
    payload (dict): A dictionaty with the data that should be calculated
    application_name (str): Application name

    Returns:
    dict: A dictionary containing input data and the information about saving a scenario.
    """
    save_scenario_parameters = ['saveScenario', 'overwriteScenario','workspaceId', 'scenarioName']
    save_scenario_default_values = {
        'saveScenario' : False,
        'overwriteScenario': False,
        'workspaceId': "",
        'scenarioName': ""
    }
    if 'supplychainmap' in application_name:
        save_scenario_parameters.insert(2, 'mergeWithExistingScenario')
        save_scenario_default_values.update({'mergeWithExistingScenario': False})
        save_scenario_default_values['saveScenario'] = True
    payload['saveScenarioParameters']  = {}
    for par in save_scenario_parameters:
        payload['saveScenarioParameters'].update({par: save_scenario_data.get(par, save_scenario_default_values[par])})

    return payload

def get_map_link(data, scenario_name):

    map_id = ''

    for line in data:
        if line['name'] == scenario_name and line['type'] == 'MAP':
            map_id = line['_id']
            workspace_id = line['workspaceId']
            break
    
    if  map_id == '':
        logging.info(f"There is not a map in the folder {scenario_name}")
    
    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/sca/platform/workspaces/" + workspace_id + "/maps/" + map_id
    
    return url

def create_the_button(workspace_id, api_key, entity_name):

    response_data = get_workspace_entities(workspace_id, api_key)
    map_link = get_map_link(response_data['data'], entity_name)

    # Define a function to open the map link
    def open_map(b):
        webbrowser.open(map_link)

    # Create a button
    button = widgets.Button(
        description="Open the map",
        button_style='succes',  # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Click to open the map',
        icon='map',  # (FontAwesome names without the `fa-` prefix)
        layout=widgets.Layout(width='200px', height='50px')
    )

    button.on_click(open_map)

    display(button)
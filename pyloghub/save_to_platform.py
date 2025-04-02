import logging
import os
logging.basicConfig(level=logging.INFO)
import webbrowser
from IPython.display import display, Javascript, HTML
import ipywidgets as widgets
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))

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

def get_entities_link(data, scenario_name):

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)

    entities_id = {}

    for line in data:
        if line['name'] == scenario_name and line['type'] == "MAP":
            entities_id['map'] = f"{LOG_HUB_API_SERVER}/sca/platform/workspaces/" + line['workspaceId'] + "/maps/" + line['_id']
        if line['name'] == scenario_name and line['type'] == "DASHBOARD":
            entities_id['dashboard'] = f"{LOG_HUB_API_SERVER}/sca/platform/workspaces/" + line['workspaceId'] + "/dashboards/" + line['_id']
        if line['name'] == scenario_name + " Input" and line['type'] == "DATASET":
            entities_id['inputDataset'] = f"{LOG_HUB_API_SERVER}/sca/platform/workspaces/" + line['workspaceId'] + "/datasets/" + line['_id']
        if line['name'] == scenario_name + " Output" and line['type'] == "DATASET":
            entities_id['outputDataset'] = f"{LOG_HUB_API_SERVER}/sca/platform/workspaces/" + line['workspaceId'] + "/datasets/" + line['_id']
    
    if  entities_id == {}:
        return None
    else:
        return entities_id

 
def create_button(links, texts):
    """
    Creates a clean, minimal button for Jupyter Notebook output that links to the specified URL.
 
    Parameters:
      link (str): The URL to open when the button is clicked.
      text (str): The text displayed on the button.
    """
    buttons_html = ""
    for link, text in zip(links, texts):
        button_html = f'''
            <a href="{link}" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
            <button style="
                font-family: 'Open Sans', sans-serif;
                font-weight: 600;
                background-color: #F7F8FA;
                color: #111;
                border: 1px solid #E5E7EB;
                padding: 10px 20px;
                font-size: 14px;
                letter-spacing: 0.5px;
                border-radius: 6px;
                transition: background-color 0.2s ease, box-shadow 0.2s ease;
                margin-bottom: 10px;
            "
            onmouseover="this.style.backgroundColor='#E5E7EB'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';"
            onmouseout="this.style.backgroundColor='#F7F8FA'; this.style.boxShadow='none';">
            {text}
            </button>
            </a>
            '''
        buttons_html += button_html

    display(HTML(buttons_html))

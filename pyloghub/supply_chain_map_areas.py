import os
import pandas as pd
import warnings
from typing import Optional
import logging
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types, convert_to_float, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_supply_chain_map_areas(areas: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
    """
    Creates a map of areas based on the given area information.

    This function takes a DataFrame of areas with their country, region and center latitude and longitude, along with an API key, 
    and creates a map of areas using the Log-hub Supply Chain Map service. 

    Parameters:
    areas (pd.DataFrame): A pandas DataFrame containing areas information.
        Each row should contain:
        - id (number): Identifier.
        - searchId (str): Area search id.
        - country (str):  Country name or country code of the area.
        - region (str): Region name.
        - name (str): Area name.
        - layer (str): Layer name for the area.
        - quantity (number): Numerical value that can be used to determine the color of an area on the map.
        - continent (str): Country and area continent.
        - countryRegionOne, countryRegionTwo (str): Continent's subregion and second subregion where country is located.
        - countryName (str): Country name.
        - centerLat, centerLong (number): Area's center point latitude and longitude.
        - population (number): Area population.
        - areaKm2 (number): Area in km2

    parameters (dict): A dictionary containg parameter 'detailLevel' (boolean). 

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.
    Returns:
    pd.DataFrame: A pandas DataFrame containg the passed area information and its length [km]. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    mandatory_columns = {'country': 'str', 'region': 'str'}
    optional_columns = {
        'searchId': 'str', 'name': 'str', 'layer': 'str', 'continent': 'str', 'countryRegionOne': 'str', 'countryRegionTwo': 'str', 'countryName': 'str'
        }
    optional_floats = ['id', 'quantity', 'centerLat', 'centerLong', 'population', 'areaKm2']

    # Validate and convert data types
    areas = validate_and_convert_data_types(areas, mandatory_columns, 'mandatory', 'areas')
    if not areas is None:
        areas = validate_and_convert_data_types(areas, optional_columns, 'optional', 'areas')
        if not areas is None:
            areas = convert_to_float(areas, optional_floats, 'optional')
            areas = convert_df_to_dict_excluding_nan(areas, optional_floats)
    if areas is None:
        return None

    url = create_url("supplychainmapareas")
    
    headers = create_headers(api_key)
    payload = {
        "areaData": areas,
        "parameters": parameters
    }
    
    payload = save_scenario_check(save_scenario, payload, "supplychainmapareas")
    
    response_data = post_method(url, payload, headers, "supply chain map areas")
    if response_data is None:
        return None
    else:
        areas_df = pd.DataFrame(response_data['areaResult'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return areas_df

def forward_supply_chain_map_areas_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapAreas.xlsx')
    areas_df = pd.read_excel(data_path, sheet_name='areas', usecols='A:O')

    parameters={
        'detailLevel': False
    }
    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'mergeWithExistingScenario': False,
        'scenarioName': 'Your scenario name'
    }

    return {'areas': areas_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
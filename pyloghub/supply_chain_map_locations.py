import os
import pandas as pd
import warnings
from typing import Optional
import sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types, convert_to_float, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_supply_chain_map_locations(addresses: pd.DataFrame, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
    """
    Creates a map of locations based on the given addresses.

    This function takes a DataFrame of addresses with their layer, quantity and descriptions, along with an API key, 
    and creates a map of locations using the Log-hub Supply Chain Map service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing addresses with their layer, quantity and descriptions.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Location name.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - layer (str): Visual settings of locations in the same layer can be adjusted together.
        - quantity (number): Numerical value affecting the size of the location symbol on the map.
        - nameDescription1, nameDescription2 (str): Additional location descriptions.

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    pd.DataFrame: A pandas DataFrame containg the addresses and their parsed latitude and longitude. Returns None if 
                  the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    mandatory_columns = {
            'name': 'str', 'country': 'str'
        }
    optional_columns = {'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'layer': 'str', 'nameDescription1': 'str', 'nameDescription2': 'str'}
    optional_floats = ['id', 'quantity']

    # Validate and convert data types
    addresses= validate_and_convert_data_types(addresses, mandatory_columns, 'mandatory')
    if not addresses is None:
        addresses = validate_and_convert_data_types(addresses, optional_columns, 'optional')
        if not addresses is None:
            addresses = convert_to_float(addresses, optional_floats, 'optional')
            addresses = convert_df_to_dict_excluding_nan(addresses, optional_floats)
    if addresses is None:
        return None

    url = create_url("supplychainmaplocations")
    
    headers = create_headers(api_key)
    payload = {
        "geocodingData": addresses,
    }
 
    payload = save_scenario_check(save_scenario, payload, "supplychainmaplocations")
    
    response_data = post_method(url, payload, headers, "supply chain map locations")

    if response_data is None:
        return None
    else:
        geocoding_result_df = pd.DataFrame(response_data['geocodingResult'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return geocoding_result_df

def forward_supply_chain_map_locations_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapLocationsAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:K', dtype={'postalCode': str})

    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'saveScenarioParameters': save_scenario}

def reverse_supply_chain_map_locations(coordinates: pd.DataFrame, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
    """
    Creates a map of locations based on the given coordinates.

    This function takes a DataFrame of coordinates with their layer, quantity and descriptions, along with an API key, 
    and creates a map of locations using the Log-hub Supply Chain Map service. 

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing coordinates with their layer, quantity and descriptions.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Location name.
        - latitude (number): Latitude of the location.
        - longitude (number): Longitude of the location.
        - layer (str): Visual settings of locations in the same layer can be adjusted together.
        - quantity (number): Numerical value affecting the size of the location symbol on the map.
        - nameDescription1, nameDescription2 (str): Additional location descriptions.

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    pd.DataFrame: A pandas DataFrame containg the coordinates. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    mandatory_columns = {'latitude':'float', 'longitude': 'float',}
    optional_columns = {'name': 'str', 'layer': 'str', 'nameDescription1': 'str', 'nameDescription2': 'str'}
    optional_floats = ['id', 'quantity']

    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, mandatory_columns, 'mandatory')
    if not coordinates is None:
        coordinates = validate_and_convert_data_types(coordinates, optional_columns, 'optional')
        if not coordinates is None:
            coordinates = convert_to_float(coordinates, optional_floats, 'optional')
            coordinates = convert_df_to_dict_excluding_nan(coordinates, optional_floats)
    if coordinates is None:
        return None

    url = create_url("reversesupplychainmaplocations")
    
    headers = create_headers(api_key)
    payload = {
        "geocodingData": coordinates,
    }
    
    payload = save_scenario_check(save_scenario, payload, "reversesupplychainmaplocations")
    response_data = post_method(url, payload, headers, "reverse supply chain map locations")
    if response_data is None:
        return None
    else:
        geocoding_data_df = pd.DataFrame(response_data['geocodingData'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return geocoding_data_df

def reverse_supply_chain_map_locations_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapLocationsReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:H')

    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'saveScenarioParameters': save_scenario}
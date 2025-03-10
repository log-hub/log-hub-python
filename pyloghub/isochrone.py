import os
import pandas as pd
import logging
from typing import Optional, Dict
import warnings
logging.basicConfig(level=logging.INFO)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_isochrone(addresses: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
    """
    Perform forward isochrone calculation on a list of addresses.

    This function takes a DataFrame of addresses, a dictionary of parameters and an API key, and calculates an
    isochrone using the Log-hub forward isochrone service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing the addresses to be geocoded.
        Required columns and their types:
        - name (str): The name of the isochrone.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
    
    parameters (dict): A dictionary containing parameters for isochrone calculation. 
        - isochroneType: "road" or "beeline"
        - distanceUnit: "km" or "mi"
        - profile: "driving-car" or "driving-hgv", used if isochroneType is "road"
        - duration: a number between 1 and 300, used if isochroneType is "road"
        - layer: a number between 1 and 10, used if isochroneType is "road"
        - distance: a number between 1 and 3000, used if isochroneType is "beeline"
        - layerBeeline: a number between 1 and 25, used if isochroneType is "beeline"

    api_key (str): The Log-hub API key for accessing the isochrone service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the original address information along 
                  with the geocoded results, cordinates, and information about area and population.
                  Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    mandatory_columns = {'name': 'str', 'country': 'str'}
    optional_columns = {'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'}

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, mandatory_columns, 'mandatory', 'addresses')
    if not addresses is None:
        addresses = validate_and_convert_data_types(addresses, optional_columns, 'optional', 'addresses')

    if addresses is None:
        return None
    
    url = create_url("isochrone")
    
    headers = create_headers(api_key)

    payload = {
        'geocodingData': addresses.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "isochrone")
    if response_data is None:
        return None
    else:
        geocoded_data_df = pd.DataFrame(response_data['geocodingResult'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return geocoded_data_df

def forward_isochrone_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'IsochroneSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:G').fillna("")
    parameters = {
        'isochroneType': 'road',
        'distanceUnit': 'km',
        'profile': 'driving-car',
        'duration': 40,
        'layers': 5,
        'distance': 3000,
        'layersBeeline': 5
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_isochrone(geocodes: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
    """
    Perform reverse isochrone calculation on a list of latitude and longitude coordinates.

    This function takes a DataFrame of geocodes (latitude and longitude), parameters and an API key, 
    and calculates isochrones using the Log-hub reverse isochrone service. 

    Parameters:
    geocodes (pd.DataFrame): A pandas DataFrame containing the geocodes to be reverse geocoded.
        Required columns and their types:
        - name (str): The name of the isochrone.
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.

    parameters (dict): A dictionary containing parameters for isochrone calculation. 
        - isochroneType: "road" or "beeline"
        - distanceUnit: "km" or "mi"
        - profile: "driving-car" or "driving-hgv", used if isochroneType is "road"
        - duration: A number between 1 and 300, used if isochroneType is "road"
        - layer: A number between 1 and 10, used if isochroneType is "road"
        - distance: A number between 1 and 3000, used if isochroneType is "beeline"
        - layerBeeline: A number between 1 and 25, used if isochroneType is "beeline"

    api_key (str): The Log-hub API key for accessing the reverse isochrone service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the original geocode information along 
                  with the reverse geocoded address results, area and population information. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    geocodes_columns = {'name': 'str', 'latitude': 'float', 'longitude': 'float'}

    # Validate and convert data types
    geocodes = validate_and_convert_data_types(geocodes, geocodes_columns, 'mandatory', 'coordinates')
    if geocodes is None:
        return None
    
    url = create_url("reverseisochrone")
    headers = create_headers(api_key)
    payload = {
        "geocodingData": geocodes.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "reverse isochrone")
    if response_data is None:
        return None
    else:
        result_df = pd.DataFrame(response_data['geocodingResult'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return result_df

def reverse_isochrone_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'IsochroneSampleDataReverse.xlsx')
    geocodes_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:D')

    parameters = {
        'isochroneType': 'road',
        'distanceUnit': 'km',
        'profile': 'driving-car',
        'duration': 40,
        'layers': 5,
        'distance': 3000,
        'layersBeeline': 5
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': geocodes_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
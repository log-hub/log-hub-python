import os
import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import logging
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities


def forward_center_of_gravity_plus(addresses: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate center of gravity plus based on a list of addresses, their weights, volumes, and revenues.

    This function takes a DataFrame of addresses with weights, volumes, and revenues, and a set of parameters,
    along with an API key, and performs center of gravity plus calculation using the Log-hub service.

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing addresses with their weights, volumes, and revenues.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - weight (float): Weight.
        - volume (float): Volume.
        - revenue (float): Revenue.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number), distanceUnit (enum: "km" or "mi"),
                        and importance factors (importanceWeight, importanceVolume, importanceRevenue).

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned addresses with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    mandatory_columns = {'country': 'str', 'weight': 'float', 'volume': 'float', 'revenue': 'float'}
    optional_columns = {'id': 'float', 'name': 'str',  'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'}

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, mandatory_columns, 'mandatory', 'addresses')
    if not addresses is None:
        addresses = validate_and_convert_data_types(addresses, optional_columns, 'optional', 'addresses')

    if addresses is None:
        return None

    url = create_url("centerofgravityplus")
    headers = create_headers(api_key)
    payload = {
        "addresses": addresses.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "center of gravity plus")
    if response_data is None:
        return None
    else:
        assigned_addresses_df = pd.DataFrame(response_data['assignedAddresses'])
        centers_df = pd.DataFrame(response_data['centers'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return assigned_addresses_df, centers_df

def forward_center_of_gravity_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'COGPlusSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:J', dtype={'postalCode': str})

    parameters = {
        "numberOfCenters": 3,
        "distanceUnit": "km",
        "importanceWeight": 5,
        "importanceVolume": 2,
        "importanceRevenue": 7
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_center_of_gravity_plus(coordinates: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate reverse center of gravity plus based on a list of coordinates, their weights, volumes, and revenues.

    This function takes a DataFrame of coordinates with weights, volumes, and revenues, and a set of parameters,
    along with an API key, and performs reverse center of gravity plus calculation using the Log-hub service.

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing geocodes with their weights, volumes, and revenues.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.
        - weight (float): Weight.
        - volume (float): Volume.
        - revenue (float): Revenue.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number), distanceUnit (enum: "km" or "mi"),
                        and importance factors (importanceWeight, importanceVolume, importanceRevenue).

    api_key (str): The Log-hub API key for accessing the reverse center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned geocodes with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    mandatory_columns = {'latitude': 'float', 'longitude': 'float', 'weight': 'float', 'volume': 'float', 'revenue': 'float'}
    optional_columns = {'id': 'float', 'name': 'str'}
    
    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, mandatory_columns, 'mandatory', 'coordinates')
    if not coordinates is None:
        coordinates = validate_and_convert_data_types(coordinates, optional_columns, 'optional', 'coordinates')

    if coordinates is None:
        return None

    url = create_url("reversecenterofgravityplus")
    
    headers = create_headers(api_key)
    payload = {
        "coordinates": coordinates.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "reverse center of gravity plus")
    if response_data is None:
        return None
    else:
        assigned_geocodes_df = pd.DataFrame(response_data['assignedGeocodes'])
        centers_df = pd.DataFrame(response_data['centers'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return assigned_geocodes_df, centers_df

def reverse_center_of_gravity_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'COGPlusSampleDataReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:G')

    parameters = {
        "numberOfCenters": 3,
        "distanceUnit": "km",
        "importanceWeight": 5,
        "importanceVolume": 2,
        "importanceRevenue": 7
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
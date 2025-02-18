import os
import pandas as pd
import warnings
from typing import Optional
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url

def forward_supply_chain_map_relations(addresses: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a map of relations based on the given addresses.

    This function takes a DataFrame of addresses pairs with their layers and quantity, along with an API key, 
    and creates a map of relations using the Log-hub Supply Chain Map service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing addresses pairs with their layers and quantity.
        Each row should contain:
        - id (number): Identifier.
        - senderName (str): Name for the start location of the relation.
        - senderCountry (str): Country code or country name for the start location of the relation. Must have at least 
                               1 character.
        - senderState (str): State code for the start location of the relation.
        - senderPostalCode (str): Postal code for the start location of the relation.
        - senderSity (str): City name for the start location of the relation.
        - senderStreet (str): Street name with house number for the start location of the relation.
        - senderLocationLayer (str): Layer name for the start location.
        - recipientName (str): Name for the end location of the relation.
        - recipientCountry (str): Country code or country name for the end location of the relation. Must have at least 
                               1 character.
        - recipientState (str): State code for the end location of the relation.
        - recipientPostalCode (str): Postal code for the end location of the relation.
        - recipientSity (str): City name for the end location of the relation.
        - recipientStreet (str): Street name with house number for the end location of the relation.
        - recipientLocationLayer (str): Layer name for the end location.
        - relationLayer (str): Layer name for the relation.
        - quantity (number): Numerical value affecting the thickness of the relation on the map.

    parameters (dict): A dictionary containing parameter 'showLocations' (boolean).

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the addresses pairs and their parsed latitude and longitude. Returns None if 
                  the process fails.
    """

    required_columns = {
            'id': 'float', 'senderName': 'str', 'senderCountry': 'str', 'senderState': 'str', 'senderPostalCode': 'str',
            'senderCity': 'str', 'senderStreet': 'str', 'senderLocationLayer': 'str', 'recipientName': 'str', 'recipientCountry': 'str', 'recipientState': 'str', 'recipientPostalCode': 'str', 'recipientCity': 'str', 'recipientStreet': 'str', 'recipientLocationLayer': 'str', 'relationLayer': 'str', 'quantity': 'string'
        }

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, required_columns)
    if addresses is None:
        return None

    url = create_url("supplychainmaprelations")
    headers = create_headers(api_key)
    payload = {
        "distanceCalculationData": addresses.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload, "supplychainmaprelations")
    
    response_data = post_method(url, payload, headers,"supply chain map relations")
    if response_data is None:
        return None
    else:
        distance_calculation_result_df = pd.DataFrame(response_data['distanceCalculationResult'])
        return distance_calculation_result_df

def forward_supply_chain_map_relations_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapRelationsAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:Q', dtype={'postalCode': str})

    parameters = {
        'showLocations': True
    }

    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_supply_chain_map_relations(coordinates: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a map of relations based on the given coordinates pairs.

    This function takes a DataFrame of coordinates pairs with their layers and quantity, along with an API key, 
    and creates a map of relations using the Log-hub Supply Chain Map service. 

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing coordinates pairs with their layers and quantity.
        Each row should contain:
        - id (number): Identifier.
        - senderName (str): Name for the start location of the relation.
        - senderLatitude (number): Latitude for the start location of the relation.
        - senderLongitude (number): Longitude for the start location of the relation.
        - senderLocationLayer (str): Layer name for the start location.
        - recipientName (str): Name for the end location of the relation.
        - recipientLatitude (number): Latitude for the end location of the relation.
        - recipientLongitude (number): Longitude for the end location of the relation.
        - recipientLocationLayer (str): Layer name for the end location.
        - relationLayer (str): Layer name for the relation.
        - quantity (number): Numerical value affecting the thickness of the relation on the map.

    parameters (dict): A dictionary containing parameter 'showLocations' (boolean).

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the coordinates pairs. Returns None if the process fails.
    """
    required_columns = {
            'id': 'float', 'senderName': 'str', 'senderLatitude':'float', 'senderLongitude': 'float', 'senderLocationLayer': 'str', 'recipientName': 'str', 'recipientLatitude':'float', 'recipientLongitude': 'float', 'recipientLocationLayer': 'str', 'relationLayer': 'str', 'quantity': 'str'
        }
    
    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, required_columns)
    if coordinates is None:
        return None

    url = create_url("reversesupplychainmaprelations")
    
    headers = create_headers(api_key)
    payload = {
        "distanceCalculationData": coordinates.to_dict(orient='records'),
        'parameters': parameters
    }
    
    payload = save_scenario_check(save_scenario, payload, "reversesupplychainmaprelations")
    
    response_data = post_method(url, payload, headers, "reverse supply chain map relations")
    if response_data is None:
        return None
    else:
        distance_calculation_result_df = pd.DataFrame(response_data['distanceCalculationData'])
        return distance_calculation_result_df

def reverse_supply_chain_map_relations_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapRelationsReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:K')

    parameters = {
        'showLocations': True
    }

    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
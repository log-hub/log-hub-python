import os
import pandas as pd
import warnings
from typing import Optional
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types, convert_to_float, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url

def forward_supply_chain_map_routes(addresses: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a map of routes based on the given route nodes addresses.

    This function takes a DataFrame of nodes addresses with their layer and pickup and delivery quantity, along with an API key, 
    and creates a map of routes using the Log-hub Supply Chain Map service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing nodes addresses with their layer and pickup and delivery quantity.
        Each row should contain:
        - id (number): Identifier.
        - routeId (str): A unique route id. All stops with the same routeId belong to the same route.
        - name (str): Name of the route node.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - layer (str): Visual settings of routes in the same layer can be adjusted together.
        - pickupQuantity (number): Quantity that is picked up at the node.
        - deliveryQuantity (number): Quantity that is delivered at the node.

    parameters (dict): A dictionary containing parameter 'streetLevel' (boolean). 

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the nodes addresses with their layer and pickup and delivery quantity.

    """

    mandatory_columns = {'routeId': 'str', 'name': 'str', 'country': 'str'}
    optional_columns = {'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'layer': 'str'}
    optional_floats = ['id', 'pickupQuantity', 'deliveryQuantity']
    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, mandatory_columns, 'mandatory')
    if not addresses is None:
        addresses = validate_and_convert_data_types(addresses, optional_columns, 'optional')
        if not addresses is None:
            addresses = convert_to_float(addresses, optional_floats, 'optional')
            addresses = convert_df_to_dict_excluding_nan(addresses, optional_floats)
    if addresses is None:
        return None

    url = create_url("supplychainmaproutes")
    
    headers = create_headers(api_key)
    payload = {
        "geocodingData": addresses,
        "parameters": parameters
    }
   
    payload = save_scenario_check(save_scenario, payload, "supplychainmaproutes")
    response_data = post_method(url, payload, headers, "supply chain map routes")
    if response_data is None:
        return None
    else: 
        route_result_df = pd.DataFrame(response_data['inputDataStructure'])
        return route_result_df
            
def forward_supply_chain_map_routes_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapRoutesAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:K', dtype={'postalCode': str})

    parameters = {
        'streetLevel': True
    }
    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_supply_chain_map_routes(coordinates: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a map of routes based on the given route nodes coordinates.

    This function takes a DataFrame of nodes coordinates with their layer and pickup and delivery quantity, along with an API key, 
    and creates a map of routes using the Log-hub Supply Chain Map service. 

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing coordinates with their layer and pickup and delivery quantity.
        Each row should contain:
        - id (number): Identifier.
        - routeId (str): A unique route id. All stops with the same routeId belong to the same route.
        - name (str): Name of the route node.
        - latitude (number): Latitude of the route node.
        - longitude (number): Longitude of the route node.
        - layer (str): Visual settings of routes in the same layer can be adjusted together.
        - pickupQuantity (number): Quantity that is picked up at the node.
        - deliveryQuantity (number): Quantity that is delivered at the node.
    
    parameters (dict): A dictionary containing parameter 'streetLevel' (boolean). 

    api_key (str): The Log-hub API key for accessing supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the route nodes coordinates. Returns None if the process fails.
    """

    mandatory_columns = {'routeId': 'str', 'name': 'str', 'latitude':'float', 'longitude': 'float'}
    optional_columns = {'layer': 'str'}
    optional_floats = ['id', 'pickupQuantity', 'deliveryQuantity']
    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, mandatory_columns, 'mandatory')
    if not coordinates is None:
        coordinates = validate_and_convert_data_types(coordinates, optional_columns, 'optional')
        if not coordinates is None:
            coordinates = convert_to_float(coordinates, optional_floats, 'optional')
            coordinates = convert_df_to_dict_excluding_nan(coordinates, optional_floats)
    if coordinates is None:
        return None
    url = create_url("reversesupplychainmaproutes")
    
    headers = create_headers(api_key)
    payload = {
        "routeLatLon": coordinates,
        "parameters": parameters
    }
    
    payload = save_scenario_check(save_scenario, payload, "reversesupplychainmaproutes")
    response_data = post_method(url, payload, headers, "reverse supply chain map routes")
    if response_data is None:
        return None
    else:
        route_result_df = pd.DataFrame(response_data['inputDataStructure'])
        return route_result_df
           
def reverse_supply_chain_map_routes_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapRoutesReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:H')

    parameters = {
        'streetLevel': True
    }
    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

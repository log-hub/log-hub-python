import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple
from pyloghub.save_to_platform import save_scenario_check, get_app_name

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

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the nodes addresses with their layer and pickup and delivery quantity.

    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'routeId': 'str', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str',
            'city': 'str', 'street': 'str', 'layer': 'str', 'pickupQuantity': 'float', 'deliveryQuantity': 'float'
        }
        for col, dtype in required_columns.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except Exception as e:
                    logging.error(f"Data type conversion failed for column '{col}': {e}")
                    return None
            else:
                logging.error(f"Missing required column: {col}")
                return None
        return df

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses)
    if addresses is None:
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/supplychainmaproutes"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "geocodingData": addresses.to_dict(orient='records'),
        "parameters": parameters
    }
    app_name = get_app_name(url)
    payload = save_scenario_check(save_scenario, payload, app_name)
    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                route_result_df = pd.DataFrame(response_data['inputDataStructure'])
                return route_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in supply chain map routes API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

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

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the route nodes coordinates. Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'routeId': 'str', 'name': 'str', 'latitude':'float', 'longitude': 'float', 'layer': 'str', 'pickupQuantity': 'float', 'deliveryQuantity': 'float'
        }
        for col, dtype in required_columns.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except Exception as e:
                    logging.error(f"Data type conversion failed for column '{col}': {e}")
                    return None
            else:
                logging.error(f"Missing required column: {col}")
                return None
        return df

    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates)
    if coordinates is None:
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversesupplychainmaproutes"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "routeLatLon": coordinates.to_dict(orient='records'),
        "parameters": parameters
    }
    app_name = get_app_name(url)
    payload = save_scenario_check(save_scenario, payload, app_name)
    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                route_result_df = pd.DataFrame(response_data['inputDataStructure'])
                return route_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in reverse supply chain map routes API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

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

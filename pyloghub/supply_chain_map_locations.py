import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple
from save_to_platform import save_scenario_check, get_app_name

def forward_supply_chain_map_locations(addresses: pd.DataFrame, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
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

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the addresses and their parsed latitude and longitude. Returns None if 
                  the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str',
            'city': 'str', 'street': 'str', 'layer': 'str', 'quantity': 'float', 'nameDescription1': 'str', 'nameDescription2': 'str'
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
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/supplychainmaplocations"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "geocodingData": addresses.to_dict(orient='records'),
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
                geocoding_result_df = pd.DataFrame(response_data['geocodingResult'])
                return geocoding_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in supply chain map locations API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

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

def reverse_supply_chain_map_locations(coordinates: pd.DataFrame, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
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

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the coordinates. Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'name': 'str', 'latitude':'float', 'longitude': 'float', 'layer': 'str', 'quantity': 'float', 'nameDescription1': 'str', 'nameDescription2': 'str'
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
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversesupplychainmaplocations"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "geocodingData": coordinates.to_dict(orient='records'),
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
                geocoding_result_df = pd.DataFrame(response_data['geocodingData'])
                return geocoding_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in reverse supply chain map locations API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

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
import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple
from save_to_platform import save_scenario_check, get_app_name

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

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the addresses pairs and their parsed latitude and longitude. Returns None if 
                  the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'senderName': 'str', 'senderCountry': 'str', 'senderState': 'str', 'senderPostalCode': 'str',
            'senderCity': 'str', 'senderStreet': 'str', 'senderLocationLayer': 'str', 'recipientName': 'str', 'recipientCountry': 'str', 'recipientState': 'str', 'recipientPostalCode': 'str', 'recipientCity': 'str', 'recipientStreet': 'str', 'recipientLocationLayer': 'str', 'relationLayer': 'str', 'quantity': 'string'
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
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/supplychainmaprelations"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "distanceCalculationData": addresses.to_dict(orient='records'),
        'parameters': parameters
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
                distance_calculation_result_df = pd.DataFrame(response_data['distanceCalculationResult'])
                return distance_calculation_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in center of gravity plus API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

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

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the coordinates pairs. Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'senderName': 'str', 'senderLatitude':'float', 'senderLongitude': 'float', 'senderLocationLayer': 'str', 'recipientName': 'str', 'recipientLatitude':'float', 'recipientLongitude': 'float', 'recipientLocationLayer': 'str', 'relationLayer': 'str', 'quantity': 'str'
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
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversesupplychainmaprelations"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "distanceCalculationData": coordinates.to_dict(orient='records'),
        'parameters': parameters
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
                distance_calculation_result_df = pd.DataFrame(response_data['distanceCalculationData'])
                return distance_calculation_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in center of gravity plus API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def reverse_supply_chain_map_relations_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapRelationsReverse.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:K', dtype={'postalCode': str})

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
    return {'coordinates': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

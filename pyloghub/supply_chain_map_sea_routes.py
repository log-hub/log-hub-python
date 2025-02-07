import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple
from pyloghub.save_to_platform import save_scenario_check, get_app_name

def forward_supply_chain_map_sea_routes(addresses: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a map of sea routes based on the given route UN/LOCODES.

    This function takes a DataFrame of routes UN/LOCODES with their quantity and route restrictions, along with an API key, 
    and creates a map of sea routes using the Log-hub Supply Chain Map service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing sea route UN/LOCODES with their quantity and route restrictions.
        Each row should contain:
        - id (number): Identifier.
        - fromName (str): Name for the start location of the sea route.
        - fronUnLocode (str): UN/LOCODE for the start location of the sea route.
        - toName (str): Name for the end location of the sea route.
        - toUnLocode (str): UN/LOCODE for the end location of the sea route.
        - quantity (number): Numerical value of goods being transferred through a specific sea route.
        - routingOptions (str): Restricting moving through channels, straits and passages based on the passed restrictions. 
                                Currently supported are Suez channel (as suez), Panama channel (as panama), Malacca strait (as malacca),
                                Gibraltar strait (as gibraltar), Dover strait (as dover), Bering strait (as bering), 
                                Magellan strait (as magellan), Bab-el-Mandeb strait (as babelmandeb), Kiel channel (as kiel), 
                                Corinth channel (as corinth), Northwest passage (as northwest) and Northeast passage (as northeast).
                                If multiple restrictions are named, comma or semicolon can be used as separators.

    parameters (dict): A dictionary containing parameter 'distanceUnit' (enum 'km' or 'mi' or 'nm'). 

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 
                        'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the sea route UN/LOCODES with their quantity and route restriction options, 
                  along with the parsed latitude and longitude, parsed country name and distance.

    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'fromName': 'str', 'fromUnLocode': 'str', 'toName': 'str', 'toUnLocode': 'str', 'quantity': 'float',
            'routingOptions': 'str'
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
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/supplychainmapsearoutes"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "seaRoutesAddressesData": addresses.to_dict(orient='records'),
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
                route_result_df = pd.DataFrame(response_data['seaRoutes'])
                return route_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in supply chain map sea routes API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_supply_chain_map_sea_routes_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapSeaRoutesAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:G')

    parameters = {
        'distanceUnit': 'nm'
    }
    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_supply_chain_map_sea_routes(coordinates: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a map of sea routes based on the given route latitude and longitude.

    This function takes a DataFrame of routes coordinates pairs with their quantity and route restrictions, along with an API key, 
    and creates a map of sea routes using the Log-hub Supply Chain Map service. 

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing sea route coordinates pairs with their quantity and route restrictions.
        Each row should contain:
        - id (number): Identifier.
        - fromName (str): Name for the start location of the sea route.
        - fromLatitude (number): Latitude of the start location.
        - fromLongitude (number): Longitude of the start location.
        - toName (str): Name for the end location of the sea route.
        - toLatitude (str): Latitude of the end location.
        - toLongitude (number): Longitude of the end location.
        - quantity (number): Numerical value of goods being transferred through a specific sea route.
        - routingOptions (str): Restricting moving through channels, straits and passages based on the passed restrictions. 
                                Currently supported are Suez channel (as suez), Panama channel (as panama), Malacca strait (as malacca),
                                Gibraltar strait (as gibraltar), Dover strait (as dover), Bering strait (as bering), 
                                Magellan strait (as magellan), Bab-el-Mandeb strait (as babelmandeb), Kiel channel (as kiel), 
                                Corinth channel (as corinth), Northwest passage (as northwest) and Northeast passage (as northeast).
                                If multiple restrictions are named, comma or semicolon can be used as separators.

    parameters (dict): A dictionary containing parameter 'distanceUnit' (enum 'km' or 'mi' or 'nm'). 

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 
                        'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the sea route coordinates pairs with their quantity and route restriction options, 
                  along with the parsed country name, parsed UN/LOCODES and distance.

    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'fromName': 'str', 'fromLatitude':'float', 'fromLongitude': 'float', 'toName': 'str', 'toLatitude': 'float', 'toLongitude': 'float', 'quantity': 'float', 'routingOptions': 'str'
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
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversesupplychainmapsearoutes"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "seaRoutesCoordinatesData": coordinates.to_dict(orient='records'),
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
                route_result_df = pd.DataFrame(response_data['seaRoutes'])
                return route_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in reverse supply chain map sea routes API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def reverse_supply_chain_map_sea_routes_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapSeaRoutesReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:I')

    parameters = {
        'distanceUnit': 'nm'
    }
    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

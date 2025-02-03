import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple
from save_to_platform import save_scenario_check

def forward_center_of_gravity_plus(addresses: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
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

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned addresses with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str',
            'city': 'str', 'street': 'str', 'weight': 'float', 'volume': 'float', 'revenue': 'float'
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
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/centerofgravityplus"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "addresses": addresses.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                assigned_addresses_df = pd.DataFrame(response_data['assignedAddresses'])
                centers_df = pd.DataFrame(response_data['centers'])
                return assigned_addresses_df, centers_df
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
    return {'addresses': addresses_df, 'parameters': parameters}


def reverse_center_of_gravity_plus(coordinates: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
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

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned geocodes with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float',
            'weight': 'float', 'volume': 'float', 'revenue': 'float'
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
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversecenterofgravityplus"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "coordinates": coordinates.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                assigned_geocodes_df = pd.DataFrame(response_data['assignedGeocodes'])
                centers_df = pd.DataFrame(response_data['centers'])
                return assigned_geocodes_df, centers_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in reverse center of gravity plus API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None


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
    return {'coordinates': coordinates_df, 'parameters': parameters}
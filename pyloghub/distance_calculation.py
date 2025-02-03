import os
import requests
import pandas as pd
import time
import logging
from typing import Optional, Dict
import warnings
from save_to_platform import save_scenario_check

logging.basicConfig(level=logging.INFO)

def forward_distance_calculation(address_pairs: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Calculate distances and durations between pairs of addresses.

    This function takes a DataFrame of address pairs (sender and recipient) and a set of parameters,
    along with an API key, and performs distance calculation using the Log-hub distance calculation service. 
    The function handles batching and rate limiting by the API.

    Parameters:
    address_pairs (pd.DataFrame): A pandas DataFrame containing pairs of addresses.
        Each row should contain:
        - senderCountry (str): Sender country code. Must have at least 1 character.
        - senderState (str): Sender state code.
        - senderPostalCode (str): Sender postal code.
        - senderCity (str): Sender city name.
        - senderStreet (str): Sender street name with house number.
        - recipientCountry (str): Recipient country code. Must have at least 1 character.
        - recipientState (str): Recipient state code.
        - recipientPostalCode (str): Recipient postal code.
        - recipientCity (str): Recipient city name.
        - recipientStreet (str): Recipient street name with house number.

    parameters (Dict): A dictionary containing parameters like distanceUnit (enum: "km" or "mi"),
                        durationUnit (enum: "min" or "sec" or "h"), vehicleType (enum: "truck" or "car") and 
                        routePreference (enum: 'recommended' or 'shortest' or 'fastest').

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    api_key (str): The Log-hub API key for accessing the distance calculation service.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the results of the distance calculations. 
                  Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'senderCountry': 'str', 'senderState': 'str', 'senderPostalCode': 'str',
            'senderCity': 'str', 'senderStreet': 'str', 'recipientCountry': 'str',
            'recipientState': 'str', 'recipientPostalCode': 'str',
            'recipientCity': 'str', 'recipientStreet': 'str'
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
    address_pairs = validate_and_convert_data_types(address_pairs)
    if address_pairs is None:
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/distancecalculation"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "addresses": address_pairs.to_dict(orient='records'), 
        "parameters": parameters,
        }
    payload = save_scenario_check(save_scenario, payload)

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                distance_calculation_df = pd.DataFrame(response_data)
                return distance_calculation_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in distance calculation API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_distance_calculation_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'DistanceCalcSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:J')

    parameters = {
        "distanceUnit": "km",
        "durationUnit": "min",
        "vehicleType": "car",
        "routePreference": "recommended"
    }
    return {'address_data': addresses_df, 'parameters': parameters}



def reverse_distance_calculation(geocodes: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Calculate distances and durations between pairs of locations based on coordinates.

    This function takes a DataFrame of geocode pairs (sender and recipient) with their locations and coordinates,
    a set of parameters, along with an API key, and performs reverse distance calculation using the 
    Log-hub reverse distance calculation service. The function handles batching and rate limiting by the API.

    Parameters:
    geocodes (pd.DataFrame): A pandas DataFrame containing pairs of geocodes with sender and recipient information.
        Each row should contain:
        - senderLocation (str): Sender location. Must have at least 1 character.
        - senderLatitude (float): Sender latitude.
        - senderLongitude (float): Sender longitude.
        - recipientLocation (str): Recipient location. Must have at least 1 character.
        - recipientLatitude (float): Recipient latitude.
        - recipientLongitude (float): Recipient longitude.

    parameters (Dict): A dictionary containing parameters like distanceUnit (enum: "km" or "mi"),
                        durationUnit (enum: "min" or "sec" or "h"), vehicleType (enum: "truck" or "car") and 
                        routePreference (enum: 'recommended' or 'shortest' or 'fastest').

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    api_key (str): The Log-hub API key for accessing the reverse distance calculation service.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the results of the reverse distance calculations.
                  Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'senderLocation': 'str', 'senderLatitude': 'float', 'senderLongitude': 'float',
            'recipientLocation': 'str', 'recipientLatitude': 'float', 'recipientLongitude': 'float'
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
    geocodes = validate_and_convert_data_types(geocodes)
    if geocodes is None:
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversedistancecalculation"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "geocodes": geocodes.to_dict(orient='records'),
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
                distance_calculation_df = pd.DataFrame(response_data)
                return distance_calculation_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in distance calculation API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None


def reverse_distance_calculation_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'DistanceCalcSampleDataReverse.xlsx')
    geocode_data_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:F')

    parameters = {
        "distanceUnit": "km",
        "durationUnit": "min",
        "vehicleType": "car",
        "routePreference": "recommended"
    }
    return {'geocode_data': geocode_data_df, 'parameters': parameters}
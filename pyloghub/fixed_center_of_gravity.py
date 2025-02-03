import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple
from save_to_platform import save_scenario_check

def forward_fixed_center_of_gravity(customers: pd.DataFrame, fixed_centers: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate fixed center of gravity based on a list of customers and their weights, and predefined fixed centers.

    This function takes a DataFrame of customers with weights, a DataFrame of fixed centers (if any), and a set of parameters,
    along with an API key, and performs fixed center of gravity calculation using the Log-hub service.

    Parameters:
    customers (pd.DataFrame): A pandas DataFrame containing customers with their weights.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name. Must have at least 1 character.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - weight (float): Weight.

    fixed_centers (pd.DataFrame): A pandas DataFrame containing predefined fixed centers.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name. Must have at least 1 character.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        This DataFrame can be empty.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number) and distanceUnit (enum: "km" or "mi").

    api_key (str): The Log-hub API key for accessing the fixed center of gravity service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned geocodes with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """
    
    def validate_and_convert_data_types(df, required_columns):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
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

    customer_columns = {
        'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str',
        'city': 'str', 'street': 'str', 'weight': 'float'
    }

    fixed_center_columns = {
        'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str',
        'city': 'str', 'street': 'str'
    }

    # Validate and convert data types for customers and fixed centers
    customers = validate_and_convert_data_types(customers, customer_columns)
    fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_columns) if not fixed_centers.empty else fixed_centers
    if customers is None or (not fixed_centers.empty and fixed_centers is None):
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/fixedcenterofgravity"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        "customers": customers.to_dict(orient='records'),
        "fixedCenters": fixed_centers.to_dict(orient='records') if not fixed_centers.empty else [],
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
                logging.error(f"Error in fixed center of gravity API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_fixed_center_of_gravity_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'FixedCOGSampleDataAddresses.xlsx')
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:H', dtype={'postalCode': str})
    fixedCenters_df = pd.read_excel(data_path, sheet_name='fixedCenters', usecols='A:G', dtype={'postalCode': str})

    parameters = {
        "numberOfCenters": 5,
        "distanceUnit": "km"
    }
    return {'customers': customers_df, 'fixedCenters': fixedCenters_df, 'parameters': parameters}


def reverse_fixed_center_of_gravity(customers: pd.DataFrame, fixed_centers: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate reverse fixed center of gravity based on a list of customers and their weights, and predefined fixed centers.

    This function takes a DataFrame of customers with weights, a DataFrame of fixed centers, and a set of parameters,
    along with an API key, and performs reverse fixed center of gravity calculation using the Log-hub service.

    Parameters:
    customers (pd.DataFrame): A pandas DataFrame containing customers with their weights.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - latitude (float): Latitude of the customer location.
        - longitude (float): Longitude of the customer location.
        - weight (float): Weight.

    fixed_centers (pd.DataFrame): A pandas DataFrame containing predefined fixed centers.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - latitude (float): Latitude of the fixed center location.
        - longitude (float): Longitude of the fixed center location.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number) and distanceUnit (enum: "km" or "mi").

    api_key (str): The Log-hub API key for accessing the reverse fixed center of gravity service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned geocodes with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """

    def validate_and_convert_data_types(df, required_columns):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
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

    customer_columns = {
        'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float', 'weight': 'float'
    }

    fixed_center_columns = {
        'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }

    # Validate and convert data types for customers and fixed centers
    customers = validate_and_convert_data_types(customers, customer_columns)
    fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_columns) if not fixed_centers.empty else fixed_centers
    if customers is None or (not fixed_centers.empty and fixed_centers is None):
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversefixedcenterofgravity"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        "customers": customers.to_dict(orient='records'),
        "fixedCenters": fixed_centers.to_dict(orient='records'),
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
                logging.error(f"Error in reverse fixed center of gravity API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None


def reverse_fixed_center_of_gravity_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'FixedCOGSampleDataReverse.xlsx')
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:E')
    fixedCenters_df = pd.read_excel(data_path, sheet_name='fixedCenters', usecols='A:D')

    parameters = {
        "numberOfCenters": 5,
        "distanceUnit": "km"
    }
    return {'customers': customers_df, 'fixedCenters': fixedCenters_df, 'parameters': parameters}
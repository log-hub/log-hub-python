import os
import requests
import pandas as pd
import time
import logging
from typing import Optional, Tuple
import warnings
logging.basicConfig(level=logging.INFO)
from save_to_platform import save_scenario_check

def validate_and_convert_data_types(df, required_columns):
    """
    Validate and convert the data types of the DataFrame columns.
    Log an error message if a required column is missing or if conversion fails.
    """
    for col, dtype in required_columns.items():
        if col not in df.columns:
            logging.error(f"Missing required column: {col}")
            return None
        try:
            df[col] = df[col].astype(dtype)
        except Exception as e:
            logging.error(f"Data type conversion failed for column '{col}': {e}")
            return None
    return df

def forward_nearest_warehouses(warehouses: pd.DataFrame, customers: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform forward nearest warehouses on a list of addresses.

    This function takes a DataFrame of addresses, parameters, and an API key, and performs forward
    nearest warehouses using the Log-hub service. 

    Parameters:
    warehouses (pd.DataFrame): A pandas DataFrame containing warehouses that should be considered in the calculation.
        Required columns and their types:
        - name (str): Warehouse name.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.

    customers (pd.DataFrame): A pandas DataFrame containing customers that should be considered in the calculation. 
        Required columns and their types:
        - name (str): Customer name.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.

    parametrs (dict): A dictionary containing parameters nearestWarehouses (an integer number), distanceUnit (enum 'km' or 'mi'), maxDistance (an integer number) and streetLevel (boolean)

    api_key (str): The Log-hub API key for accessing the nearest warehouses service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    Optional[Tuple[pd.DataFrame, pd.DataFrame]]: A pandas DataFrame containing information about the nearest warehouses for each 
                                                 customer, and a pandas DataFrame for unassigned customers. Returns None if the process fails.
    """
    warehouses_columns = {
        'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'
    }
    customer_columns = {
        'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'
    }

    # Validate and convert data types
    warehouses = validate_and_convert_data_types(warehouses, warehouses_columns)
    customers = validate_and_convert_data_types(customers, customer_columns)

    if any(df is None for df in [warehouses, customers]):
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/nearestwarehouses"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'warehouses': warehouses.to_dict(orient='records'),
        'customers': customers.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                nearest_warehouses_df = pd.DataFrame(response_data['nearestWarehouses'])
                unassigned_df = pd.DataFrame(response_data['unassignedCustomers'])
                return nearest_warehouses_df, unassigned_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in geocoding API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_nearest_warehouses_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'nearestWarehousesAddresses.xlsx')
    warehouses_df = pd.read_excel(data_path, sheet_name='warehouses', usecols='A:G').fillna("")
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:G').fillna("")
    parameters = {
        "nearestWarehouses": 3,
        "distanceUnit": "km",
        "maxDistance": 2000,
        "streetLevel": False
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'warehouses': warehouses_df, 'customers': customers_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_nearest_warehouses(warehouses: pd.DataFrame, customers: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform reverse nearest warehouses on a list of coordinates for warehouses and customers.

    This function takes a DataFrame of coordinates for warehouses and customers, parameters, and an API key, and performs reverse
    nearest warehouses using the Log-hub service. 

    Parameters:
    warehouses (pd.DataFrame): A pandas DataFrame containing warehouses that should be considered in the calculation.
        Required columns and their types:
        - name (str): Warehouse name.
        - latitude (number): Warehouse latitude.
        - longitude (number): Warehouse longitude.

    customers (pd.DataFrame): A pandas DataFrame containing customers that should be considered in the calculation. 
        Required columns and their types:
        - name (str): Customer name.
        - latitude (number): Customer latitude.
        - longitude (number): Customer longitude.

    parametrs (dict): A dictionary containing parameters nearestWarehouses (an integer number), distanceUnit (enum 'km' or 'mi'), maxDistance (an integer number) and streetLevel (boolean)

    api_key (str): The Log-hub API key for accessing the nearest warehouses service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    Optional[Tuple[pd.DataFrame, pd.DataFrame]]: A pandas DataFrame containing information about the nearest warehouses for each 
                                                 customer, and a pandas DataFrame for unassigned customers. Returns None if the process fails.
    """
    warehouses_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }
    customer_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }

    # Validate and convert data types
    warehouses = validate_and_convert_data_types(warehouses, warehouses_columns)
    customers = validate_and_convert_data_types(customers, customer_columns)

    if any(df is None for df in [warehouses, customers]):
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversenearestwarehouses"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'warehouses': warehouses.to_dict(orient='records'),
        'customers': customers.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                nearest_warehouses_df = pd.DataFrame(response_data['nearestWarehouses'])
                unassigned_df = pd.DataFrame(response_data['unassignedCustomers'])
                return nearest_warehouses_df, unassigned_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in geocoding API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def reverse_nearest_warehouses_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'nearestWarehousesReverse.xlsx')
    warehouses_df = pd.read_excel(data_path, sheet_name='warehouses', usecols='A:D').fillna("")
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:D').fillna("")
    parameters = {
        "nearestWarehouses": 3,
        "distanceUnit": "km",
        "maxDistance": 2000,
        "streetLevel": False
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'warehouses': warehouses_df, 'customers': customers_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

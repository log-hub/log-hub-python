import os
import requests
import pandas as pd
import time
import logging
from typing import Optional, Tuple
import warnings
logging.basicConfig(level=logging.INFO)
from save_to_platform import save_scenario_check

def convert_dates(df, date_columns):
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
        return df
    
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

def forward_freight_shipment_emissions_rail(addresses: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Perform forward freignt emissions by rail on a list of UN/LOCODEs.

    This function takes a DataFrame of UN/LOCODEs and an API key, and performs forward
    freight emissions by rail using the Log-hub service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing the UN/LOCODEs for calculating a CO2 footprint based on your shipments or route legs defined as separate shipments.
        Required columns and their types:
        - shipmentId (str): Unique identifier for each shipment.
        - shipmentDate (str): Dates related to the shipment (Format: YYYY-MM-DD)
        - fromUICCode (str): UN/LOCODE for the shipment's start location.
        - toUICCode (str): UN/LOCODE for the shipment's end location.
        - isRefrigirated (str): A YES/NO option that specifies whether the content being transferred through the shipments is refrigirated or not. If not specified will be taken as NO.
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - fuelType: enum "diesel", "electricity" or "other"
        - weightUnit: enum "kilograms" or "LBS"

    api_key (str): The Log-hub API key for accessing the freight emissions service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    Optional[pd.DataFrame]: A pandas DataFrame contains the original shipment information along 
                  with the calculated CO2 emissions. Returns None if the process fails.
    """
        
    addresses_columns = {
        'shipmentId': 'str', 'shipmentDate': 'str', 'fromUICCode': 'str', 'toUICCode': 'str', 'weight': 'float'
    }

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, addresses_columns)
    addresses = convert_dates(addresses, ['shipmentDate'])
    if addresses is None:
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/co2emissionsrail"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'freightShipmentEmissionsByTrain': addresses.to_dict(orient='records'),
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
                freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputTrain'])
                return freight_emissions_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in freight emission by rail API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_freight_shipment_emissions_rail_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2RailAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:F').fillna("")
    parameters = {
        "fuelType": "diesel",
        "weightUnit": "kilograms"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_freight_shipment_emissions_rail(coordinates: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Perform reverse freignt emissions by rail on a list of coordinates.

    This function takes a DataFrame of coordinates and an API key, and performs forward
    freight emissions by rail using the Log-hub service. 

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing the coordinates for calculating a CO2 footprint based on your shipments or route legs defined as separate shipments.
        Required columns and their types:
        - shipmentId (str): Unique identifier for each shipment.
        - shipmentDate (str): Dates related to the shipment (Format: YYYY-MM-DD)
        - fromLatitude (number): The latitude of the coordinate from which a shipment should be sent.
        - fromLongitude(number): The longitude of the coordinate from which a shipment should be sent.
        - toLatitude (number): The latitude of the coordinate to which a shipment should arrive at.
        - toLongitude (numebr): The longitude of the coordinate to which a shipment should arrive at.
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - fuelType: enum "diesel", "petrol", "hybrid", "CNG", "LPG", "pluginHybrid", "electricity" or "other"
        - weightUnit: enum "kilograms" or "LBS"

    api_key (str): The Log-hub API key for accessing the reverse freight emissions service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    Optional[pd.DataFrame]: A pandas DataFrame containing the original coordinates information along 
                  with the calculated CO2 emissions. Returns None if the process fails.
    """
    
    coordinates_columns = {
        'shipmentId': 'str', 'shipmentDate': 'str', 'fromLatitude': 'float', 'fromLongitude': 'float', 'toLatitude': 'float', 'toLongitude': 'float', 'weight': 'float'
    }

    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, coordinates_columns)
    coordinates = convert_dates(coordinates, ['shipmentDate'])
    if coordinates is None:
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reverseco2emissionsrail"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'freightShipmentEmissionsByTrainReverse': coordinates.to_dict(orient='records'),
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
                freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputTrain'])
                return freight_emissions_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in freight emission by road API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def reverse_freight_shipment_emissions_rail_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2RailReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:H').fillna("")
    parameters = {
        "fuelType": "diesel",
        "weightUnit": "kilograms"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

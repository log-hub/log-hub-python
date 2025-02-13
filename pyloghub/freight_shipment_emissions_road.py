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

def forward_freight_shipment_emissions_road(addresses: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform forward freight emissions by road on a list of addresses.

    This function takes a DataFrame of addresses and an API key, and performs forward
    freight emissions by road using the Log-hub service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing the addresses for calculating a CO2 footprint based on your shipments or route legs defined as separate shipments.
        Required columns and their types:
        - shipmentId (str): Unique identifier for each shipment.
        - shipmentDate (str): Dates related to the shipment (Format: YYYY-MM-DD)
        - fromCountry (str): Country code of the address from which a shipment should be sent.
        - fromState (str): State code of the address from which a shipment should be sent.
        - fromPostalCode (str): Postal code of the address from which a shipment should be sent.
        - fromCity (str): City name of the address from which a shipment should be sent.
        - fromStreet (str): Street name with house number of the address from which a shipment should be sent.
        - toCountry (str): Country code of the address to which a shipment should arrive at.
        - toState (str): State code of the address to which a shipment should arrive at.
        - toPostalCode (str): Postal code of the address to which a shipment should arrive at.
        - toCity (str): City name of the address to which a shipment should arrive at.
        - toStreet (str): Street name with house number of the address to which a shipment should arrive at.
        - isRefrigirated (str): A YES/NO option that specifies whether the content being transferred through the shipments is refrigirated or not. If not specified will be taken as NO.
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - vehicleType: "van(0-3.5)", "truck", "truckUrbanTruck", "truckMGV", "truckHGV", "truckRigid(3.5-7.5)", "truckRigid(7.5-12)", "truckRigid(12-20)" , "truckRigid(20-26)", "truckRigid(26-32)", "truckArticulated(3.5-34)", "truckArticulated(34-40)", "truckArticulated(40-44)", "truckArticulated(44-60)", "truckArticulated(60-72)", "truckGeneral", "truckAutoCarrier", "truckDray", "truckExpedited", "truckFlatbed", "truckHeavybulk", "truckLTL", "truckMixed", "truckMoving", "truckPackage", "truckSpecialized", "truckTanker" or "truckTL" 
        - fuelType: enum "diesel", "petrol", "hybrid", "CNG", "LPG", "pluginHybrid", "electricity" or "other"
        - weightUnit: enum "kilograms" or "lbs"
        - emissionStandard: enum "EURO_5" or :EURO_6"

    api_key (str): The Log-hub API key for accessing the freight emissions service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    Optional[Tuple[pd.DataFrame, pd.DataFrame]]: One pandas DataFrame contains the original address information along 
                  with the calculated CO2 emissions, and the second one contains shipments with no CO2 emission calculated. Returns None if the process fails.
    """
        
    addresses_columns = {
        'shipmentId': 'str', 'shipmentDate': 'str', 'fromCountry': 'str', 'fromState': 'str', 'fromPostalCode': 'str', 'fromCity': 'str', 'fromStreet': 'str', 'toCountry': 'str', 'toState': 'str', 'toPostalCode': 'str', 'toCity': 'str', 'toStreet': 'str', 'isRefrigirated': 'str', 'weight': 'float'
    }

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, addresses_columns)
    addresses = convert_dates(addresses, ['shipmentDate'])
    if addresses is None:
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/co2emissionsroad"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'freightShipmentEmissionsByRoad': addresses.to_dict(orient='records'),
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
                freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputStandardRoad'])
                not_evaluated_df  = pd.DataFrame(response_data['notEvaluatedShipmentsStandardRoad'])
                return freight_emissions_df, not_evaluated_df
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

def forward_freight_shipment_emissions_road_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2RoadAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:O').fillna("")
    parameters = {
        "vehicleType": "truck",
        "fuelType": "diesel",
        "weightUnit": "kilograms",
        "emissionStandard": "EURO_6"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_freight_shipment_emissions_road(coordinates: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform reverse freight emissions by road on a list of coordinates.

    This function takes a DataFrame of coordinates and an API key, and performs forward
    freight emissions by road using the Log-hub service. 

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing the coordinates for calculating a CO2 footprint based on your shipments or route legs defined as separate shipments.
        Required columns and their types:
        - shipmentId (str): Unique identifier for each shipment.
        - shipmentDate (str): Dates related to the shipment (Format: YYYY-MM-DD)
        - fromLatitude (number): The latitude of the coordinate from which a shipment should be sent.
        - fromLongitude(number): The longitude of the coordinate from which a shipment should be sent.
        - toLatitude (number): The latitude of the coordinate to which a shipment should arrive at.
        - toLongitude (numebr): The longitude of the coordinate to which a shipment should arrive at.
        - isRefrigirated (str): A YES/NO option that specifies whether the content being transferred through the shipments is refrigirated or not. If not specified will be taken as NO.
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - vehicleType: "van(0-3.5)", "truck", "truckUrbanTruck", "truckMGV", "truckHGV", "truckRigid(3.5-7.5)", "truckRigid(7.5-12)", "truckRigid(12-20)" , "truckRigid(20-26)", "truckRigid(26-32)", "truckArticulated(3.5-34)", "truckArticulated(34-40)", "truckArticulated(40-44)", "truckArticulated(44-60)", "truckArticulated(60-72)", "truckGeneral", "truckAutoCarrier", "truckDray", "truckExpedited", "truckFlatbed", "truckHeavybulk", "truckLTL", "truckMixed", "truckMoving", "truckPackage", "truckSpecialized", "truckTanker" or "truckTL" 
        - fuelType: enum "diesel", "petrol", "hybrid", "CNG", "LPG", "pluginHybrid", "electricity" or "other"
        - weightUnit: enum "kilograms" or "lbs"
        - emissionStandard: enum "EURO_5" or :EURO_6"

    api_key (str): The Log-hub API key for accessing the reverse freight emissions service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    Optional[Tuple[pd.DataFrame, pd.DataFrame]]: One pandas DataFrame contains the original coordinates information along 
                  with the calculated CO2 emissions, and the second one contains shipments with no CO2 emission calculated. Returns None if the process fails.
    """

    coordinates_columns = {
        'shipmentId': 'str', 'shipmentDate': 'str', 'fromLatitude': 'float', 'fromLongitude': 'float', 'toLatitude': 'float', 'toLongitude': 'float', 'isRefrigirated': 'str', 'weight': 'float'
    }

    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, coordinates_columns)
    coordinates = convert_dates(coordinates, ['shipmentDate'])
    if coordinates is None:
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reverseco2emissionsroad"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'freightShipmentEmissionsByRoad': coordinates.to_dict(orient='records'),
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
                freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputReverseRoad'])
                not_evaluated_df  = pd.DataFrame(response_data['notEvaluatedShipmentsReverseRoad'])
                return freight_emissions_df, not_evaluated_df
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

def reverse_freight_shipment_emissions_road_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2RoadReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:I').fillna("")
    parameters = {
        "vehicleType": "truck",
        "fuelType": "diesel",
        "weightUnit": "kilograms",
        "emissionStandard": "EURO_6"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
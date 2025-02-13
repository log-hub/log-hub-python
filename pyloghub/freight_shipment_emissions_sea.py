import os
import requests
import pandas as pd
import time
import logging
from typing import Optional
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

def forward_freight_shipment_emissions_sea(un_locodes: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Perform forward freight emissions by sea on a list of UN/LOCODEs.

    This function takes a DataFrame of UN/LOCODEs and an API key, and performs forward
    freight emissions by sea using the Log-hub service. 

    Parameters:
    un_locodes (pd.DataFrame): A pandas DataFrame containing the UN/LOCODEs for calculating a CO2 footprint based on your shipments or route legs defined as separate shipments.
        Required columns and their types:
        - shipmentId (str): Unique identifier for each shipment.
        - shipmentDate (str): Dates related to the shipment (Format: YYYY-MM-DD)
        - fromUnLocode (str): UN/LOCODE for the shipment's start location.
        - toUnLocode (str): UN/LOCODE for the shipment's end location.
        - vesselId (str): The 7 digit IMO (International Maritime Organization) ship identifier of the cargo ships.
        - isRefrigirated (str): A YES/NO option that specifies whether the content being transferred through the shipments is refrigirated or not. If not specified will be taken as NO.
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - shipType: enum "shipBulkCarrierAvg", "shipBulkCarrier(0-10k)", "shipBulkCarrier(10-100k)", "shipBulkCarrier(>100k)",
        "shipBulkCarrierGeneralCargo", "shipBulkCarrierGeneralCargo(0-10k)", "shipBulkCarrierGeneralCargo(10-20k)", "shipContainerShipAvg", "shipRoRoFerry" or "shipRoPaxFerry"
        - weightUnit: enum "kilograms" or "lbs" or "teu"

    api_key (str): The Log-hub API key for accessing the freight emissions service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    Optional[pd.DataFrame]: A pandas DataFrame contains the original shipment information along 
                  with the calculated CO2 emissions. Returns None if the process fails.
    """
        
    un_locodes_columns = {
        'shipmentId': 'str', 'shipmentDate': 'str', 'fromUnLocode': 'str', 'toUnLocode': 'str', 'vesselId': 'str', 'isRefrigirated': 'str', 'weight': 'float'
    }

    # Validate and convert data types
    un_locodes = validate_and_convert_data_types(un_locodes, un_locodes_columns)
    un_locodes = convert_dates(un_locodes, ['shipmentDate'])
    if un_locodes is None:
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/co2emissionssea"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'freightShipmentEmissionsBySea': un_locodes.to_dict(orient='records'),
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
                freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputSea'])
                return freight_emissions_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in freight emission by sea API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_freight_shipment_emissions_sea_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2Sea.xlsx')
    un_locodes_df = pd.read_excel(data_path, sheet_name='sea', usecols='A:H').fillna("")
    parameters = {
        "shipType": "shipContainerShipAvg",
        "weightUnit": "teu"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'unLocodes': un_locodes_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

if __name__ == "__main__":

    api_key_dev = "e75d5db6ca8e6840e185bc1c63f20f39e65fbe0b"
    workspace_id = "7cb180c0d9e15db1a71342df559d19d473c539ad"

    sample = forward_freight_shipment_emissions_sea_sample_data()

    sea = sample['unLocodes']
    par = sample['parameters']
    save_scenario = sample['saveScenarioParameters']
    save_scenario['saveScenario'] = True
    save_scenario['workspaceId'] = workspace_id
    save_scenario['scenarioName'] = 'CO2 sea'

    out = forward_freight_shipment_emissions_sea(sea, par, api_key_dev, save_scenario)

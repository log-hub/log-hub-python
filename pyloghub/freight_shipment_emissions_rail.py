import os
import pandas as pd
import logging
from typing import Optional
import warnings
logging.basicConfig(level=logging.INFO)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import convert_dates, validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url

def forward_freight_shipment_emissions_rail(addresses: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Perform forward freight emissions by rail on a list of UN/LOCODEs.

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
        - weightUnit: enum "kilograms" or "lbs"

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
    if not addresses is None:
        addresses = convert_dates(addresses, ['shipmentDate'])
    else:
        return None
    
    url = create_url("co2emissionsrail")
    
    headers = create_headers(api_key)

    payload = {
        'freightShipmentEmissionsByTrain': addresses.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "co2 emissions rail")
    if response_data is None:
        return None
    else:
        freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputTrain'])
        return freight_emissions_df

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
    Perform reverse freight emissions by rail on a list of coordinates.

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
        - weightUnit: enum "kilograms" or "lbs"

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
    if not coordinates is None:
        coordinates = convert_dates(coordinates, ['shipmentDate'])
    if coordinates is None:
        return None
    
    url = create_url("reverseco2emissionsrail")
    
    headers = create_headers(api_key)

    payload = {
        'freightShipmentEmissionsByTrainReverse': coordinates.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "reverse co2 emissions rail")
    if response_data is None:
        return None
    else:
            freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputTrain'])
            return freight_emissions_df

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

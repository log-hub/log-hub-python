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

def forward_freight_shipment_emissions_air(iata_codes: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Perform forward freight emissions by air on a list of IATA Codes.

    This function takes a DataFrame of IATA Codes and an API key, and performs forward
    freight emissions by air using the Log-hub service. 

    Parameters:
    iata_codes (pd.DataFrame): A pandas DataFrame containing the IATA Codes for calculating a CO2 footprint based on your shipments or route legs defined as separate shipments.
        Required columns and their types:
        - shipmentId (str): Unique identifier for each shipment.
        - shipmentDate (str): Dates related to the shipment (Format: YYYY-MM-DD)
        - fromIataCode (str): IATA Code for the shipment's start location.
        - toIataCode (str): IATA Code for the shipment's end location.
        - flightNumber (str): A flight number is a code for any airline service.
        - isRefrigirated (str): A YES/NO option that specifies whether the content being transferred through the shipments is refrigirated or not. If not specified will be taken as NO.
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - weightUnit: enum "kilograms" or "lbs"

    api_key (str): The Log-hub API key for accessing the freight emissions service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    Optional[pd.DataFrame]: A pandas DataFrame contains the original shipment information along 
                  with the calculated CO2 emissions. Returns None if the process fails.
    """
        
    iata_codes_columns = {
        'shipmentId': 'str', 'shipmentDate': 'str', 'fromIataCode': 'str', 'toIataCode': 'str', 'flightNumber': 'str', 'isRefrigirated': 'str', 'weight': 'float'
    }

    # Validate and convert data types
    iata_codes = validate_and_convert_data_types(iata_codes, iata_codes_columns)
    if not iata_codes is None:
        iata_codes = convert_dates(iata_codes, ['shipmentDate'])
    if iata_codes is None:
        return None
    
    url = create_url("co2emissionsair")
    
    headers = create_headers(api_key)

    payload = {
        'freightShipmentEmissionsByAir': iata_codes.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "co2 emissions air")
    if response_data is None:
        return None
    else:
        freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputAir'])
        return freight_emissions_df

def forward_freight_shipment_emissions_air_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2Air.xlsx')
    iata_codes_df = pd.read_excel(data_path, sheet_name='air', usecols='A:H').fillna("")
    parameters = {
        "weightUnit": "kilograms"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'iataCodes': iata_codes_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
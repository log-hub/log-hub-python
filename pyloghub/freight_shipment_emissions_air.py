import os
import pandas as pd
import logging
from typing import Optional
import warnings
logging.basicConfig(level=logging.INFO)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import convert_dates, validate_and_convert_data_types, convert_to_float, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_freight_shipment_emissions_air(iata_codes: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
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
        - isRefrigirated (str): A YES/NO option that specifies whether the content being transferred through the shipments is refrigirated or not. If not specified will be taken as NO.
        -distance (number): Distance between sender and recipient. If not provided, the distance will be calculated.
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - weightUnit: enum "kilograms" or "lbs"
        - planeType: enum "average", "freighter" or "bellyFreight"
        - refrigerantFactor: a number between 0 and 100 

    api_key (str): The Log-hub API key for accessing the freight emissions service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Optional[pd.DataFrame]: A pandas DataFrame contains the original shipment information along 
                  with the calculated CO2 emissions. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    iata_codes_mandatory_columns = {'shipmentId': 'str', 'shipmentDate': 'str', 'fromIataCode': 'str', 'toIataCode': 'str', 'weight': 'float'}
    iata_codes_optional_columns = {'isRefrigirated': 'str'}
    iata_codes_optional_floats = ['distance']

    # Validate and convert data types
    iata_codes = validate_and_convert_data_types(iata_codes, iata_codes_mandatory_columns, 'mandatory', 'iata codes')
    if not iata_codes is None:
        iata_codes = validate_and_convert_data_types(iata_codes, iata_codes_optional_columns, 'optional', 'iata codes')
        if not iata_codes is None:
            iata_codes = convert_dates(iata_codes, ['shipmentDate'])
            iata_codes = convert_to_float(iata_codes, iata_codes_optional_floats, 'optional')
            iata_codes = convert_df_to_dict_excluding_nan(iata_codes, iata_codes_optional_floats)
    if iata_codes is None:
        return None
    
    url = create_url("co2emissionsair")
    
    headers = create_headers(api_key)

    payload = {
        'freightShipmentEmissionsByAir': iata_codes,
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "co2 emissions air")
    if response_data is None:
        return None
    else:
        freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputAir'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return freight_emissions_df

def forward_freight_shipment_emissions_air_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2Air.xlsx')
    iata_codes_df = pd.read_excel(data_path, sheet_name='air', usecols='A:H').fillna("")
    parameters = {
        "planeType": "average",
        "weightUnit": "kilograms",
        "refrigerantFactor": 12
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'iataCodes': iata_codes_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

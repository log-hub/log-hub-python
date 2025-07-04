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

def forward_freight_shipment_emissions_sea(un_locodes: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
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
        - isRefrigirated (str): A YES/NO option that specifies whether the content being transferred through the shipments is refrigirated or not. If not specified will be taken as NO.
        - distance: Distance between sender and recipient. It will be calculated if not provided
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - shipType: enum "shipBulkCarrierAvg", "shipBulkCarrier(0-10k)", "shipBulkCarrier(10-100k)", "shipBulkCarrier(>100k)",
        "shipBulkCarrierGeneralCargo", "shipBulkCarrierGeneralCargo(0-10k)", "shipBulkCarrierGeneralCargo(10-20k)", "shipContainerShipAvg", "shipRoRoFerry" or "shipRoPaxFerry"
        - weightUnit: enum "kilograms" or "LBS" or "TEU"
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
    
    un_locodes_mandatory_columns = {'shipmentId': 'str', 'shipmentDate': 'str', 'fromUnLocode': 'str', 'toUnLocode': 'str', 'weight': 'float'}
    un_locodes_optional_columns = {'isRefrigirated': 'str'}
    un_locodes_optional_floats = ['distance']

    # Validate and convert data types
    un_locodes = validate_and_convert_data_types(un_locodes, un_locodes_mandatory_columns, 'mandatory', 'un locodes')
    if not un_locodes is None:
        un_locodes = validate_and_convert_data_types(un_locodes, un_locodes_optional_columns, 'optional', 'un locodes')
        if not un_locodes is None:
            un_locodes = convert_dates(un_locodes, ['shipmentDate'])
            un_locodes = convert_to_float(un_locodes, un_locodes_optional_floats, 'optional')
            un_locodes = convert_df_to_dict_excluding_nan(un_locodes, un_locodes_optional_floats)
    if un_locodes is None:
        return None
    
    url = create_url("co2emissionssea")
    
    headers = create_headers(api_key)

    payload = {
        'freightShipmentEmissionsBySea': un_locodes,
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "co2 emissions sea")
    if response_data is None:
        return None
    else:
        freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputSea'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return freight_emissions_df

def forward_freight_shipment_emissions_sea_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2Sea.xlsx')
    un_locodes_df = pd.read_excel(data_path, sheet_name='sea', usecols='A:H').fillna("")
    parameters = {
        "shipType": "shipContainerShipAvg",
        "weightUnit": "TEU",
        "refrigerantFactor": 12
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'unLocodes': un_locodes_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
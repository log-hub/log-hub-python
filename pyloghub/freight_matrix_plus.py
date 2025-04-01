import os
import pandas as pd
from typing import Optional
import warnings
import logging
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check,  create_button
from input_data_validation import convert_df_to_dict_excluding_nan, convert_to_float, validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_freight_matrix_plus(shipments_df: pd.DataFrame, matrix_id: str, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
    """
    Calculate the freight matrix for a list of shipments provided in a pandas DataFrame.

    Parameters:
    shipments_df (pd.DataFrame): A pandas DataFrame containing the shipment details. Each row represents a unique shipment, and the columns include:

    - shipmentId (str): A unique identifier for the shipment. 
    - shipmentDate (str): The scheduled date and time of the shipment in UTC, in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
    - fromLocationId (str): Identifier for the origin location.
    - fromCountry (str): ISO country code for the origin location.
    - fromState (str): State or region code for the origin location. 
    - fromCity (str): City name of the origin location. 
    - fromPostalCode (str): Postal code of the origin location. Increases address accuracy.
    - fromStreet (str): Street address of the origin location. Increases address accuracy.
    - fromZone (str): A logistics zone or area at the origin. Used for categorizing regions for shipping purposes, which can impact cost.
    - toLocationId (str): Identifier for the destination location. 
    - toCountry (str): ISO country code for the destination location. 
    - toState (str): State or region code for the destination location. 
    - toCity (str): City name of the destination location. 
    - toPostalCode (str): Postal code of the destination location. Increases address accuracy.
    - toStreet (str): Street address of the destination location. Increases address accuracy.
    - toZone (str): A logistics zone or area at the destination. Used to categorize regions for shipping purposes, impacting delivery strategies and costs.
    - distance (float): The total distance between the origin and destination locations in kilometers or miles. 
    - weight (float): The total weight of the shipment in kilograms or pounds. Make sure that it is aligned with the dimension that is used in the freight matrix.
    - volume (float): The total volume of the shipment in cubic meters or cubic feet. Make sure that it is aligned with the dimension that is used in the freight matrix.
    - pallets (int): The number of pallets used for the shipment. Make sure that it is aligned with the dimension that is used in the freight matrix.
    - loadingMeters (float): The total space in meters required by the shipment on the transport vehicle. Make sure that it is aligned with the dimension that is used in the freight matrix.

    matrix_id (str): The Freight Matrix ID from a matrix that was created on the Log-hub Platform.

    api_key (str): The Log-hub API key for accessing the freight matrix service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    pd.DataFrame: A pandas DataFrame containing evaluated shipments with additional
                  details such as fromLatitude, fromLongitude, toLatitude, toLongitude, costs, etc.
                  Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    float_columns = ['distance', 'weight', 'volume', 'pallets', 'loadingMeters']
    shipments_df = convert_to_float(shipments_df, float_columns, 'optional')
    mandatory_columns = {'shipmentId': 'str', 'fromLocationId': 'str', 'fromCountry': 'str', 'toLocationId': 'str', 'toCountry': 'str'}
    optional_columns = {'fromState': 'str', 'fromCity': 'str', 'fromPostalCode': 'str', 'fromStreet': 'str', 'fromZone': 'str', 'toState': 'str', 'toCity': 'str', 'toPostalCode': 'str', 'toStreet': 'str', 'toZone': 'str'}
    shipments_df = validate_and_convert_data_types(shipments_df, mandatory_columns, 'mandatory', 'shipments')
    if not shipments_df is None:
        shipments_df = validate_and_convert_data_types(shipments_df, optional_columns, 'optional', 'shipments')
    # Convert DataFrame to list of dicts for the payload, excluding NaN values in specified columns
    shipments_list = convert_df_to_dict_excluding_nan(shipments_df, float_columns)
    
    url = create_url("freightmatrixplus")
    
    headers = create_headers(api_key)
    payload = {
        "shipments": shipments_list,
        "matrix": {"matrixId": matrix_id}
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "freight matrix plus")
    if response_data is None:
        return None
    else:
        evaluated_shipments = pd.DataFrame(response_data['evaluatedShipments'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return evaluated_shipments

def forward_freight_matrix_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'freightMatrixAddresses.xlsx')
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:U', dtype={'shipmentId': str, 'shipmentDate': str, 'fromLocationId': str, 'toLocationId': str, 'fromPostalCode': str, 'toPostalCode': str, 'distance': str, 'weight': float, 'volume': float, 'pallets': float, 'loadingMeters': float})

    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'shipments': shipments_df, 'saveScenarioParameters': save_scenario}


def reverse_freight_matrix_plus(shipments_df: pd.DataFrame, matrix_id: str, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
    """
    Calculate the reverse freight matrix for a list of shipments provided in a pandas DataFrame.
    
    Parameters:
    shipments_df (pd.DataFrame): A pandas DataFrame containing the shipment details for reverse logistics. Each row represents a unique shipment, and the columns include:
        - shipmentId (str): A unique identifier for the shipment.
        - shipmentDate (str): The scheduled date and time of the shipment in UTC, in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
        - fromLocationId (str): Identifier for the origin location.
        - fromLatitude (float): Latitude of the origin location.
        - fromLongitude (float): Longitude of the origin location.
        - fromZone (str): A logistics zone or area at the origin, impacting shipping strategies and costs.
        - toLocationId (str): Identifier for the destination location.
        - toLatitude (float): Latitude of the destination location.
        - toLongitude (float): Longitude of the destination location.
        - toZone (str): A logistics zone or area at the destination, impacting delivery strategies and costs.
        - distance (float): The total distance between the origin and destination locations in kilometers or miles.
        - weight (float): The total weight of the shipment in kilograms or pounds, critical for cost calculations.
        - volume (float): The total volume of the shipment in cubic meters or cubic feet, affecting space utilization.
        - pallets (int): The number of pallets used for the shipment, influencing handling requirements.
        - loadingMeters (float): The total space required by the shipment on the transport vehicle, impacting vehicle utilization.

    matrix_id (str): The Freight Matrix ID from a matrix that was created on the Log-hub Platform.

    api_key (str): The Log-hub API key for accessing the reverse freight matrix service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    pd.DataFrame: A pandas DataFrame containing evaluated shipments with additional
                  details such as costs, weight class, distance class, and price per unit. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map" , "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    float_columns = ['distance', 'weight', 'volume', 'pallets', 'loadingMeters']
    shipments_df = convert_to_float(shipments_df, float_columns, 'optional')
    mandatory_columns = {'shipmentId': 'str', 'fromLocationId': 'str', 'fromLatitude': 'float', 'fromLongitude': 'float', 'toLocationId': 'str', 'toLatitude': 'float', 'toLongitude': 'float'}
    optional_columns = {'fromState': 'str', 'fromZone': 'str', 'toZone': 'str'}
    shipments_df = validate_and_convert_data_types(shipments_df, mandatory_columns, 'mandatory', 'shipments')
    if not shipments_df is None:
        shipments_df = validate_and_convert_data_types(shipments_df, optional_columns, 'optional', 'shipments')

    # Convert DataFrame to list of dicts for the payload, excluding NaN values in specified columns
    shipments_list = convert_df_to_dict_excluding_nan(shipments_df, float_columns)
    
    url = create_url("reversefreightmatrixplus")
    
    headers = create_headers(api_key)
    payload = {
        "shipments": shipments_list,
        "matrix": {"matrixId": matrix_id}
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "reverse freight matrix plus")
    if response_data is None:
        return None
    else:
        evaluated_shipments = pd.DataFrame(response_data['evaluatedShipments'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return evaluated_shipments

def reverse_freight_matrix_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'freightMatrixReverse.xlsx')
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:O', dtype={'shipmentId': str, 'shipmentDate': str, 'fromLocationId': str, 'toLocationId': str, 'weight': float, 'volume': float, 'pallets': float, 'loadingMeters': float})

    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'shipments': shipments_df, 'saveScenarioParameters': save_scenario}
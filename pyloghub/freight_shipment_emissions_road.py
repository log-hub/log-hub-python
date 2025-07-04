import os
import pandas as pd
import logging
from typing import Optional, Tuple
import warnings
logging.basicConfig(level=logging.INFO)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import convert_dates, validate_and_convert_data_types, convert_to_float, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_freight_shipment_emissions_road(addresses: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
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
        -distance: Distance between sender and recipient. It will be calculated if not provided.
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - vehicleType: "van(0-3.5)", "truck", "truckUrbanTruck", "truckMGV", "truckHGV", "truckRigid(3.5-7.5)", "truckRigid(7.5-12)", "truckRigid(12-20)" , "truckRigid(20-26)", "truckRigid(26-32)", "truckArticulated(3.5-34)", "truckArticulated(34-40)", "truckArticulated(40-44)", "truckArticulated(44-60)", "truckArticulated(60-72)", "truckGeneral", "truckAutoCarrier", "truckDray", "truckExpedited", "truckFlatbed", "truckHeavybulk", "truckLTL", "truckMixed", "truckMoving", "truckPackage", "truckSpecialized", "truckTanker" or "truckTL" 
        - fuelType: enum "diesel", "petrol", "CNG", "LPG", "electricity" or "other"
        - weightUnit: enum "kilograms" or "LBS"
        - emissionStandard: enum "EURO_5" or :EURO_6"

    api_key (str): The Log-hub API key for accessing the freight emissions service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Optional[Tuple[pd.DataFrame, pd.DataFrame]]: One pandas DataFrame contains the original address information along 
                  with the calculated CO2 emissions, and the second one contains shipments with no CO2 emission calculated. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])
        
    addresses_mandatory_columns = {'shipmentId': 'str', 'shipmentDate': 'str', 'fromCountry': 'str', 'toCountry': 'str', 'weight': 'float'}
    addresses_optional_columns = {'fromState': 'str', 'fromPostalCode': 'str', 'fromCity': 'str', 'fromStreet': 'str', 'toState': 'str', 'toPostalCode': 'str', 'toCity': 'str', 'toStreet': 'str', 'isRefrigirated': 'str'}
    addresses_optional_floats = ['distance']

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, addresses_mandatory_columns, 'mandatory', 'addresses')
    if not addresses is None:
        addresses = validate_and_convert_data_types(addresses, addresses_optional_columns, 'optional', 'addresses')
        if not addresses is None:
            addresses = convert_dates(addresses, ['shipmentDate'])
            addresses = convert_to_float(addresses, addresses_optional_floats, 'optional')
            addresses = convert_df_to_dict_excluding_nan(addresses, addresses_optional_floats)
    if addresses is None:
        return None
    
    url = create_url("co2emissionsroad")
    
    headers = create_headers(api_key)

    payload = {
        'freightShipmentEmissionsByRoad': addresses,
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "co2 emissions road")
    if response_data is None:
        return None
    else:
        freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputStandardRoad'])
        not_evaluated_df  = pd.DataFrame(response_data['notEvaluatedShipmentsStandardRoad'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return freight_emissions_df, not_evaluated_df

def forward_freight_shipment_emissions_road_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2RoadAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:P').fillna("")
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


def reverse_freight_shipment_emissions_road(coordinates: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
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
        - distance: Distance beteen sender and recipient. It will be calculated if not provided.
        - weight (number): The weight of the shipment.

    parameters (dict): A dictionary containing parameters:
        - vehicleType: "van(0-3.5)", "truck", "truckUrbanTruck", "truckMGV", "truckHGV", "truckRigid(3.5-7.5)", "truckRigid(7.5-12)", "truckRigid(12-20)" , "truckRigid(20-26)", "truckRigid(26-32)", "truckArticulated(3.5-34)", "truckArticulated(34-40)", "truckArticulated(40-44)", "truckArticulated(44-60)", "truckArticulated(60-72)", "truckGeneral", "truckAutoCarrier", "truckDray", "truckExpedited", "truckFlatbed", "truckHeavybulk", "truckLTL", "truckMixed", "truckMoving", "truckPackage", "truckSpecialized", "truckTanker" or "truckTL" 
        - fuelType: enum "diesel", "petrol", "CNG", "LPG", "electricity" or "other"
        - weightUnit: enum "kilograms" or "LBS"
        - emissionStandard: enum "EURO_5" or :EURO_6"

    api_key (str): The Log-hub API key for accessing the reverse freight emissions service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Optional[Tuple[pd.DataFrame, pd.DataFrame]]: One pandas DataFrame contains the original coordinates information along 
                  with the calculated CO2 emissions, and the second one contains shipments with no CO2 emission calculated. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    coordinates_mandatory_columns = {'shipmentId': 'str', 'shipmentDate': 'str', 'fromLatitude': 'float', 'fromLongitude': 'float', 'toLatitude': 'float', 'toLongitude': 'float', 'weight': 'float'}
    coordinates_optional_columns = {'isRefrigirated': 'str'}
    coordinates_optional_floats = ['distance']

    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, coordinates_mandatory_columns, 'mandatory', 'coordinates')
    if not coordinates is None:
        coordinates = validate_and_convert_data_types(coordinates, coordinates_optional_columns, 'optional', 'coordinates')
        if not coordinates is None:
            coordinates = convert_dates(coordinates, ['shipmentDate'])
            coordinates = convert_to_float(coordinates, coordinates_optional_floats, 'optional')
            coordinates = convert_df_to_dict_excluding_nan(coordinates, coordinates_optional_floats)
    if coordinates is None:
        return None
    url = create_url("reverseco2emissionsroad")
    
    headers = create_headers(api_key)

    payload = {
        'freightShipmentEmissionsByRoad': coordinates,
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "reverse co2 emissions road")
    if response_data is None:
        return None
    else:
        freight_emissions_df = pd.DataFrame(response_data['freightShipmentEmissionOutputReverseRoad'])
        not_evaluated_df  = pd.DataFrame(response_data['notEvaluatedShipmentsReverseRoad'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return freight_emissions_df, not_evaluated_df

def reverse_freight_shipment_emissions_road_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'CO2RoadReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:J').fillna("")
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
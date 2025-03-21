import os
import pandas as pd
import logging
from typing import Optional, Dict, Tuple
import warnings
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities
from distance_calculation import forward_distance_calculation_sample_data, reverse_distance_calculation_sample_data

logging.basicConfig(level=logging.INFO)

def forward_distance_calculation_with_extra_details(address_pairs: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Along the distances and durations between a pair of addresses, it as well gives additional information such as the distance covered within each country the road goes through and the distance travelled on the road type (highway, uncategorized, tollway).

    This function takes a DataFrame of address pairs (sender and recipient) and a set of parameters,
    along with an API key, and performs distance calculation with sending additional details about the road using the Log-hub distance calculation service. 

    Parameters:
    address_pairs (pd.DataFrame): A pandas DataFrame containing pairs of addresses.
        Each row should contain:
        - senderCountry (str): Sender country code. Must have at least 1 character.
        - senderState (str): Sender state code.
        - senderPostalCode (str): Sender postal code.
        - senderCity (str): Sender city name.
        - senderStreet (str): Sender street name with house number.
        - recipientCountry (str): Recipient country code. Must have at least 1 character.
        - recipientState (str): Recipient state code.
        - recipientPostalCode (str): Recipient postal code.
        - recipientCity (str): Recipient city name.
        - recipientStreet (str): Recipient street name with house number.

    parameters (Dict): A dictionary containing parameters like distanceUnit (enum: "km" or "mi"),
                        durationUnit (enum: "min" or "sec" or "h"), vehicleType (enum: "truck" or "car") and 
                        routePreference (enum: 'recommended' or 'shortest' or 'fastest').

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    api_key (str): The Log-hub API key for accessing the distance calculation service.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: The first pandas DataFrame contains the results of the distance calculations, and the second one contains additional details about the road between start and end points. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    mandatory_columns = {'senderCountry': 'str', 'recipientCountry': 'str'}
    optional_columns = {'senderState': 'str', 'senderPostalCode': 'str', 'senderCity': 'str', 'senderStreet': 'str', 'recipientState': 'str',
                        'recipientPostalCode': 'str', 'recipientCity': 'str', 'recipientStreet': 'str'}

    address_pairs = validate_and_convert_data_types(address_pairs, mandatory_columns, 'mandatory', 'addresses')
    if not address_pairs is None:
        address_pairs = validate_and_convert_data_types(address_pairs, optional_columns, 'optional', 'addresses')
    if address_pairs is None:
        return None

    url = create_url("distancecalculationwithextradetails")
    
    headers = create_headers(api_key)

    payload = {
        "addresses": address_pairs.to_dict(orient='records'), 
        "parameters": parameters,
        }
    
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "distance calculation with extra details")
    if response_data is None:
        return None
    else:
        distances_df = pd.DataFrame(response_data['distanceCalculationResult'])
        extra_details_df = pd.DataFrame(response_data['extraDetailsResult'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return distances_df, extra_details_df
    
def forward_distance_calculation_with_extra_details_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'DistanceCalcSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:J')

    parameters = {
        "distanceUnit": "km",
        "durationUnit": "min",
        "vehicleType": "car",
        "routePreference": "recommended"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'address_data': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_distance_calculation_with_extra_details(geocodes: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Along the distances and durations between a pair of coordinates, it as well gives additional information such as the distance covered within each country the road goes through and the distance travelled on the road type (highway, uncategorized, tollway).

    This function takes a DataFrame of pairs of coordinates and a set of parameters,
    along with an API key, and performs reverse distance calculation with sending additional details about the road using the Log-hub reverse distance calculation service. 

    Parameters:
    geocodes (pd.DataFrame): A pandas DataFrame containing pairs of geocodes with sender and recipient information.
        Each row should contain:
        - senderLocation (str): Sender location. Must have at least 1 character.
        - senderLatitude (float): Sender latitude.
        - senderLongitude (float): Sender longitude.
        - recipientLocation (str): Recipient location. Must have at least 1 character.
        - recipientLatitude (float): Recipient latitude.
        - recipientLongitude (float): Recipient longitude.

    parameters (Dict): A dictionary containing parameters like distanceUnit (enum: "km" or "mi"),
                        durationUnit (enum: "min" or "sec" or "h"), vehicleType (enum: "truck" or "car") and 
                        routePreference (enum: 'recommended' or 'shortest' or 'fastest').

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table will be created. If the scenario is not saved, a proper message will be shown.

    api_key (str): The Log-hub API key for accessing the reverse distance calculation service.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: The first pandas DataFrame contains the results of the distance calculations, and the second one contains additional details about the road between start and end points. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    mandatory_columns = {
            'senderLocation': 'str', 'senderLatitude': 'float', 'senderLongitude': 'float',
            'recipientLocation': 'str', 'recipientLatitude': 'float', 'recipientLongitude': 'float'
        }
    
    # Validate and convert data types
    geocodes = validate_and_convert_data_types(geocodes, mandatory_columns, 'mandatory', 'coordinates')
    if geocodes is None:
        return None

    url = create_url("reversedistancecalculationwithextradetails")
    
    headers = create_headers(api_key)
    payload = {
        "geocodes": geocodes.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "reverse distance calculation with extra details")
    if response_data is None:
        return None
    else:
        distances_df = pd.DataFrame(response_data['distanceCalculationResult'])
        extra_details_df = pd.DataFrame(response_data['extraDetailsResult'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return distances_df, extra_details_df
    
def reverse_distance_calculation_with_extra_details_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'DistanceCalcSampleDataReverse.xlsx')
    geocode_data_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:F')

    parameters = {
        "distanceUnit": "km",
        "durationUnit": "min",
        "vehicleType": "car",
        "routePreference": "recommended"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'geocode_data': geocode_data_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


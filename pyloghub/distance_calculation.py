import os
import requests
import pandas as pd
import time
import logging
from typing import Optional, Dict
import warnings
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url

logging.basicConfig(level=logging.INFO)

def forward_distance_calculation(address_pairs: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Calculate distances and durations between pairs of addresses.

    This function takes a DataFrame of address pairs (sender and recipient) and a set of parameters,
    along with an API key, and performs distance calculation using the Log-hub distance calculation service. 
    The function handles batching and rate limiting by the API.

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

    api_key (str): The Log-hub API key for accessing the distance calculation service.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the results of the distance calculations. 
                  Returns None if the process fails.
    """
    required_columns = {
            'senderCountry': 'str', 'senderState': 'str', 'senderPostalCode': 'str',
            'senderCity': 'str', 'senderStreet': 'str', 'recipientCountry': 'str',
            'recipientState': 'str', 'recipientPostalCode': 'str',
            'recipientCity': 'str', 'recipientStreet': 'str'
        }

    address_pairs = validate_and_convert_data_types(address_pairs, required_columns)
    if address_pairs is None:
        return None

    url = create_url("distancecalculation")
    
    headers = create_headers(api_key)

    payload = {
        "addresses": address_pairs.to_dict(orient='records'), 
        "parameters": parameters,
        }
    
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "distance calculation")
    if response_data is None:
        return None
    else:
        distances_df = pd.DataFrame(response_data)
        return distances_df
    
def forward_distance_calculation_sample_data():
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



def reverse_distance_calculation(geocodes: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Calculate distances and durations between pairs of locations based on coordinates.

    This function takes a DataFrame of geocode pairs (sender and recipient) with their locations and coordinates,
    a set of parameters, along with an API key, and performs reverse distance calculation using the 
    Log-hub reverse distance calculation service. The function handles batching and rate limiting by the API.

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

    api_key (str): The Log-hub API key for accessing the reverse distance calculation service.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the results of the reverse distance calculations.
                  Returns None if the process fails.
    """

    required_columns = {
            'senderLocation': 'str', 'senderLatitude': 'float', 'senderLongitude': 'float',
            'recipientLocation': 'str', 'recipientLatitude': 'float', 'recipientLongitude': 'float'
        }
    
    # Validate and convert data types
    geocodes = validate_and_convert_data_types(geocodes, required_columns)
    if geocodes is None:
        return None

    url = create_url("reversedistancecalculation")
    
    headers = create_headers(api_key)
    payload = {
        "geocodes": geocodes.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    max_retries = 3
    retry_delay = 15  # seconds

    response_data = post_method(url, payload, headers, "reverse distance calculation")
    if response_data is None:
        return None
    else:
        distances_df = pd.DataFrame(response_data)
        return distances_df

def reverse_distance_calculation_sample_data():
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
import os
import requests
import pandas as pd
import time
import logging
from typing import Optional
import warnings
logging.basicConfig(level=logging.INFO)
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types
from sending_requests import create_url, create_headers, post_method


def forward_geocoding(addresses: pd.DataFrame, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Perform forward geocoding on a list of addresses.

    This function takes a DataFrame of addresses and an API key, and performs forward
    geocoding using the Log-hub geocoding service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing the addresses to be geocoded.
        Required columns and their types:
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - searchString (str): Key location details. Information such as country, state, city, street, and zip code, although the zip code cannot be the first entry.

    api_key (str): The Log-hub API key for accessing the geocoding service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containing the original address information along 
                  with the geocoded results. Includes latitude and longitude for each address.
                  Returns None if the process fails.
    """
    geocoding_columns = {'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'searchString': 'str'}

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, geocoding_columns)
    if addresses is None:
        return None
    
    url = create_url("geocoding")
    
    headers = create_headers(api_key)

    payload = {
        'addresses': addresses.to_dict(orient='records'),
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers)
    if response_data is None:
        return None
    else:
        geocoded_data_df = response_data['geocodes']
        return geocoded_data_df



def forward_geocoding_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'GeocodingSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:F').fillna("")
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'saveScenarioParameters': save_scenario}

def reverse_geocoding(geocodes: pd.DataFrame, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Perform reverse geocoding on a list of latitude and longitude coordinates.

    This function takes a DataFrame of geocodes (latitude and longitude) and an API key, 
    and performs reverse geocoding using the Log-hub reverse geocoding service. 

    Parameters:
    geocodes (pd.DataFrame): A pandas DataFrame containing the geocodes to be reverse geocoded.
        Required columns and their types:
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.

    api_key (str): The Log-hub API key for accessing the reverse geocoding service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containing the original geocode information along 
                  with the reverse geocoded address results. Includes fields like country, 
                  state, city, and street. Returns None if the process fails.
    """
    geocodes_columns = {'latitude': 'float', 'longitude': 'float'}

    # Validate and convert data types
    geocodes = validate_and_convert_data_types(geocodes, geocodes_columns)
    if geocodes is None:
        return None
    
    url = create_url("reversegeocoding")
    headers = create_headers(api_key)
    payload = {
        "geocodes": geocodes.to_dict(orient='records')
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers)
    if response_data is None:
        return None
    else:
        addresses_df = response_data['addresses']
        return addresses_df

def reverse_geocoding_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'GeocodingSampleDataReverse.xlsx')
    geocodes_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:B')
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'geocodes': geocodes_df, 'saveScenarioParameters': save_scenario}

if __name__ == "__main__":

    api_key_dev = "e75d5db6ca8e6840e185bc1c63f20f39e65fbe0b"
    workspace_id = "7cb180c0d9e15db1a71342df559d19d473c539ad"

    sample = reverse_geocoding_sample_data()

    geocodes = sample['geocodes']
    save_scenario = sample['saveScenarioParameters']

    out = reverse_geocoding(geocodes, api_key_dev, save_scenario)

import os
import pandas as pd
import logging
from typing import Optional
import warnings
logging.basicConfig(level=logging.INFO)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_geocoding(addresses: pd.DataFrame, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
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

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the original address information along 
                  with the geocoded results. Includes latitude and longitude for each address.
                  Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    mandatory_columns = {'country': 'str'}
    optional_columns = {'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'searchString': 'str'}

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, mandatory_columns, 'mandatory', 'addresses')
    if not addresses is None:
        addresses = validate_and_convert_data_types(addresses, optional_columns, 'optional', 'addresses')

    if addresses is None:
        return None
    
    url = create_url("geocoding")
    
    headers = create_headers(api_key)

    payload = {
        'addresses': addresses.to_dict(orient='records'),
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "geocoding")
    if response_data is None:
        return None
    else:
        geocoded_data_df = pd.DataFrame(response_data['geocodes'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
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

def reverse_geocoding(geocodes: pd.DataFrame, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
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

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the original geocode information along 
                  with the reverse geocoded address results. Includes fields like country, 
                  state, city, and street. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    geocodes_columns = {'latitude': 'float', 'longitude': 'float'}

    # Validate and convert data types
    geocodes = validate_and_convert_data_types(geocodes, geocodes_columns, 'mandatory', 'geocodes')
    if geocodes is None:
        return None
    
    url = create_url("reversegeocoding")
    headers = create_headers(api_key)
    payload = {
        "geocodes": geocodes.to_dict(orient='records')
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "reverse geocoding")
    if response_data is None:
        return None
    else:
        addresses_df = pd.DataFrame(response_data['addresses'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
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
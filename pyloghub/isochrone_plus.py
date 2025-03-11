import os
import pandas as pd
import logging
from typing import Optional, Dict, Tuple
import warnings
logging.basicConfig(level=logging.INFO)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_isochrone_plus(addresses: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform forward isochrone plus calculation on a list of addresses.

    This function takes a DataFrame of addresses, a dictionary of parameters and an API key, and calculates an
    isochrone using the Log-hub forward isochrone plus service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing the addresses to be geocoded.
        Required columns and their types:
        - name (str): The name of the isochrone.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
    
    parameters (dict): A dictionary containing parameters for isochrone calculation. 
        - level (str): A number between 1 and 5, sent as a string, and representing administration level.
        - duration1 (number): A number between 1 and 1000. The maximum duration for Administration Level 1.
        - duration2 (number): A number between 1 and 600. The maximum duration for Administration Level 2.
        - duration3 (number): A number between 1 and 600. The maximum duration for Administration Level 3.
        - duration4 (number): A number between 1 and 500. The maximum duration for Administration Level 4.
        - duration5 (number): A number between 1 and 200. The maximum duration for Administration Level 5.
        - averageSpeed (number): Average speed.
        - distanceUnit (str): Distance unit "km" or "mi".
        - detourFactor (number): A decimal number between 1 and 3.
        - restrictedByCountryBoundaries (boolean): A parameter taking value True or False depending on whether the country borders should be considered during the isochrone calculation.

    api_key (str): The Log-hub API key for accessing the isochrone plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: Twio pandas DataFrames containing the original address information along 
                  with the geocoded results, and information about the reachable areas, like area name, coordinates of the area center, and population.
                  Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    mandatory_columns = {'name': 'str', 'country': 'str'}
    optional_columns = {'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'}

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, mandatory_columns, 'mandatory' 'addresses')
    if not addresses is None:
        addresses = validate_and_convert_data_types(addresses, optional_columns, 'optional', 'addresses')

    if addresses is None:
        return None
    
    url = create_url("isochroneplus")
    
    headers = create_headers(api_key)

    payload = {
        'geocodingData': addresses.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "isochrone plus")
    if response_data is None:
        return None
    else:
        geocoded_data_df = pd.DataFrame(response_data['geocodingResult'])
        reachable_areas_df = pd.DataFrame(response_data['reachableAreasTable'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return geocoded_data_df, reachable_areas_df

def forward_isochrone_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'IsochronePlusSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:G').fillna("")
    parameters = {
        'level': '3',
        'duration1': 300,
        'duration2': 300,
        'duration3': 100,
        'duration4': 100,
        'duration5': 50,
        'averageSpeed': 60,
        'distanceUnit': 'km',
        'detourFactor': 1.2, 
        'restrictedByCountryBoundaries': False
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_isochrone_plus(geocodes: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform reverse isochrone calculation on a list of latitude and longitude coordinates.

    This function takes a DataFrame of geocodes (latitude and longitude), parameters and an API key, 
    and calculates isochrones using the Log-hub reverse isochrone service. 

    Parameters:
    geocodes (pd.DataFrame): A pandas DataFrame containing the geocodes to be reverse geocoded.
        Required columns and their types:
        - name (str): The name of the isochrone.
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.

    parameters (dict): A dictionary containing parameters for isochrone calculation. 
        - level (str): A number between 1 and 5, sent as a string, and representing administration level.
        - duration1 (number): A number between 1 and 1000. The maximum duration for Administration Level 1.
        - duration2 (number): A number between 1 and 600. The maximum duration for Administration Level 2.
        - duration3 (number): A number between 1 and 600. The maximum duration for Administration Level 3.
        - duration4 (number): A number between 1 and 500. The maximum duration for Administration Level 4.
        - duration5 (number): A number between 1 and 200. The maximum duration for Administration Level 5.
        - averageSpeed (number): Average speed.
        - distanceUnit (str): Distance unit "km" or "mi".
        - detourFactor (number): A decimal number between 1 and 3.
        - restrictedByCountryBoundaries (boolean): A parameter taking value True or False depending on whether the country borders should be considered during the isochrone calculation.

    api_key (str): The Log-hub API key for accessing the reverse isochrone plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: Two pandas DataFrames containing the original geocode information along 
                  with the reverse geocoded address results, and information about the reachable areas, like area name, coordinates of the area center, and population.
                  Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    geocodes_columns = {'name': 'str', 'latitude': 'float', 'longitude': 'float'}

    # Validate and convert data types
    geocodes = validate_and_convert_data_types(geocodes, geocodes_columns, 'mandatory', 'coordinates')
    if geocodes is None:
        return None
    
    url = create_url("reverseisochroneplus")
    headers = create_headers(api_key)
    payload = {
        "geocodingData": geocodes.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "reverse isochrone plus")
    if response_data is None:
        return None
    else:
        geocoded_data_df = pd.DataFrame(response_data['geocodingResult'])
        reachable_areas_df = pd.DataFrame(response_data['reachableAreasTable'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return geocoded_data_df, reachable_areas_df

def reverse_isochrone_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'IsochronePlusSampleDataReverse.xlsx')
    geocodes_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:D')

    parameters = {
        'level': '3',
        'duration1': 300,
        'duration2': 300,
        'duration3': 100,
        'duration4': 100,
        'duration5': 50,
        'averageSpeed': 60,
        'distanceUnit': 'km',
        'detourFactor': 1.2, 
        'restrictedByCountryBoundaries': False
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': geocodes_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
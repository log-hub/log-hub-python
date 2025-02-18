import os
import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url


def forward_center_of_gravity_plus(addresses: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate center of gravity plus based on a list of addresses, their weights, volumes, and revenues.

    This function takes a DataFrame of addresses with weights, volumes, and revenues, and a set of parameters,
    along with an API key, and performs center of gravity plus calculation using the Log-hub service.

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing addresses with their weights, volumes, and revenues.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - weight (float): Weight.
        - volume (float): Volume.
        - revenue (float): Revenue.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number), distanceUnit (enum: "km" or "mi"),
                        and importance factors (importanceWeight, importanceVolume, importanceRevenue).

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned addresses with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """

    required_columns = {
            'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str',
            'city': 'str', 'street': 'str', 'weight': 'float', 'volume': 'float', 'revenue': 'float'
        }

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, required_columns)
    if addresses is None:
        return None

    url = create_url("centerofgravityplus")
    headers = create_headers(api_key)
    payload = {
        "addresses": addresses.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "center of gravity plus")
    if response_data is None:
        return None
    else:
        assigned_addresses_df = pd.DataFrame(response_data['assignedAddresses'])
        centers_df = pd.DataFrame(response_data['centers'])
        return assigned_addresses_df, centers_df

def forward_center_of_gravity_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'COGPlusSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:J', dtype={'postalCode': str})

    parameters = {
        "numberOfCenters": 3,
        "distanceUnit": "km",
        "importanceWeight": 5,
        "importanceVolume": 2,
        "importanceRevenue": 7
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_center_of_gravity_plus(coordinates: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate reverse center of gravity plus based on a list of coordinates, their weights, volumes, and revenues.

    This function takes a DataFrame of coordinates with weights, volumes, and revenues, and a set of parameters,
    along with an API key, and performs reverse center of gravity plus calculation using the Log-hub service.

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing geocodes with their weights, volumes, and revenues.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.
        - weight (float): Weight.
        - volume (float): Volume.
        - revenue (float): Revenue.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number), distanceUnit (enum: "km" or "mi"),
                        and importance factors (importanceWeight, importanceVolume, importanceRevenue).

    api_key (str): The Log-hub API key for accessing the reverse center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned geocodes with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """
    required_columns = {
            'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float',
            'weight': 'float', 'volume': 'float', 'revenue': 'float'
        }
    
    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, required_columns)
    if coordinates is None:
        return None

    url = create_url("reversecenterofgravityplus")
    
    headers = create_headers(api_key)
    payload = {
        "coordinates": coordinates.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "reverse center of gravity plus")
    if response_data is None:
        return None
    else:
        assigned_geocodes_df = pd.DataFrame(response_data['assignedGeocodes'])
        centers_df = pd.DataFrame(response_data['centers'])
        return assigned_geocodes_df, centers_df

def reverse_center_of_gravity_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'COGPlusSampleDataReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:G')

    parameters = {
        "numberOfCenters": 3,
        "distanceUnit": "km",
        "importanceWeight": 5,
        "importanceVolume": 2,
        "importanceRevenue": 7
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
import os
import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url

def forward_center_of_gravity(addresses: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate center of gravity based on a list of addresses and their weights.

    This function takes a DataFrame of addresses with weights and a set of parameters,
    along with an API key, and performs center of gravity calculation using the Log-hub service.

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing addresses with their weights.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - weight (float): Weight.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number) 
                       and distanceUnit (enum: "km" or "mi").
    
    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    api_key (str): The Log-hub API key for accessing the center of gravity service.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame 
                                       contains the assigned addresses with their respective centers, 
                                       and the second DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """
    required_columns = {
            'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str',
            'postalCode': 'str', 'city': 'str', 'street': 'str', 'weight': 'float'
        }
    
    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, required_columns)
    if addresses is None:
        return None
    
    url = create_url("centerofgravity")
    
    headers = create_headers(api_key)
    payload = {
        "addresses": addresses.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "center of gravity")
    if response_data is None:
        return None
    else:
        assigned_addresses_df = pd.DataFrame(response_data['assignedAddresses'])
        centers_df = pd.DataFrame(response_data['centers'])
        return assigned_addresses_df, centers_df
            

def forward_center_of_gravity_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'COGSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:H', dtype={'postalCode': str})

    parameters = {
        "numberOfCenters": 5,
        "distanceUnit": "km"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_center_of_gravity(coordinates: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate reverse center of gravity based on a list of geocodes and their weights.

    This function takes a DataFrame of coordinates with weights and a set of parameters,
    along with an API key, and performs reverse center of gravity calculation using the Log-hub service.

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing geocodes with their weights.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.
        - weight (float): Weight.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number) 
                       and distanceUnit (enum: "km" or "mi").

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    api_key (str): The Log-hub API key for accessing the reverse center of gravity service.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame 
                                       contains the assigned geocodes with their respective centers, 
                                       and the second DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """

    required_columns = {
            'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float', 'weight': 'float'
        }

    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, required_columns)
    if coordinates is None:
        return None

    url = create_url("reversecenterofgravity")
    headers = create_headers(api_key)
    payload = {
        "coordinates": coordinates.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario,payload)
    response_data = post_method(url, payload, headers, "reverse center of gravity")
    if response_data is None:
        return None
    else:
        assigned_geocodes_df = pd.DataFrame(response_data['assignedGeocodes'])
        centers_df = pd.DataFrame(response_data['centers'])
        return assigned_geocodes_df, centers_df
            
def reverse_center_of_gravity_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'COGSampleDataReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:E')

    parameters = {
        "numberOfCenters": 5,
        "distanceUnit": "km"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
if __name__ == "__main__":

    api_key_dev = "e75d5db6ca8e6840e185bc1c63f20f39e65fbe0b"
    workspace_id = "6df5ba5dc72a6f949340df9110bdbe5fb661d1c7"

    sample = reverse_center_of_gravity_sample_data()
    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': workspace_id,
        'scenarioName': 'CoG reverse'
    }
    out = reverse_center_of_gravity(sample['coordinates'], sample['parameters'], api_key_dev, save_scenario)

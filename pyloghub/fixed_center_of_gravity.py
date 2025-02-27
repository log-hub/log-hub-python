import os
import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url

def forward_fixed_center_of_gravity(customers: pd.DataFrame, fixed_centers: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate fixed center of gravity based on a list of customers and their weights, and predefined fixed centers.

    This function takes a DataFrame of customers with weights, a DataFrame of fixed centers (if any), and a set of parameters,
    along with an API key, and performs fixed center of gravity calculation using the Log-hub service.

    Parameters:
    customers (pd.DataFrame): A pandas DataFrame containing customers with their weights.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name. Must have at least 1 character.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - weight (float): Weight.

    fixed_centers (pd.DataFrame): A pandas DataFrame containing predefined fixed centers.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name. Must have at least 1 character.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        This DataFrame can be empty.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number) and distanceUnit (enum: "km" or "mi").

    api_key (str): The Log-hub API key for accessing the fixed center of gravity service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned geocodes with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """
    
    customer_mandatory_columns = {'name': 'str', 'country': 'str',  'weight': 'float'}
    customer_optional_columns = {'id': 'float', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str',}
    fixed_center_mandatory_columns = {'name': 'str', 'country': 'str'}
    fixed_center_optional_columns = {'id': 'float', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'}

    # Validate and convert data types for customers and fixed centers
    customers = validate_and_convert_data_types(customers, customer_mandatory_columns, 'mandatory')
    if not customers is None:
        customers = validate_and_convert_data_types(customers, customer_optional_columns, 'optional')

    fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_mandatory_columns, 'mandatory') if not fixed_centers.empty else fixed_centers
    if not fixed_centers is None:
        fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_optional_columns, 'optional') if not fixed_centers.empty else fixed_centers
    if customers is None or (not fixed_centers.empty and fixed_centers is None):
        return None
    
    url = create_url("fixedcenterofgravity")
    
    headers = create_headers(api_key)

    payload = {
        "customers": customers.to_dict(orient='records'),
        "fixedCenters": fixed_centers.to_dict(orient='records') if not fixed_centers.empty else [],
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "fixedcenterofgravity")
    if response_data is None:
        return None
    else:
        assigned_geocodes_df = pd.DataFrame(response_data['assignedGeocodes'])
        centers_df = pd.DataFrame(response_data['centers'])
        return assigned_geocodes_df, centers_df
            
def forward_fixed_center_of_gravity_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'FixedCOGSampleDataAddresses.xlsx')
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:H', dtype={'postalCode': str})
    fixedCenters_df = pd.read_excel(data_path, sheet_name='fixedCenters', usecols='A:G', dtype={'postalCode': str})

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
    return {'customers': customers_df, 'fixedCenters': fixedCenters_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_fixed_center_of_gravity(customers: pd.DataFrame, fixed_centers: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Calculate reverse fixed center of gravity based on a list of customers and their weights, and predefined fixed centers.

    This function takes a DataFrame of customers with weights, a DataFrame of fixed centers, and a set of parameters,
    along with an API key, and performs reverse fixed center of gravity calculation using the Log-hub service.

    Parameters:
    customers (pd.DataFrame): A pandas DataFrame containing customers with their weights.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - latitude (float): Latitude of the customer location.
        - longitude (float): Longitude of the customer location.
        - weight (float): Weight.

    fixed_centers (pd.DataFrame): A pandas DataFrame containing predefined fixed centers.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - latitude (float): Latitude of the fixed center location.
        - longitude (float): Longitude of the fixed center location.

    parameters (Dict): A dictionary containing parameters like numberOfCenters (number) and distanceUnit (enum: "km" or "mi").

    api_key (str): The Log-hub API key for accessing the reverse fixed center of gravity service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned geocodes with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """

    customer_mandatory_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float', 'weight': 'float'
    }
    customer_optional_columns = {'id': 'float'}

    fixed_center_mandatory_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }
    fixed_center_optional_columns = {'id': 'float'}

    # Validate and convert data types for customers and fixed centers
    customers = validate_and_convert_data_types(customers, customer_mandatory_columns, 'mandatory')
    if not customers is None:
        customers = validate_and_convert_data_types(customers, customer_optional_columns, 'optional')

    fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_mandatory_columns, 'mandatory') if not fixed_centers.empty else fixed_centers
    if not fixed_centers is None:
        fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_optional_columns, 'optional') if not fixed_centers.empty else fixed_centers
    if customers is None or (not fixed_centers.empty and fixed_centers is None):
        return None

    url = create_url("reversefixedcenterofgravity")
    
    headers = create_headers(api_key)

    payload = {
        "customers": customers.to_dict(orient='records'),
        "fixedCenters": fixed_centers.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "reverse fixed center of gravity")
    if response_data is None:
        return None
    else:
        assigned_geocodes_df = pd.DataFrame(response_data['assignedGeocodes'])
        centers_df = pd.DataFrame(response_data['centers'])
        return assigned_geocodes_df, centers_df

def reverse_fixed_center_of_gravity_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'FixedCOGSampleDataReverse.xlsx')
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:E')
    fixedCenters_df = pd.read_excel(data_path, sheet_name='fixedCenters', usecols='A:D')

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
    return {'customers': customers_df, 'fixedCenters': fixedCenters_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

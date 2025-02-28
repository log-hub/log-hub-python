import os
import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import logging
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_fixed_center_of_gravity(customers: pd.DataFrame, fixed_centers: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
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

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned geocodes with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    
    customer_columns = {
        'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str',
        'city': 'str', 'street': 'str', 'weight': 'float'
    }

    fixed_center_columns = {
        'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str',
        'city': 'str', 'street': 'str'
    }

    # Validate and convert data types for customers and fixed centers
    customers = validate_and_convert_data_types(customers, customer_columns)
    fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_columns) if not fixed_centers.empty else fixed_centers
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
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
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


def reverse_fixed_center_of_gravity(customers: pd.DataFrame, fixed_centers: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
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
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple of two pandas DataFrames. The first DataFrame contains the 
                                       assigned geocodes with their respective centers, and the second 
                                       DataFrame contains the details of the centers.
                                       Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    customer_columns = {
        'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float', 'weight': 'float'
    }

    fixed_center_columns = {
        'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }

    # Validate and convert data types for customers and fixed centers
    customers = validate_and_convert_data_types(customers, customer_columns)
    fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_columns) if not fixed_centers.empty else fixed_centers
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
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
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

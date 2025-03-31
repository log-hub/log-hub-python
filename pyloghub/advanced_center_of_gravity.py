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

def forward_advanced_center_of_gravity(customers: pd.DataFrame, sources: pd.DataFrame, fixed_centers: pd.DataFrame, product_groups: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Calculate fixed center of gravity based on a list of customers and predefined fixed centers, with an extension of setting product groups and their sources. 

    This function takes a DataFrame of customers with weights and product group, a DataFrame of fixed centers (if any), a DataFrame of sources of the products, a DataFrame of product groups, and a set of parameters, along with an API key, and performs fixed center of gravity calculation using the Log-hub service.

    Parameters:
    customers (pd.DataFrame): A pandas DataFrame containing customers with their weights and product group information.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name. Must have at least 1 character.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - productGroup (str): Product group required from the customer.
        - weight (float): Weight.
        - assignedCenter (str): Center assigned to a customer.
        - assignedSource (str): Source of the product group.

    sources (pd.DataFrame): A pandas DataFrame containing information about sources of the product groups.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name. Must have at least 1 character.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - availableProductGroups (str): Product groups available in the named source.
        This DataFrame can be empty.

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
    
    product_groups (pd.DataFrame): A pandas DataFrame with the product groups data.
        Each row should contain:
        - id (number): Identifier.
        - productGroupName (str): Name of the product group.
        - serviceLevel (number): Percenatege of the total weight that must be within the given distance.
        - serviceLevelDistance (number): The distance in which the given service level must be located.

    parameters (Dict): A dictionary containing parameters: distanceUnit (enum: "km" or "mi"), minmaximumCenters (minimum number of centers) and maxmaximumCenters (maximum number of centers) integer numbers that must be equal or smaller than the amount of customers, and inboundOutboundFactor (integer number).

    api_key (str): The Log-hub API key for accessing the advanced center of gravity service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Returns three pandas DataFrames. First one contains assigned centers and their coordinates, second one describes the inbound flows from sources to centers and the third one shows flows from centers to customers. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    
    customer_mandatory_columns = {'country': 'str',  'weight': 'float', 'productGroup': 'str'}
    customer_optional_columns = {'name': 'str', 'id': 'float', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'assignedCenter': 'str', 'assignedSource': 'str'}
    sources_optional_columns = {'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'}
    fixed_center_optional_columns = {'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'}
    product_groups_mandatory_columns = {'productGroupName': 'str', 'serviceLevel': 'float', 'serviceLevelDistance': 'float'}

    # Validate and convert data types for customers and fixed centers
    customers = validate_and_convert_data_types(customers, customer_mandatory_columns, 'mandatory', 'customers')
    if not customers is None:
        customers = validate_and_convert_data_types(customers, customer_optional_columns, 'optional', 'customers')
    sources = validate_and_convert_data_types(sources, sources_optional_columns, 'optional', 'sources')
    fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_optional_columns, 'optional', 'fixed centers') if not fixed_centers.empty else fixed_centers
    product_groups = validate_and_convert_data_types(product_groups, product_groups_mandatory_columns, 'mandatory', 'product groups')
    if any(df is None for df in [customers, sources, fixed_centers, product_groups]):
        return None
    
    url = create_url("advancedcenterofgravity")
    
    headers = create_headers(api_key)

    payload = {
        "customers": customers.to_dict(orient='records'),
        "sources": sources.to_dict(orient='records'),
        "fixedCenters": fixed_centers.to_dict(orient='records') if not fixed_centers.empty else [],
        "productGroups": product_groups.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "advanced center of gravity")
    if response_data is None:
        return None
    else:
        assigned_centers_df = pd.DataFrame(response_data['assignedCenters'])
        inbound_df = pd.DataFrame(response_data['inbound'])
        outbound_df = pd.DataFrame(response_data['outbound'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return assigned_centers_df, inbound_df, outbound_df
            
def forward_advanced_center_of_gravity_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'AdvancedCoGAddresses.xlsx')
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:K', dtype={'postalCode': str})
    sources_df = pd.read_excel(data_path, sheet_name='sources', usecols='A:H', dtype={'postalCode': str})
    fixedCenters_df = pd.read_excel(data_path, sheet_name='fixedCenters', usecols='A:G', dtype={'postalCode': str})
    product_groups_df = pd.read_excel(data_path, sheet_name='productGroups', usecols='A:D')

    parameters = {
        "distanceUnit": "km",
        'minmaximumCenters': 1,
        'maxmaximumCenters': 50,
        'inboundOutboundFactor': 8
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'customers': customers_df, 'sources': sources_df, 'fixedCenters': fixedCenters_df, 'productGroups': product_groups_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_advanced_center_of_gravity(customers: pd.DataFrame, sources: pd.DataFrame, fixed_centers: pd.DataFrame, product_groups: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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
        - productGroup (str): Product group required from the customer.
        - weight (float): Weight.
        - assignedCenter (str): Center assigned to a customer.
        - assignedSource (str): Source of the product group.

    sources (pd.DataFrame): A pandas DataFrame containing products' sources information.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - latitude (float): Latitude of the fixed center location.
        - longitude (float): Longitude of the fixed center location.
        - availableProductGroups (str): Product groups available in the named source.
        This DataFrame can be empty.

    fixed_centers (pd.DataFrame): A pandas DataFrame containing predefined fixed centers.
        Each row should contain:
        - id (number): Identifier.
        - name (str): Name.
        - latitude (float): Latitude of the fixed center location.
        - longitude (float): Longitude of the fixed center location.

    product_groups (pd.DataFrame): A pandas DataFrame with the product groups data.
        Each row should contain:
        - id (number): Identifier.
        - productGroupName (str): Name of the product group.
        - serviceLevel (number): Percenatege of the total weight that must be within the given distance.
        - serviceLevelDistance (number): The distance in which the given service level must be located.

    parameters (Dict): A dictionary containing parameters: distanceUnit (enum: "km" or "mi"), minmaximumCenters (minimum number of centers) and maxmaximumCenters (maximum number of centers) integer numbers that must be equal or smaller than the amount of customers, and inboundOutboundFactor (integer number).

    api_key (str): The Log-hub API key for accessing the reverse advanced center of gravity service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Returns three pandas DataFrames. First one contains assigned centers and their coordinates, second one describes the inbound flows from sources to centers and the third one shows flows from centers to customers. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])
    customer_mandatory_columns = {
        'latitude': 'float', 'longitude': 'float', 'weight': 'float', 'productGroup': 'str'
    }
    customer_optional_columns = {'name': 'str', 'id': 'float', 'assignedCenter': 'str', 'assignedSource': 'str'}
    sources_optional_columns = {'name': 'str', 'id': 'float', 'latitude': 'float', 'longitude': 'float', 'availableProductGroups': 'str'}
    fixed_center_optional_columns = {'name': 'str', 'id': 'float', 'latitude': 'float', 'longitude': 'float'}
    product_groups_mandatory_columns = product_groups_mandatory_columns = {'productGroupName': 'str', 'serviceLevel': 'float', 'serviceLevelDistance': 'float'}

    # Validate and convert data types for customers and fixed centers
    customers = validate_and_convert_data_types(customers, customer_mandatory_columns, 'mandatory', 'customers')
    if not customers is None:
        customers = validate_and_convert_data_types(customers, customer_optional_columns, 'optional', 'customers')
    sources = validate_and_convert_data_types(sources, sources_optional_columns, 'optional', 'sources')
    fixed_centers = validate_and_convert_data_types(fixed_centers, fixed_center_optional_columns, 'optional', 'fixed centers') if not fixed_centers.empty else fixed_centers
    product_groups = validate_and_convert_data_types(product_groups, product_groups_mandatory_columns, 'mandatory', 'product groups')
    if any(df is None for df in [customers, sources, fixed_centers, product_groups]):
        return None

    url = create_url("reverseadvancedcenterofgravity")
    
    headers = create_headers(api_key)

    payload = {
        "customers": customers.to_dict(orient='records'),
        "sources": sources.to_dict(orient='records'),
        "fixedCenters": fixed_centers.to_dict(orient='records') if not fixed_centers.empty else [],
        "productGroups": product_groups.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "reverse advanced center of gravity")
    if response_data is None:
        return None
    else:
        assigned_centers_df = pd.DataFrame(response_data['assignedCenters'])
        inbound_df = pd.DataFrame(response_data['inbound'])
        outbound_df = pd.DataFrame(response_data['outbound'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return assigned_centers_df, inbound_df, outbound_df

def reverse_advanced_center_of_gravity_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'AdvancedCoGReverse.xlsx')
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:H')
    sources_df = pd.read_excel(data_path, sheet_name='sources', usecols='A:E')
    fixedCenters_df = pd.read_excel(data_path, sheet_name='fixedCenters', usecols='A:D')
    product_groups_df = pd.read_excel(data_path, sheet_name='productGroups', usecols='A:D')

    parameters = {
        "distanceUnit": "km",
        'minmaximumCenters': 1,
        'maxmaximumCenters': 50,
        'inboundOutboundFactor': 8
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'customers': customers_df, 'sources': sources_df, 'fixedCenters': fixedCenters_df, 'productGroups': product_groups_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

if __name__ == "__main__":

    sample_data = forward_advanced_center_of_gravity_sample_data()
    customers_df = sample_data['customers']
    sources_df = sample_data['sources']
    fixed_centers_df = sample_data['fixedCenters']
    product_groups_df = sample_data['productGroups']
    parameters =sample_data['parameters']
    api_key = "14d872084c972dd5087bee9b6fa1593a5061a2e7"
    save_scenario = sample_data['saveScenarioParameters']
    save_scenario['saveScenario'] = True
    save_scenario['workspaceId'] = "dde088e344d7f19a669623c862cb144c4f9370dc"
    save_scenario['scenarioName'] = "Forward advanced cog"

    assigned_centers_df, inbound_df, outbound_df = forward_advanced_center_of_gravity(customers_df, sources_df, fixed_centers_df, product_groups_df, parameters, api_key, save_scenario, show_buttons=True)
import os
import pandas as pd
import logging
from typing import Optional, Tuple
import warnings
logging.basicConfig(level=logging.INFO)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities


def forward_nearest_warehouses(warehouses: pd.DataFrame, customers: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform forward nearest warehouses on a list of addresses.

    This function takes a DataFrame of addresses, parameters, and an API key, and performs forward
    nearest warehouses using the Log-hub service. 

    Parameters:
    warehouses (pd.DataFrame): A pandas DataFrame containing warehouses that should be considered in the calculation.
        Required columns and their types:
        - name (str): Warehouse name.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.

    customers (pd.DataFrame): A pandas DataFrame containing customers that should be considered in the calculation. 
        Required columns and their types:
        - name (str): Customer name.
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.

    parametrs (dict): A dictionary containing parameters nearestWarehouses (an integer number), distanceUnit (enum 'km' or 'mi'), maxDistance (an integer number) and streetLevel (boolean)

    api_key (str): The Log-hub API key for accessing the nearest warehouses service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Optional[Tuple[pd.DataFrame, pd.DataFrame]]: A pandas DataFrame containing information about the nearest warehouses for each 
                                                 customer, and a pandas DataFrame for unassigned customers. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    warehouses_columns = {
        'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'
    }
    customer_columns = {
        'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'
    }

    # Validate and convert data types
    warehouses = validate_and_convert_data_types(warehouses, warehouses_columns)
    customers = validate_and_convert_data_types(customers, customer_columns)

    if any(df is None for df in [warehouses, customers]):
        return None
    
    url = create_url("nearestwarehouses")
    
    headers = create_headers(api_key)

    payload = {
        'warehouses': warehouses.to_dict(orient='records'),
        'customers': customers.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "nearest warehouses")
    if response_data is None:
        return None
    else: 
        nearest_warehouses_df = pd.DataFrame(response_data['nearestWarehouses'])
        unassigned_df = pd.DataFrame(response_data['unassignedCustomers'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return nearest_warehouses_df, unassigned_df
            
def forward_nearest_warehouses_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'nearestWarehousesAddresses.xlsx')
    warehouses_df = pd.read_excel(data_path, sheet_name='warehouses', usecols='A:G').fillna("")
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:G').fillna("")
    parameters = {
        "nearestWarehouses": 3,
        "distanceUnit": "km",
        "maxDistance": 2000,
        "streetLevel": False
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'warehouses': warehouses_df, 'customers': customers_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_nearest_warehouses(warehouses: pd.DataFrame, customers: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform reverse nearest warehouses on a list of coordinates for warehouses and customers.

    This function takes a DataFrame of coordinates for warehouses and customers, parameters, and an API key, and performs reverse
    nearest warehouses using the Log-hub service. 

    Parameters:
    warehouses (pd.DataFrame): A pandas DataFrame containing warehouses that should be considered in the calculation.
        Required columns and their types:
        - name (str): Warehouse name.
        - latitude (number): Warehouse latitude.
        - longitude (number): Warehouse longitude.

    customers (pd.DataFrame): A pandas DataFrame containing customers that should be considered in the calculation. 
        Required columns and their types:
        - name (str): Customer name.
        - latitude (number): Customer latitude.
        - longitude (number): Customer longitude.

    parametrs (dict): A dictionary containing parameters nearestWarehouses (an integer number), distanceUnit (enum 'km' or 'mi'), maxDistance (an integer number) and streetLevel (boolean)

    api_key (str): The Log-hub API key for accessing the nearest warehouses service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Optional[Tuple[pd.DataFrame, pd.DataFrame]]: A pandas DataFrame containing information about the nearest warehouses for each 
                                                 customer, and a pandas DataFrame for unassigned customers. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    warehouses_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }
    customer_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }

    # Validate and convert data types
    warehouses = validate_and_convert_data_types(warehouses, warehouses_columns)
    customers = validate_and_convert_data_types(customers, customer_columns)

    if any(df is None for df in [warehouses, customers]):
        return None
    
    url = create_url("reversenearestwarehouses")
    
    headers = create_headers(api_key)

    payload = {
        'warehouses': warehouses.to_dict(orient='records'),
        'customers': customers.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url,payload, headers, "reverse nearest warehouses")
    if response_data is None:
        return None
    else:
        nearest_warehouses_df = pd.DataFrame(response_data['nearestWarehouses'])
        unassigned_df = pd.DataFrame(response_data['unassignedCustomers'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return nearest_warehouses_df, unassigned_df

def reverse_nearest_warehouses_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'nearestWarehousesReverse.xlsx')
    warehouses_df = pd.read_excel(data_path, sheet_name='warehouses', usecols='A:D').fillna("")
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:D').fillna("")
    parameters = {
        "nearestWarehouses": 3,
        "distanceUnit": "km",
        "maxDistance": 2000,
        "streetLevel": False
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'warehouses': warehouses_df, 'customers': customers_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


import os
import pandas as pd
import warnings
from typing import Optional
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types, convert_to_float, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url

def forward_supply_chain_map_sea_routes(addresses: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a map of sea routes based on the given route UN/LOCODES.

    This function takes a DataFrame of routes UN/LOCODES with their quantity and route restrictions, along with an API key, 
    and creates a map of sea routes using the Log-hub Supply Chain Map service. 

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing sea route UN/LOCODES with their quantity and route restrictions.
        Each row should contain:
        - id (number): Identifier.
        - fromName (str): Name for the start location of the sea route.
        - fronUnLocode (str): UN/LOCODE for the start location of the sea route.
        - toName (str): Name for the end location of the sea route.
        - toUnLocode (str): UN/LOCODE for the end location of the sea route.
        - quantity (number): Numerical value of goods being transferred through a specific sea route.
        - routingOptions (str): Restricting moving through channels, straits and passages based on the passed restrictions. 
                                Currently supported are Suez channel (as suez), Panama channel (as panama), Malacca strait (as malacca),
                                Gibraltar strait (as gibraltar), Dover strait (as dover), Bering strait (as bering), 
                                Magellan strait (as magellan), Bab-el-Mandeb strait (as babelmandeb), Kiel channel (as kiel), 
                                Corinth channel (as corinth), Northwest passage (as northwest) and Northeast passage (as northeast).
                                If multiple restrictions are named, comma or semicolon can be used as separators.

    parameters (dict): A dictionary containing parameter 'distanceUnit' (enum 'km' or 'mi' or 'nm'). 

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 
                        'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the sea route UN/LOCODES with their quantity and route restriction options, 
                  along with the parsed latitude and longitude, parsed country name and distance.

    """
    mandatory_columns = {'fromName': 'str', 'fromUnLocode': 'str', 'toName': 'str', 'toUnLocode': 'str'}
    optional_columns = {'routingOptions': 'str'}
    optional_floats = ['id', 'quantity']
    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses, mandatory_columns, 'mandatory')
    if not addresses is None:
         addresses = validate_and_convert_data_types(addresses, optional_columns, 'optional')
         if not addresses is None:
              addresses = convert_to_float(addresses, optional_floats, 'optional')
              addresses = convert_df_to_dict_excluding_nan(addresses, optional_floats)
    if addresses is None:
        return None

    url = create_url("supplychainmapsearoutes")
    
    headers = create_headers(api_key)
    payload = {
        "seaRoutesAddressesData": addresses,
        "parameters": parameters
    }
    
    payload = save_scenario_check(save_scenario, payload, "supplychainmapsearoutes")
    response_data = post_method(url, payload, headers, "supply chain map sea routes")
    if response_data is None:
        return response_data
    else:
        route_result_df = pd.DataFrame(response_data['seaRoutes'])
        return route_result_df
            

def forward_supply_chain_map_sea_routes_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapSeaRoutesAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:G')

    parameters = {
        'distanceUnit': 'nm'
    }
    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_supply_chain_map_sea_routes(coordinates: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a map of sea routes based on the given route latitude and longitude.

    This function takes a DataFrame of routes coordinates pairs with their quantity and route restrictions, along with an API key, 
    and creates a map of sea routes using the Log-hub Supply Chain Map service. 

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing sea route coordinates pairs with their quantity and route restrictions.
        Each row should contain:
        - id (number): Identifier.
        - fromName (str): Name for the start location of the sea route.
        - fromLatitude (number): Latitude of the start location.
        - fromLongitude (number): Longitude of the start location.
        - toName (str): Name for the end location of the sea route.
        - toLatitude (str): Latitude of the end location.
        - toLongitude (number): Longitude of the end location.
        - quantity (number): Numerical value of goods being transferred through a specific sea route.
        - routingOptions (str): Restricting moving through channels, straits and passages based on the passed restrictions. 
                                Currently supported are Suez channel (as suez), Panama channel (as panama), Malacca strait (as malacca),
                                Gibraltar strait (as gibraltar), Dover strait (as dover), Bering strait (as bering), 
                                Magellan strait (as magellan), Bab-el-Mandeb strait (as babelmandeb), Kiel channel (as kiel), 
                                Corinth channel (as corinth), Northwest passage (as northwest) and Northeast passage (as northeast).
                                If multiple restrictions are named, comma or semicolon can be used as separators.

    parameters (dict): A dictionary containing parameter 'distanceUnit' (enum 'km' or 'mi' or 'nm'). 

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 
                        'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the sea route coordinates pairs with their quantity and route restriction options, 
                  along with the parsed country name, parsed UN/LOCODES and distance.

    """

    mandatory_columns = {'fromName': 'str', 'fromLatitude':'float', 'fromLongitude': 'float', 'toName': 'str', 'toLatitude': 'float', 'toLongitude': 'float'}
    optional_columns = {'routingOptions': 'str'}
    optional_floats = ['id', 'quantity']
    # Validate and convert data types
    coordinates = validate_and_convert_data_types(coordinates, mandatory_columns, 'mandatory')
    if not coordinates is None:
         coordinates = validate_and_convert_data_types(coordinates, optional_columns, 'optional')
         if not coordinates is None:
              coordinates = convert_to_float(coordinates, optional_floats, 'optional')
              coordinates = convert_df_to_dict_excluding_nan(coordinates, optional_floats)
    if coordinates is None:
        return None

    url = create_url("reversesupplychainmapsearoutes")
    
    headers = create_headers(api_key)
    payload = {
        "seaRoutesCoordinatesData": coordinates,
        "parameters": parameters
    }
    
    payload = save_scenario_check(save_scenario, payload, "reversesupplychainmapsearoutes")
    response_data = post_method(url, payload, headers, "reverse supply chain map sea routes")
    if response_data is None:
                return None
    else:
        route_result_df = pd.DataFrame(response_data['seaRoutes'])
        return route_result_df
            

def reverse_supply_chain_map_sea_routes_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapSeaRoutesReverse.xlsx')
    coordinates_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:I')

    parameters = {
        'distanceUnit': 'nm'
    }
    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'coordinates': coordinates_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
import os
import requests
import pandas as pd
import time
import logging
from typing import Optional, Tuple
import warnings
logging.basicConfig(level=logging.INFO)
from save_to_platform import save_scenario_check

def convert_df_to_dict_excluding_nan(df, columns_to_check):
    """
    Convert a DataFrame to a list of dictionaries, excluding specified keys if their values are NaN.

    Parameters:
    df (pd.DataFrame): The DataFrame to convert.
    columns_to_check (list): List of column names to check for NaN values.

    Returns:
    list: A list of dictionaries representing the rows of the DataFrame, excluding keys for NaN values in specified columns.
    """
    records = []
    for ind, row in df.iterrows():
        record = {}
        for column, value in row.items():
            if column not in columns_to_check:
                logging.error(f"Missing required column: {column}")
                return None
            elif columns_to_check[column] == 'float':
                df.loc[ind, column] = pd.to_numeric(df[column][ind], errors='coerce')
                if pd.notna(df[column][ind]):
                    record[column] = float(df[column][ind])
            elif columns_to_check[column] == 'str':
                df.loc[ind, column] = str(df[column][ind])
                record[column] = df[column].loc[ind]
        records.append(record)
    return records


def forward_location_planning(customers: pd.DataFrame, warehouses: pd.DataFrame, costs_adjustments: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> dict:
    """
    Perform location planning based on customers, warehouses, and costs adjustment.

    This function takes DataFrames of customers, warehouses, costs adjustment, and an API key, and performs forward network design plus using the Log-hub service. 

    Parameters:
    customers (pd.DataFrame): Customer data with its address and its shipment structure for the optimization run.
        - name (str): Customer name.
        - country (str): Country code or country name.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - weight (number): Average weight of a shipment that goes to this customer.
        - volume (number): Average volume of a shipment that goes to this customer.
        - numberOfShipments (number): Total number of shipments (integer value) the customer receives.
    warehouses (pd.DataFrame): A pandas DataFrame containing the warehouses information for the optimization run.
        - name (str): Warehouse name.
        - country (str): Country code or country name.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - fixed (0 or 1): If the warehouse should be in every case part of the result, then mark it as fixed (1).
        - minWeight (number): The weight that should be at least assigned to this warehouse.
        - maxWeight (number): The maximum weight capacity of the warehouse.
        - penaltyCostsWeight (number): Penalty costs per weight unit. 
        - minVolume (number): The volume that should be at least assigned to this warehouse.
        - maxVolume (number): The maximum volume capacity of the warehouse.
        - penaltyCostsVolume (number): Penalty costs per volume unit. 
        - fixedCosts (number):  Fixed warehouse costs.
        - costsPerWeightUnit (number): Costs by weight unit.
        - costsPerVolumeUnit (number): Costs by volume unit.
    costs_adjustments (pd.DataFrame): A pandas DataFrame containing information that allows users to customize the transportation costs between warehouses and customers by defining adjustment factors and flat on top fees.
        - customerCountryIso2 (str): A two-letter ISO2 code representing the country of the customer.
        - warehouseCountryIso2 (str): A two-letter ISO2 code representing the country of the warehouse.
        - customerName (str): Customer name.
        - warehouseName (str): Warehouse name.
        - adjustmentFactor (number): A numerical value which will be multiplied by the transport costs.
        - flatOnTop (number): A flat fee that will be added to the transport costs.

    parametrs (dict): A dictionary containing parameters distanceUnit (enum 'km' or 'mi'), weightUnit (enum 'kg' or 't' or 'LBS'), volumeUnit (enum 'cbm' or 'l'), vehicleType (enum 'car' or 'truck'), streetLevel (boolean), minWarehouses (integer number), maxWarehouses (integer number). 

    api_key (str): The Log-hub API key for accessing the location planning service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    dict: A dictionary containing url and apiServer that should be passed to a GET method in order to get output tables, along with the explanation.
    """
    customers_columns = {
        'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'weight': 'float', 'volume': 'float', 'numberOfShipments': 'float'
    }
    warehouses_columns = {
        'id': 'float', 'name': 'str', 'country': 'str', 'state' : 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'fixed': 'float', 'minWeight': 'float', 'maxWeight': 'float', 'penaltyCostsWeight': 'float', 'minVolume': 'float', 'maxVolume': 'float', 'penaltyCostsVolume': 'float','fixedCosts': 'float','costsPerWeightUnit': 'float', 'costsPerVolumeUnit': 'float'
    }
    costs_adjustments_columns = {
        'id': 'float', 'customerCountryIso2': 'str',  'warehouseCountryIso2': 'str', 'customerName': 'str', 'warehouseName': 'str', 'adjustmentFactor': 'float', 'flatOnTop': 'float'
        }

    # Validate and convert data types
    warehouses = convert_df_to_dict_excluding_nan(warehouses, warehouses_columns)
    customers = convert_df_to_dict_excluding_nan(customers, customers_columns)
    costs_adjustments = convert_df_to_dict_excluding_nan(costs_adjustments, costs_adjustments_columns)

    if any(df is None for df in [warehouses, customers, costs_adjustments]):
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/locationplanninglongrun"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'customers': customers,
        'warehouses': warehouses,
        'costsAdjustmentTransportationCostsStandard': costs_adjustments,
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                result = response_data['result']
                return result
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in location planning API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_location_planning_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'LocationPlanningAddresses.xlsx')
    warehouses_df = pd.read_excel(data_path, sheet_name='warehouses', usecols='A:Q').fillna("")
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:J').fillna("")
    costs_adjustments_df = pd.read_excel(data_path, sheet_name='costsAdjustment', usecols='A:G').fillna("")
    parameters = {
        "distanceUnit": "km",
        "vehicleType": "car",
        "streetLevel": False,
        "weightUnit": "kg",
        "volumeUnit": "cbm",
        "minWarehouses": 1,
        "maxWarehouses": 2

    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'warehouses': warehouses_df, 'customers': customers_df, 'costsAdjustments': costs_adjustments_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_location_planning(customers: pd.DataFrame, warehouses: pd.DataFrame, costs_adjustments: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> dict:
    """
    Perform reverse location planning based on customers, warehouses, and costs adjustment.

    This function takes DataFrames of customers, warehouses, costs adjustment, and an API key, and performs reverse network design plus using the Log-hub service. 

    Parameters:
    customers (pd.DataFrame): Customer data with its address and its shipment structure for the optimization run.
        - name (str): Customer name.
        - latitude (number): Customer latitude.
        - longitude (number): Customer longitude.
        - weight (number): Average weight of a shipment that goes to this customer.
        - volume (number): Average volume of a shipment that goes to this customer.
        - numberOfShipments (number): Total number of shipments (integer value) the customer receives.
    warehouses (pd.DataFrame): A pandas DataFrame containing the warehouses information for the optimization run.
        - name (str): Warehouse name.
        - latitude (number): Warehouse latitude.
        - longitude (number): Warehouse longitude.
        - fixed (0 or 1): If the warehouse should be in every case part of the result, then mark it as fixed (1).
        - minWeight (number): The weight that should be at least assigned to this warehouse.
        - maxWeight (number): The maximum weight capacity of the warehouse.
        - penaltyCostsWeight (number): Penalty costs per weight unit. 
        - minVolume (number): The volume that should be at least assigned to this warehouse.
        - maxVolume (number): The maximum volume capacity of the warehouse.
        - penaltyCostsVolume (number): Penalty costs per volume unit. 
        - fixedCosts (number):  Fixed warehouse costs.
        - costsPerWeightUnit (number): Costs by weight unit.
        - costsPerVolumeUnit (number): Costs by volume unit.
    costs_adjustments (pd.DataFrame): A pandas DataFrame containing information that allows users to customize the transportation costs between warehouses and customers by defining adjustment factors and flat on top fees.
        - customerCountryIso2 (str): A two-letter ISO2 code representing the country of the customer.
        - warehouseCountryIso2 (str): A two-letter ISO2 code representing the country of the warehouse.
        - customerName (str): Customer name.
        - warehouseName (str): Warehouse name.
        - adjustmentFactor (number): A numerical value which will be multiplied by the transport costs.
        - flatOnTop (number): A flat fee that will be added to the transport costs.

    parametrs (dict): A dictionary containing parameters distanceUnit (enum 'km' or 'mi'), weightUnit (enum 'kg' or 't' or 'LBS'), volumeUnit (enum 'cbm' or 'l'), vehicleType (enum 'car' or 'truck'), streetLevel (boolean), minWarehouses (integer number), maxWarehouses (integer number). 

    api_key (str): The Log-hub API key for accessing the location planning service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    dict: A dictionary containing url and apiServer that should be passed to a GET method in order to get output tables, along with the explanation.
    """
    customers_columns = {
        'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float', 'weight': 'float', 'volume': 'float', 'numberOfShipments': 'float'
    }
    warehouses_columns = {
        'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float', 'fixed': 'float', 'minWeight': 'float', 'maxWeight': 'float', 'penaltyCostsWeight': 'float', 'minVolume': 'float', 'maxVolume': 'float', 'penaltyCostsVolume': 'float','fixedCosts': 'float','costsPerWeightUnit': 'float', 'costsPerVolumeUnit': 'float'
    }
    costs_adjustments_columns = {
        'id': 'float', 'customerCountryIso2': 'str',  'warehouseCountryIso2': 'str', 'customerName': 'str', 'warehouseName': 'str', 'adjustmentFactor': 'float', 'flatOnTop': 'float'
        }

    # Validate and convert data types
    warehouses = convert_df_to_dict_excluding_nan(warehouses, warehouses_columns)
    customers = convert_df_to_dict_excluding_nan(customers, customers_columns)
    costs_adjustments = convert_df_to_dict_excluding_nan(costs_adjustments, costs_adjustments_columns)

    if any(df is None for df in [warehouses, customers, costs_adjustments]):
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reverselocationplanninglongrun"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'customers': customers,
        'warehouses': warehouses,
        'costsAdjustmentTransportationCostsStandard': costs_adjustments,
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                result = response_data['result']
                return result
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in reverse location planning API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def reverse_location_planning_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'LocationPlanningReverse.xlsx')
    warehouses_df = pd.read_excel(data_path, sheet_name='warehouses', usecols='A:N').fillna("")
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:G').fillna("")
    costs_adjustments_df = pd.read_excel(data_path, sheet_name='costsAdjustment', usecols='A:G').fillna("")
    parameters = {
        "distanceUnit": "km",
        "vehicleType": "car",
        "streetLevel": False,
        "weightUnit": "kg",
        "volumeUnit": "cbm",
        "minWarehouses": 1,
        "maxWarehouses": 2

    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'warehouses': warehouses_df, 'customers': customers_df, 'costsAdjustments': costs_adjustments_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

if __name__ == "__main__":
    api_key_dev = "e75d5db6ca8e6840e185bc1c63f20f39e65fbe0b"
    workspace_id = "7cb180c0d9e15db1a71342df559d19d473c539ad"

    sample = reverse_location_planning_sample_data()

    customer = sample['customers']
    warehouses = sample['warehouses']
    costs_adjustments = sample['costsAdjustments']
    par = sample['parameters']
    save_scenario = sample['saveScenarioParameters']
    save_scenario['saveScenario'] = True
    save_scenario['workspaceId'] = workspace_id
    save_scenario['scenarioName'] = 'Location planning'

    out = reverse_location_planning(customer, warehouses, costs_adjustments, par, api_key_dev, save_scenario)
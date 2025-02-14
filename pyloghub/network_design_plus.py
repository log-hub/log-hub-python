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


def forward_network_design_plus(factories: pd.DataFrame, warehouses: pd.DataFrame, customers: pd.DataFrame, product_segments: pd.DataFrame, transport_costs: pd.DataFrame, transport_costs_rules: pd.DataFrame, stepwise_function_weight: pd.DataFrame, stepwise_function_volume: pd.DataFrame, distance_limits: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> dict:
    """
    Perform network design plus based on factories, warehouses, customers, product segments, transport costs, transport costs rules, stepwise functions for weight and volume, and distance limits.

    This function takes DataFrames of factories, warehouses, customers, product segments, transport costs, transport costs rules, stepwise functions for weight and volume, distance limits and an API key, and performs forward network design plus using the Log-hub service. 

    Parameters:
    factories (pd.DataFrame): A pandas DataFrame containing the factories information for the optimization run.
        Required columns and their types:
        - name (str): Factory name.
        - country (str): Country code or country name.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - outboundFtlCapacityWeight (number): Maximum truck capacity regarding the weight dimension for outbound transports.
        - outboundFtlCapacityVolume (number): Maximum truck capacity regarding the volume dimension for outbound transports.
        - minimumFtlCosts (number): Minimum costs of a full truck.
        - outboundFtlCost1DistanceUnit (number): Costs per km/mi for the first distance unit.
        - outboundFtlCost1000DistanceUnit (number): Costs per km/mi for the 1000. distance unit.
        - minimumLtlCosts (number): Minimum costs of an LTL truck.
        - outboundCostsHalfFtlPercent (number): Costs for 1/2 truck.
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
        - outboundFtlCapacityWeight (number): Maximum truck capacity regarding the weight dimension for outbound transports.
        - outboundFtlCapacityVolume (number): Maximum truck capacity regarding the volume dimension for outbound transports.
        - minimumFtlCosts (number): Minimum costs of a full truck.
        - outboundFtlCost1DistanceUnit (number): Costs per km/mi for the first distance unit.
        - outboundFtlCost1000DistanceUnit (number): Costs per km/mi for the 1000. distance unit.
        - minimumLtlCosts (number): Minimum costs of an LTL truck.
        - outboundCostsHalfFtlPercent (number): Costs for 1/2 truck.
        - minimumInboundReplenishmentFrequency (number): Minimum number of shipments that should go between a factory and a warehouse.
        - minimumOutboundReplenishmentFrequency (number): Minimum number of shipments that should go between a warehouse and a customer.
        - weightCostFunction (str): ID of the relevant weight cost function.
        - volumeCostFunction (str): ID of the relevant volume cost function.
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
        - productSegments (str): Influences which warehouses could be used to fulfill the customer demand.
        - factory (str): The factory that delivers to the customer.
        - warehouse (str): The warehouse that delivers to the customer.
        - maximumWarehouseDistance (number): Maximum allowed distance from the assigned warehouse.
        - penaltyCostsWarehouseDistance (number): Penalty costs per distance unit.
    product_segments (pd.DataFrame): Data for the existing product segments, and the available warehouses for each of segment. 
        - segmentName (str): Name of a specific product segment.
        - availableWarehouses (str): List of warehouses which could be used for a specific segment separated with a semicolon.
    transport_costs (pd.DataFrame): Defining detailed transport costs for all factory-warehouse and warehouse-customer relations.
        - startLocationName (str): Start name of the relation.
        - endLocationName (str): End name of the relation.
        - weightCapacity (number): Capacity for the weight dimension for the transport unit.
        - volumeCapacity (number): Capacity for the volume dimension for the transport unit.
        - costsPerUnit (number): Costs per transport unit.
    transport_costs_rules (pd.DataFrame): Defining general rules and the corresponding vehicle capacities transport costs.
        - fromCountryIso2 (str): ISO 2 code of the sender country.
        - fromZip (str): Postal code of the sender.
        - fromName (str): Start name of the relation. 
        - toCountryIso2 (str): ISO 2 code of the recipient country.
        - toZip (str): Postal code of the recipient.
        - toName (str): End name of the relation. 
        - layer (str): The direction of the flow, can only be "inbound" (from factory to warehouse) or "outbound" 
                       (from warehouse to customer).
        - distance (number): Distance between sender and recipient.
        - weightCapacityPerUnit (number): Capacity for the weight dimension for the transport unit.
        - volumeCapacityPerUnit (number): Capacity for the volume dimension for the transport unit.
        - costsPerUnit (number): Costs per transport unit.
    stepwise_function_weight (pd.DataFrame): Data for a stepwise (piecewise) cost function for the weight dimension.   
        - stepFunctionId (str): ID of the respective cost function.
        - stepEnd (number): An upper limit for a specific step.
        - fixedCost (number): Fixed cost for a specific step.
        - costPerWeightUnit (number): Cost per weight unit for a specific step.
    stepwise_function_volume (pd.DataFrame): Data for a stepwise (piecewise) cost function for the volume dimension.   
        - stepFunctionId (str): ID of the respective cost function.
        - stepEnd (number): An upper limit for a specific step.
        - fixedCost (number): Fixed cost for a specific step.
        - costPerVolumeUnit (number): Cost per volume unit for a specific step.
    distance_limits (pd.DataFrame): Data specifying the maximum distance within which a given percentage of total demand must be met.
        - distanceLimit (number):  Maximum possible distance between the warehouse and delivery points.
        - weightPercentage (number): Minimum percentage of total weight that needs to be covered within the specified distance.
        - volumePercentage (number): Minimum percentage of total volume that needs to be covered within the specified distance.
        - distanceLimitPenalty (number): Penalty cost, if the constraint would not be fulfilled.

    parametrs (dict): A dictionary containing parameters distanceUnit (enum 'km' or 'mi'), vehicleType (enum 'car' or 
                      'truck'), streetLevel (boolean), inboundConsolidation (boolean), outboundConsolidation (boolean), 
                      allowMultisourcing (boolean), minWarehouses (integer number), maxWarehouses (integer number).

    api_key (str): The Log-hub API key for accessing the network design service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    dict: A dictionary containing url and apiServer that should be passed to a GET method in order to get output tables, along with the explanation.
    """
    factories_columns = {
        'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 
        'street': 'str', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'minimumFtlCosts': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'minimumLtlCosts': 'float', 'outboundCostsHalfFtlPercent': 'float'
    }
    warehouses_columns = {
        'id': 'float', 'name': 'str', 'country': 'str', 'state' : 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'fixed': 'float', 'minWeight': 'float', 'maxWeight': 'float', 'penaltyCostsWeight': 'float', 'minVolume': 'float', 'maxVolume': 'float', 'penaltyCostsVolume': 'float','fixedCosts': 'float','costsPerWeightUnit': 'float', 'costsPerVolumeUnit': 'float', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'minimumFtlCosts': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'minimumLtlCosts': 'float', 'outboundCostsHalfFtlPercent': 'float', 'minimumInboundReplenishmentFrequency': 'float', 'minimumOutboundReplenishmentFrequency': 'float', 'weightCostFunction': 'str', 'volumeCostFunction': 'str'
    }
    customers_columns = {
        'id': 'float', 'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'weight': 'float', 'volume': 'float', 'numberOfShipments': 'float', 'productSegments': 'str', 'factory': 'str', 'warehouse': 'str', 'maximumWarehouseDistance': 'float', 'penaltyCostsWarehouseDistance': 'float',
    }
    product_segments_columns = {
        'id': 'float', 'segmentName': 'str', 'availableWarehouses': 'str'
    }
    transport_costs_columns = {
        'id': 'float', 'startLocationName': 'str', 'endLocationName': 'str', 'weightCapacity': 'float', 'volumeCapacity': 'float', 'costsPerUnit': 'float',
    }
    transport_costs_rules_columns = {
        'id': 'float', 'fromCountryIso2': 'str', 'fromZip': 'str',  'fromName': 'str', 'toCountryIso2': 'str', 'toZip': 'str', 'toName': 'str', 'layer': 'str', 'distance': 'float', 'weightCapacityPerUnit': 'float', 'volumeCapacityPerUnit': 'float', 'costsPerUnit': 'float'
    }
    stepwise_function_weight_columns = {
        'id': 'float', 'stepFunctionId': 'str', 'stepEnd': 'float', 'fixedCost': 'float', 'costPerWeightUnit': 'float',
        }
    stepwise_function_volume_columns = {
        'id': 'float', 'stepFunctionId': 'str', 'stepEnd': 'float', 'fixedCost': 'float', 'costPerVolumeUnit': 'float',
        }
    distance_limits_columns = {
        'id': 'float', 'distanceLimit': 'str',  'weightPercentage': 'str', 'volumePercentage': 'str', 'distanceLimitPenalty': 'str', 
        }

    # Validate and convert data types
    factories = convert_df_to_dict_excluding_nan(factories, factories_columns)
    warehouses = convert_df_to_dict_excluding_nan(warehouses, warehouses_columns)
    customers = convert_df_to_dict_excluding_nan(customers, customers_columns)
    product_segments = convert_df_to_dict_excluding_nan(product_segments, product_segments_columns)
    transport_costs = convert_df_to_dict_excluding_nan(transport_costs, transport_costs_columns)
    transport_costs_rules = convert_df_to_dict_excluding_nan(transport_costs_rules, transport_costs_rules_columns)
    stepwise_function_weight = convert_df_to_dict_excluding_nan(stepwise_function_weight, stepwise_function_weight_columns)
    stepwise_function_volume = convert_df_to_dict_excluding_nan(stepwise_function_volume, stepwise_function_volume_columns)
    distance_limits = convert_df_to_dict_excluding_nan(distance_limits, distance_limits_columns)

    if any(df is None for df in [factories, warehouses, customers, product_segments, transport_costs, transport_costs_rules, stepwise_function_weight, stepwise_function_volume, distance_limits]):
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/networkdesignpluslongrun"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'factories': factories,
        'warehouses': warehouses,
        'customers': customers,
        'productSegments': product_segments,
        'transportCosts': transport_costs,
        'transportsCostsRules': transport_costs_rules,
        'stepwiseCostFunctionWeight': stepwise_function_weight,
        'stepwiseCostFunctionVolume': stepwise_function_volume,
        'distanceLimits': distance_limits,
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
                logging.error(f"Error in network design plus API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_network_design_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'NetworkDesignPlusAddresses.xlsx')
    factories_df = pd.read_excel(data_path, sheet_name='factories', usecols='A:N').fillna("")
    warehouses_df = pd.read_excel(data_path, sheet_name='warehouses', usecols='A:AB').fillna("")
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:O').fillna("")
    product_segments_df = pd.read_excel(data_path, sheet_name='productSegments', usecols='A:C').fillna("")
    transport_costs_df = pd.read_excel(data_path, sheet_name='transportCosts', usecols='A:F').fillna("")
    transport_costs_rules_df = pd.read_excel(data_path, sheet_name='transportCostsRules', usecols='A:L').fillna("")
    stepwise_function_weight_df = pd.read_excel(data_path, sheet_name='stepwiseCostFunctionWeight', usecols='A:E').fillna("")
    stepwise_function_volume_df = pd.read_excel(data_path, sheet_name='stepwiseCostFunctionVolume', usecols='A:E').fillna("")
    distance_limits_df = pd.read_excel(data_path, sheet_name='distanceLimits', usecols='A:E').fillna("")
    parameters = {
        "distanceUnit": "km",
        "vehicleType": "car",
        "streetLevel": False,
        "inboundConsolidation": True,
        "outboundConsolidation": False,
        "allowMultisourcing": True,
        "minWarehouses": 1,
        "maxWarehouses": 2

    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'factories': factories_df, 'warehouses': warehouses_df, 'customers': customers_df, 'productSegments': product_segments_df, 'transportCosts': transport_costs_df, 'transportCostsRules': transport_costs_rules_df, 'stepwiseCostFunctionWeight': stepwise_function_weight_df, 'stepwiseCostFunctionVolume': stepwise_function_volume_df, 'distanceLimits': distance_limits_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_network_design_plus(factories: pd.DataFrame, warehouses: pd.DataFrame, customers: pd.DataFrame, product_segments: pd.DataFrame, transport_costs: pd.DataFrame, transport_costs_rules: pd.DataFrame, stepwise_function_weight: pd.DataFrame, stepwise_function_volume: pd.DataFrame, distance_limits: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> dict:
    """
    Perform reverse network design plus based on factories, warehouses, customers, product segments, transport costs, transport costs rules, stepwise functions for weight and volume, and distance limits.

    This function takes DataFrames of factories, warehouses, customers, product segments, transport costs, transport costs rules, stepwise functions for weight and volume, distance limits and an API key, and performs reverse network design plus using the Log-hub service. 

    Parameters:
    factories (pd.DataFrame): A pandas DataFrame containing the factories information for the optimization run.
        Required columns and their types:
        - name (str): Factory name.
        - latitude (number): Factory latitude.
        - longitude (number): Factory longitude.
        - outboundFtlCapacityWeight (number): Maximum truck capacity regarding the weight dimension for outbound transports.
        - outboundFtlCapacityVolume (number): Maximum truck capacity regarding the volume dimension for outbound transports.
        - minimumFtlCosts (number): Minimum costs of a full truck.
        - outboundFtlCost1DistanceUnit (number): Costs per km/mi for the first distance unit.
        - outboundFtlCost1000DistanceUnit (number): Costs per km/mi for the 1000. distance unit.
        - minimumLtlCosts (number): Minimum costs of an LTL truck.
        - outboundCostsHalfFtlPercent (number): Costs for 1/2 truck.
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
        - outboundFtlCapacityWeight (number): Maximum truck capacity regarding the weight dimension for outbound transports.
        - outboundFtlCapacityVolume (number): Maximum truck capacity regarding the volume dimension for outbound transports.
        - minimumFtlCosts (number): Minimum costs of a full truck.
        - outboundFtlCost1DistanceUnit (number): Costs per km/mi for the first distance unit.
        - outboundFtlCost1000DistanceUnit (number): Costs per km/mi for the 1000. distance unit.
        - minimumLtlCosts (number): Minimum costs of an LTL truck.
        - outboundCostsHalfFtlPercent (number): Costs for 1/2 truck.
        - minimumInboundReplenishmentFrequency (number): Minimum number of shipments that should go between a factory and a warehouse.
        - minimumOutboundReplenishmentFrequency (number): Minimum number of shipments that should go between a warehouse and a customer.
        - weightCostFunction (str): ID of the relevant weight cost function.
        - volumeCostFunction (str): ID of the relevant volume cost function.
    customers (pd.DataFrame): Customer data with its address and its shipment structure for the optimization run.
        - name (str): Customer name.
        - latitude (number): Customer latitude.
        - longitude (number): Customer longitude.
        - weight (number): Average weight of a shipment that goes to this customer.
        - volume (number): Average volume of a shipment that goes to this customer.
        - numberOfShipments (number): Total number of shipments (integer value) the customer receives.
        - productSegments (str): Influences which warehouses could be used to fulfill the customer demand.
        - factory (str): The factory that delivers to the customer.
        - warehouse (str): The warehouse that delivers to the customer.
        - maximumWarehouseDistance (number): Maximum allowed distance from the assigned warehouse.
        - penaltyCostsWarehouseDistance (number): Penalty costs per distance unit.
    product_segments (pd.DataFrame): Data for the existing product segments, and the available warehouses for each of segment. 
        - segmentName (str): Name of a specific product segment.
        - availableWarehouses (str): List of warehouses which could be used for a specific segment separated with a semicolon.
    transport_costs (pd.DataFrame): Defining detailed transport costs for all factory-warehouse and warehouse-customer relations.
        - startLocationName (str): Start name of the relation.
        - endLocationName (str): End name of the relation.
        - weightCapacity (number): Capacity for the weight dimension for the transport unit.
        - volumeCapacity (number): Capacity for the volume dimension for the transport unit.
        - costsPerUnit (number): Costs per transport unit.
    transport_costs_rules (pd.DataFrame): Defining general rules and the corresponding vehicle capacities transport costs.
        - fromCountryIso2 (str): ISO 2 code of the sender country.
        - fromZip (str): Postal code of the sender.
        - fromName (str): Start name of the relation. 
        - toCountryIso2 (str): ISO 2 code of the recipient country.
        - toZip (str): Postal code of the recipient.
        - toName (str): End name of the relation. 
        - layer (str): The direction of the flow, can only be "inbound" (from factory to warehouse) or "outbound" 
                       (from warehouse to customer).
        - distance (number): Distance between sender and recipient.
        - weightCapacityPerUnit (number): Capacity for the weight dimension for the transport unit.
        - volumeCapacityPerUnit (number): Capacity for the volume dimension for the transport unit.
        - costsPerUnit (number): Costs per transport unit.
    stepwise_function_weight (pd.DataFrame): Data for a stepwise (piecewise) cost function for the weight dimension.   
        - stepFunctionId (str): ID of the respective cost function.
        - stepEnd (number): An upper limit for a specific step.
        - fixedCost (number): Fixed cost for a specific step.
        - costPerWeightUnit (number): Cost per weight unit for a specific step.
    stepwise_function_volume (pd.DataFrame): Data for a stepwise (piecewise) cost function for the volume dimension.   
        - stepFunctionId (str): ID of the respective cost function.
        - stepEnd (number): An upper limit for a specific step.
        - fixedCost (number): Fixed cost for a specific step.
        - costPerVolumeUnit (number): Cost per volume unit for a specific step.
    distance_limits (pd.DataFrame): Data specifying the maximum distance within which a given percentage of total demand must be met.
        - distanceLimit (number):  Maximum possible distance between the warehouse and delivery points.
        - weightPercentage (number): Minimum percentage of total weight that needs to be covered within the specified distance.
        - volumePercentage (number): Minimum percentage of total volume that needs to be covered within the specified distance.
        - distanceLimitPenalty (number): Penalty cost, if the constraint would not be fulfilled.

    parametrs (dict): A dictionary containing parameters distanceUnit (enum 'km' or 'mi'), vehicleType (enum 'car' or 
                      'truck'), streetLevel (boolean), inboundConsolidation (boolean), outboundConsolidation (boolean), 
                      allowMultisourcing (boolean), minWarehouses (integer number), maxWarehouses (integer number).

    api_key (str): The Log-hub API key for accessing the network design service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    dict: A dictionary containing url and apiServer that should be passed to a GET method in order to get output tables, along with the explanation. 
    """
    factories_columns = {
        'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'minimumFtlCosts': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'minimumLtlCosts': 'float', 'outboundCostsHalfFtlPercent': 'float'
    }
    warehouses_columns = {
        'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float', 'fixed': 'float', 'minWeight': 'float', 'maxWeight': 'float', 'penaltyCostsWeight': 'float', 'minVolume': 'float', 'maxVolume': 'float', 'penaltyCostsVolume': 'float','fixedCosts': 'float','costsPerWeightUnit': 'float', 'costsPerVolumeUnit': 'float', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'minimumFtlCosts': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'minimumLtlCosts': 'float', 'outboundCostsHalfFtlPercent': 'float', 'minimumInboundReplenishmentFrequency': 'float', 'minimumOutboundReplenishmentFrequency': 'float', 'weightCostFunction': 'str', 'volumeCostFunction': 'str'
    }
    customers_columns = {
        'id': 'float', 'name': 'str', 'latitude': 'float', 'longitude': 'float', 'weight': 'float', 'volume': 'float', 'numberOfShipments': 'float', 'productSegments': 'str', 'factory': 'str', 'warehouse': 'str', 'maximumWarehouseDistance': 'float', 'penaltyCostsWarehouseDistance': 'float',
    }
    product_segments_columns = {
        'id': 'float', 'segmentName': 'str', 'availableWarehouses': 'str'
    }
    transport_costs_columns = {
        'id': 'float', 'startLocationName': 'str', 'endLocationName': 'str', 'weightCapacity': 'float', 'volumeCapacity': 'float', 'costsPerUnit': 'float',
    }
    transport_costs_rules_columns = {
        'id': 'float', 'fromCountryIso2': 'str', 'fromZip': 'str',  'fromName': 'str', 'toCountryIso2': 'str', 'toZip': 'str', 'toName': 'str', 'layer': 'str', 'distance': 'float', 'weightCapacityPerUnit': 'float', 'volumeCapacityPerUnit': 'float', 'costsPerUnit': 'float'
    }
    stepwise_function_weight_columns = {
        'id': 'float', 'stepFunctionId': 'str', 'stepEnd': 'float', 'fixedCost': 'float', 'costPerWeightUnit': 'float',
        }
    stepwise_function_volume_columns = {
        'id': 'float', 'stepFunctionId': 'str', 'stepEnd': 'float', 'fixedCost': 'float', 'costPerVolumeUnit': 'float',
        }
    distance_limits_columns = {
        'id': 'float', 'distanceLimit': 'str',  'weightPercentage': 'str', 'volumePercentage': 'str', 'distanceLimitPenalty': 'str', 
        }

    # Validate and convert data types
    factories = convert_df_to_dict_excluding_nan(factories, factories_columns)
    warehouses = convert_df_to_dict_excluding_nan(warehouses, warehouses_columns)
    customers = convert_df_to_dict_excluding_nan(customers, customers_columns)
    product_segments = convert_df_to_dict_excluding_nan(product_segments, product_segments_columns)
    transport_costs = convert_df_to_dict_excluding_nan(transport_costs, transport_costs_columns)
    transport_costs_rules = convert_df_to_dict_excluding_nan(transport_costs_rules, transport_costs_rules_columns)
    stepwise_function_weight = convert_df_to_dict_excluding_nan(stepwise_function_weight, stepwise_function_weight_columns)
    stepwise_function_volume = convert_df_to_dict_excluding_nan(stepwise_function_volume, stepwise_function_volume_columns)
    distance_limits = convert_df_to_dict_excluding_nan(distance_limits, distance_limits_columns)

    if any(df is None for df in [factories, warehouses, customers, product_segments, transport_costs, transport_costs_rules, stepwise_function_weight, stepwise_function_volume, distance_limits]):
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversenetworkdesignpluslongrun"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'factories': factories,
        'warehouses': warehouses,
        'customers': customers,
        'productSegments': product_segments,
        'transportCosts': transport_costs,
        'transportsCostsRules': transport_costs_rules,
        'stepwiseCostFunctionWeight': stepwise_function_weight,
        'stepwiseCostFunctionVolume': stepwise_function_volume,
        'distanceLimits': distance_limits,
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
                logging.error(f"Error in reverse network design plus API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def reverse_network_design_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'NetworkDesignPlusReverse.xlsx')
    factories_df = pd.read_excel(data_path, sheet_name='factories', usecols='A:K').fillna("")
    warehouses_df = pd.read_excel(data_path, sheet_name='warehouses', usecols='A:Y').fillna("")
    customers_df = pd.read_excel(data_path, sheet_name='customers', usecols='A:L').fillna("")
    product_segments_df = pd.read_excel(data_path, sheet_name='productSegments', usecols='A:C').fillna("")
    transport_costs_df = pd.read_excel(data_path, sheet_name='transportCosts', usecols='A:F').fillna("")
    transport_costs_rules_df = pd.read_excel(data_path, sheet_name='transportCostsRules', usecols='A:L').fillna("")
    stepwise_function_weight_df = pd.read_excel(data_path, sheet_name='stepwiseCostFunctionWeight', usecols='A:E').fillna("")
    stepwise_function_volume_df = pd.read_excel(data_path, sheet_name='stepwiseCostFunctionVolume', usecols='A:E').fillna("")
    distance_limits_df = pd.read_excel(data_path, sheet_name='distanceLimits', usecols='A:E').fillna("")
    parameters = {
        "distanceUnit": "km",
        "vehicleType": "car",
        "streetLevel": False,
        "inboundConsolidation": True,
        "outboundConsolidation": False,
        "allowMultisourcing": True,
        "minWarehouses": 1,
        "maxWarehouses": 2

    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'factories': factories_df, 'warehouses': warehouses_df, 'customers': customers_df, 'productSegments': product_segments_df, 'transportCosts': transport_costs_df, 'transportCostsRules': transport_costs_rules_df, 'stepwiseCostFunctionWeight': stepwise_function_weight_df, 'stepwiseCostFunctionVolume': stepwise_function_volume_df, 'distanceLimits': distance_limits_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

if __name__ == "__main__":

    api_key_dev = "e75d5db6ca8e6840e185bc1c63f20f39e65fbe0b"
    workspace_id = "7cb180c0d9e15db1a71342df559d19d473c539ad"

    sample = forward_network_design_plus_sample_data()

    factories = sample['factories']
    warehouses = sample['warehouses']
    customers = sample['customers']
    prod_segments = sample['productSegments']
    transport_costs = sample['transportCosts']
    transport_costs_rules = sample['transportCostsRules']
    stepwise_weight = sample['stepwiseCostFunctionWeight']
    stepwise_volume = sample['stepwiseCostFunctionVolume']
    distance_limits = sample['distanceLimits']
    par = sample['parameters']
    save_scenario = sample['saveScenarioParameters']

    out = forward_network_design_plus(factories, warehouses, customers, prod_segments, transport_costs, transport_costs_rules, stepwise_weight, stepwise_volume, distance_limits, par, api_key_dev, save_scenario)



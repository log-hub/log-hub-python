import os
import requests
import pandas as pd
import time
import logging
from typing import Optional, Tuple
import warnings
logging.basicConfig(level=logging.INFO)
from pyloghub.save_to_platform import save_scenario_check


def forward_network_design_plus(factories: pd.DataFrame, warehouses: pd.DataFrame, customers: pd.DataFrame, product_segments: pd.DataFrame, transport_costs: pd.DataFrame, transport_costs_rules: pd.DataFrame, stepwise_function_weight: pd.DataFrame, stepwise_function_volume: pd.DataFrame, distance_limits: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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

    api_key (str): The Log-hub API key for accessing the geocoding service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Four pandas DataFrames containing open warehouses, 
                        factory-warehouse assignment, customer-warehouse assignment and KPIs table. Returns None if the process fails. 
    """
    
    def validate_and_convert_data_types(df, required_columns):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        for col, dtype in required_columns.items():
            if col not in df.columns:
                logging.error(f"Missing required column: {col}")
                return None
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                logging.error(f"Data type conversion failed for column '{col}': {e}")
                return None
        return df
    
    factories_columns = {
        'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 
        'street': 'str', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'minimumFtlCosts': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'minimumLtlCosts': 'float', 'outboundCostsHalfFtlPercent': 'float'
    }
    warehouses_columns = {
        'name': 'str', 'country': 'str', 'state' : 'str', 'postalCode': 'str', 'city': 'str', 'fixed': 'float', 'minWeight': 'float', 'maxWeight': 'float', 'penaltyCostsWeight': 'float', 'minVolume': 'float', 'maxVolume': 'float', 'penaltyCostsVolume': 'float','fixedCosts': 'float','costsPerWeightUnit': 'float', 'costsPerVolumeUnit': 'float', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'minimumFtlCosts': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'minimumLtlCosts': 'float', 'outboundCostsHalfFtlPercent': 'float', 'minimumInboundReplenishmentFrequency': 'float', 'minimumOutboundReplenishmentFrequency': 'float', 'weightCostFunction': 'str', 'volumeCostFunction': 'str'
    }
    customers_columns = {
        'name': 'str', 'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'weight': 'float', 'volume': 'float', 'numberOfShipments': 'float', 'productSegments': 'str', 'factory': 'str', 'warehouse': 'str', 'maximumWarehouseDistance': 'float', 'penaltyCostsWarehouseDistance': 'float',
    }
    product_segments_columns = {
        'segmentName': 'str', 'availableWarehouses': 'str'
    }
    transport_costs_columns = {
        'startLocationName': 'str', 'endLocationName': 'str', 'weightCapacity': 'float', 'volumeCapacity': 'float', 'costsPerUnit': 'float',
    }
    transport_costs_rules_columns = {
        'fromCountryIso2': 'str', 'fromZip': 'str',  'fromName': 'str', 'toCountryIso2': 'str', 'toZip': 'str', 'toName': 'str', 'layer': 'str', 'distance': 'float', 'weightCapacityPerUnit': 'float', 'volumeCapacityPerUnit': 'float', 'costsPerUnit': 'float'
    }
    stepwise_function_weight_columns = {
        'stepFunctionId': 'str', 'stepEnd': 'float', 'fixedCost': 'float', 'costPerWeightUnit': 'float',
        }
    stepwise_function_volume_columns = {
        'stepFunctionId': 'str', 'stepEnd': 'float', 'fixedCost': 'float', 'costPerVolumeUnit': 'float',
        }
    distance_limits_columns = {
        'distanceLimit': 'float',  'weightPercentage': 'float', 'volumePercentage': 'float', 'distanceLimitPenalty': 'float', 
        }

    # Validate and convert data types
    factories = validate_and_convert_data_types(factories, factories_columns)
    warehouses = validate_and_convert_data_types(warehouses, warehouses_columns)
    customers = validate_and_convert_data_types(customers, customers_columns)
    product_segments = validate_and_convert_data_types(product_segments, product_segments_columns)
    transport_costs = validate_and_convert_data_types(transport_costs, transport_costs_columns)
    transport_costs_rules = validate_and_convert_data_types(transport_costs_rules, transport_costs_rules_columns)
    stepwise_function_weight = validate_and_convert_data_types(stepwise_function_weight, stepwise_function_weight_columns)
    stepwise_function_volume = validate_and_convert_data_types(stepwise_function_volume, stepwise_function_volume_columns)
    distance_limits = validate_and_convert_data_types(distance_limits, distance_limits_columns)

    if any(df is None for df in [factories, warehouses, customers, product_segments, transport_costs, transport_costs_rules, stepwise_function_weight, stepwise_function_volume, distance_limits]):
        return None
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/geocoding"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        'addresses': addresses.to_dict(orient='records'),
    }
    payload = save_scenario_check(save_scenario, payload)

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                geocoded_data_df = pd.DataFrame(response_data['geocodes'])
                return geocoded_data_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in geocoding API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_geocoding_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'GeocodingSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:F').fillna("")
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'addresses': addresses_df, 'saveScenarioParameters': save_scenario}

def reverse_geocoding(geocodes: pd.DataFrame, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Perform reverse geocoding on a list of latitude and longitude coordinates.

    This function takes a DataFrame of geocodes (latitude and longitude) and an API key, 
    and performs reverse geocoding using the Log-hub reverse geocoding service. The function 
    handles batching and rate limiting by the API.

    Parameters:
    geocodes (pd.DataFrame): A pandas DataFrame containing the geocodes to be reverse geocoded.
        Required columns and their types:
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.

    api_key (str): The Log-hub API key for accessing the reverse geocoding service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containing the original geocode information along 
                  with the reverse geocoded address results. Includes fields like country, 
                  state, city, and street. Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        float_columns = ['latitude', 'longitude']
        for col in float_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='raise')
                except Exception as e:
                    logging.error(f"Data type conversion failed for column '{col}': {e}")
                    return None
            else:
                logging.error(f"Missing required column: {col}")
                return None
        return df

    # Validate and convert data types
    geocodes = validate_and_convert_data_types(geocodes)
    if geocodes is None:
        return None
    
    # Convert the latitude and longitude columns to a list of dictionaries
    geocodes = geocodes.applymap(lambda x: x.to_dict() if isinstance(x, pd.Series) else x)
    geocodes = geocodes.to_dict(orient='records')
    
    # Convert the list of dictionaries to a list of lists
    geocodes = [list(d.values()) for d in geocodes]
    
    # Convert the list of lists to a list of dictionaries
    geocodes = [{"latitude": lat, "longitude": lon} for lat, lon in geocodes]
    
    # Convert the list of dictionaries to a pandas DataFrame
    geocodes = pd.DataFrame(geocodes)
    
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversegeocoding"

    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "geocodes": geocodes.to_dict(orient='records')
    }
    payload = save_scenario_check(save_scenario, payload)

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                reverse_geocoding_df = pd.DataFrame(response_data['addresses'])
                return reverse_geocoding_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in reverse geocoding API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def reverse_geocoding_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'GeocodingSampleDataReverse.xlsx')
    geocodes_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:B')
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'geocodes': geocodes_df, 'saveScenarioParameters': save_scenario}
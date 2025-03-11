import os
import pandas as pd
import logging
import warnings
logging.basicConfig(level=logging.INFO)
from typing import Optional, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import exclude_nan_depending_on_dtype, convert_to_float, validate_and_convert_data_types, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url, get_method, get_workspace_entities

def forward_network_design_plus(factories: pd.DataFrame, warehouses: pd.DataFrame, customers: pd.DataFrame, product_segments: pd.DataFrame, transport_costs: pd.DataFrame, transport_costs_rules: pd.DataFrame, stepwise_function_weight: pd.DataFrame, stepwise_function_volume: pd.DataFrame, distance_limits: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Four dataframes with the information about opened warehouses, factory and customer assignment, and solution kpis. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    factories_mandatory_columns = {
       'name': 'str', 'country': 'str', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'outboundCostsHalfFtlPercent': 'float'
    }
    factories_optional_columns = { 'id': 'float', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'}
    factories_optional_float = ['minimumFtlCosts', 'minimumLtlCosts']
    warehouses_mandatory_columns = {
        'name': 'str', 'country': 'str', 'fixed': 'float', 'minWeight': 'float', 'maxWeight': 'float', 'minVolume': 'float', 'maxVolume': 'float','fixedCosts': 'float','costsPerWeightUnit': 'float', 'costsPerVolumeUnit': 'float', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'outboundCostsHalfFtlPercent': 'float'
    }
    warehouses_optional_columns = {'id': 'float', 'state' : 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'weightCostFunction': 'str', 'volumeCostFunction': 'str'}
    warehouses_optional_float = ['penaltyCostsWeight', 'penaltyCostsVolume', 'minimumFtlCosts', 'minimumLtlCosts', 'minimumInboundReplenishmentFrequency', 'minimumOutboundReplenishmentFrequency']
    customers_mandatory_columns = {
        'name': 'str', 'country': 'str', 'weight': 'float', 'volume': 'float', 'numberOfShipments': 'float'
    }
    customers_optional_columns = {'id': 'float', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'productSegments': 'str', 'factory': 'str', 'warehouse': 'str'}
    customers_optional_float = ['maximumWarehouseDistance', 'penaltyCostsWarehouseDistance']
    product_segments_optional_columns = {
        'id': 'float', 'segmentName': 'str', 'availableWarehouses': 'str'
    }
    transport_costs_mandatory_columns = {
        'startLocationName': 'str', 'endLocationName': 'str', 'volumeCapacity': 'float', 'costsPerUnit': 'float',
    }
    transport_costs_optional_columns = {'id': 'float'}
    transport_costs_optional_float = ['weightCapacity']
    transport_costs_rules_optional_columns = {
        'id': 'float', 'fromCountryIso2': 'str', 'fromZip': 'str',  'fromName': 'str', 'toCountryIso2': 'str', 'toZip': 'str', 'toName': 'str', 'layer': 'str'
    }
    transport_costs_rules_optional_float = ['distance', 'weightCapacityPerUnit', 'volumeCapacityPerUnit', 'costsPerUnit']
    stepwise_function_weight_optional_columns = {
        'id': 'float', 'stepFunctionId': 'str'
        }
    stepwise_function_weight_optional_float = ['stepEnd', 'fixedCost', 'costPerWeightUnit']
    stepwise_function_volume_optional_columns = {
        'id': 'float', 'stepFunctionId': 'str'
        }
    stepwise_function_volume_optional_float = ['stepEnd', 'fixedCost', 'costPerVolumeUnit']
    distance_limits_columns = {
        'id': 'float', 'distanceLimit': 'str',  'weightPercentage': 'str', 'volumePercentage': 'str', 'distanceLimitPenalty': 'str', 
        }

    # Validate and convert data types
    factories = validate_and_convert_data_types(factories, factories_mandatory_columns, 'mandatory', 'factories')
    if not factories is None:
        factories = validate_and_convert_data_types(factories, factories_optional_columns, 'optional', 'factories')
        if not factories is None:
            factories = convert_to_float(factories, factories_optional_float, 'optional')
            factories = convert_df_to_dict_excluding_nan(factories, factories_optional_float)

    warehouses = validate_and_convert_data_types(warehouses, warehouses_mandatory_columns, 'mandatory', 'warehouses')
    if not warehouses is None:
        warehouses = validate_and_convert_data_types(warehouses, warehouses_optional_columns, 'optional', 'warehouses')
        if not warehouses is None:
            warehouses = convert_to_float(warehouses, warehouses_optional_float, 'optional')
            warehouses = convert_df_to_dict_excluding_nan(warehouses,warehouses_optional_float)

    customers = validate_and_convert_data_types(customers, customers_mandatory_columns, 'mandatory', 'customers')
    if not customers is None:
        customers = validate_and_convert_data_types(customers, customers_optional_columns, 'optional', 'customers')
        if not customers is None:
            customers = convert_to_float(customers, customers_optional_float, 'optional')
            customers = convert_df_to_dict_excluding_nan(customers, customers_optional_float)

    product_segments = validate_and_convert_data_types(product_segments, product_segments_optional_columns, 'optional', 'roduct segments')
    
    transport_costs = validate_and_convert_data_types(transport_costs, transport_costs_mandatory_columns, 'mandatory', 'transport costs')
    if not transport_costs is None:
        transport_costs = validate_and_convert_data_types(transport_costs, transport_costs_optional_columns, 'optional', 'transport costs')
        if not transport_costs is None:
            transport_costs = convert_to_float(transport_costs, transport_costs_optional_float, 'optional')
            transport_costs = convert_df_to_dict_excluding_nan(transport_costs, transport_costs_optional_float)

    transport_costs_rules = validate_and_convert_data_types(transport_costs_rules, transport_costs_rules_optional_columns, 'optional', 'transport costs rules')
    if not transport_costs_rules is None:
        transport_costs_rules = convert_to_float(transport_costs_rules, transport_costs_rules_optional_float, 'optional')
        transport_costs_rules = convert_df_to_dict_excluding_nan(transport_costs_rules, transport_costs_rules_optional_float)

    stepwise_function_weight = validate_and_convert_data_types(stepwise_function_weight, stepwise_function_weight_optional_columns, 'optional', 'stepwise function weight')
    if not stepwise_function_weight is None:
        stepwise_function_weight = convert_to_float(stepwise_function_weight, stepwise_function_weight_optional_float, 'optional')
        stepwise_function_weight = convert_df_to_dict_excluding_nan(stepwise_function_weight, stepwise_function_weight_optional_float)

    stepwise_function_volume = validate_and_convert_data_types(stepwise_function_volume, stepwise_function_volume_optional_columns, 'optional', 'stepwise function volume')
    if not stepwise_function_volume is None:
        stepwise_function_volume = convert_to_float(stepwise_function_volume, stepwise_function_volume_optional_float, 'optional')
        stepwise_function_volume = convert_df_to_dict_excluding_nan(stepwise_function_volume, stepwise_function_volume_optional_float)

    distance_limits = validate_and_convert_data_types(distance_limits, distance_limits_columns, 'optional', 'distance limits')

    if any(df is None for df in [factories, warehouses, customers, product_segments, transport_costs, transport_costs_rules, stepwise_function_weight, stepwise_function_volume, distance_limits]):
        return None
    
    url = create_url("networkdesignpluslongrun")
    
    headers = create_headers(api_key)

    payload = {
        'factories': factories,
        'warehouses': warehouses,
        'customers': customers,
        'productSegments': product_segments.to_dict(orient='records'),
        'transportCosts': transport_costs,
        'transportsCostsRules': transport_costs_rules,
        'stepwiseCostFunctionWeight': stepwise_function_weight,
        'stepwiseCostFunctionVolume': stepwise_function_volume,
        'distanceLimits': distance_limits.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "network design plus")
    if response_data is None:
        return None
    else:
        result = response_data['result']
        get_method_result = get_method(result['apiServer'], result['url'], {"authorization": f"apikey {api_key}"}, "network design plus")
        if get_method_result is None:
            return None
        else:
            open_warehouses = pd.DataFrame(get_method_result['openWarehouses'])
            factory_assignment = pd.DataFrame(get_method_result['factoryAssignment'])
            customer_assignment = pd.DataFrame(get_method_result['customerAssignment'])
            solution_kpis = pd.DataFrame(get_method_result['solutionKpis'])
            if (show_buttons and save_scenario['saveScenario']):
                create_buttons()
            if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
                logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
            return open_warehouses, factory_assignment, customer_assignment,solution_kpis

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

def reverse_network_design_plus(factories: pd.DataFrame, warehouses: pd.DataFrame, customers: pd.DataFrame, product_segments: pd.DataFrame, transport_costs: pd.DataFrame, transport_costs_rules: pd.DataFrame, stepwise_function_weight: pd.DataFrame, stepwise_function_volume: pd.DataFrame, distance_limits: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Four dataframes with the information about opened warehouses, factory and customer assignment, and solution kpis. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    factories_mandatory_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'outboundCostsHalfFtlPercent': 'float'
    }
    factories_optional_float = ['id', 'minimumFtlCosts', 'minimumLtlCosts']
    warehouses_mandatory_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float', 'fixed': 'float', 'minWeight': 'float', 'maxWeight': 'float', 'minVolume': 'float', 'maxVolume': 'float', 'fixedCosts': 'float','costsPerWeightUnit': 'float', 'costsPerVolumeUnit': 'float', 'outboundFtlCapacityWeight': 'float', 'outboundFtlCapacityVolume': 'float', 'outboundFtlCost1DistanceUnit': 'float', 'outboundFtlCost1000DistanceUnit': 'float', 'outboundCostsHalfFtlPercent': 'float'
    }
    warehouses_optional_columns = {'weightCostFunction': 'str', 'volumeCostFunction': 'str'}
    warehouses_optional_float = ['id', 'penaltyCostsWeight', 'penaltyCostsVolume', 'minimumFtlCosts', 'minimumLtlCosts', 'minimumInboundReplenishmentFrequency', 'minimumOutboundReplenishmentFrequency']
    customers_mandatory_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float', 'weight': 'float', 'volume': 'float', 'numberOfShipments': 'float'
    }
    customers_optional_columns = {'productSegments': 'str', 'factory': 'str', 'warehouse': 'str'}
    customers_optional_float = ['id', 'maximumWarehouseDistance', 'penaltyCostsWarehouseDistance']
    product_segments_optional_columns = {
        'id': 'float', 'segmentName': 'str', 'availableWarehouses': 'str'
    }
    transport_costs_mandatory_columns = {
        'startLocationName': 'str', 'endLocationName': 'str', 'volumeCapacity': 'float', 'costsPerUnit': 'float',
    }
    transport_costs_optional_columns = {'id': 'float'}
    transport_costs_optional_float = ['weightCapacity']
    transport_costs_rules_optional_columns = {
        'id': 'float', 'fromCountryIso2': 'str', 'fromZip': 'str',  'fromName': 'str', 'toCountryIso2': 'str', 'toZip': 'str', 'toName': 'str', 'layer': 'str'
    }
    transport_costs_rules_optional_float = ['distance', 'weightCapacityPerUnit', 'volumeCapacityPerUnit', 'costsPerUnit']
    stepwise_function_weight_optional_columns = {
        'id': 'float', 'stepFunctionId': 'str'
        }
    stepwise_function_weight_optional_float = ['stepEnd', 'fixedCost', 'costPerWeightUnit']
    stepwise_function_volume_optional_columns = {
        'id': 'float', 'stepFunctionId': 'str'
        }
    stepwise_function_volume_optional_float = ['stepEnd', 'fixedCost', 'costPerVolumeUnit']
    distance_limits_columns = {
        'id': 'float', 'distanceLimit': 'str',  'weightPercentage': 'str', 'volumePercentage': 'str', 'distanceLimitPenalty': 'str', 
        }

    # Validate and convert data types
    factories = validate_and_convert_data_types(factories, factories_mandatory_columns, 'mandatory', 'factories')
    if not factories is None:
        factories = convert_to_float(factories, factories_optional_float, 'optional')
        factories = convert_df_to_dict_excluding_nan(factories, factories_optional_float)

    warehouses = validate_and_convert_data_types(warehouses, warehouses_mandatory_columns, 'mandatory', 'warehouses')
    if not warehouses is None:
        warehouses = validate_and_convert_data_types(warehouses, warehouses_optional_columns, 'optional', 'warehouses')
        if not warehouses is None:
            warehouses = convert_to_float(warehouses, warehouses_optional_float, 'optional')
            warehouses = convert_df_to_dict_excluding_nan(warehouses,warehouses_optional_float)

    customers = validate_and_convert_data_types(customers, customers_mandatory_columns, 'mandatory', 'customers')
    if not customers is None:
        customers = validate_and_convert_data_types(customers, customers_optional_columns, 'optional', 'customers')
        if not customers is None:
            customers = convert_to_float(customers, customers_optional_float, 'optional')
            customers = convert_df_to_dict_excluding_nan(customers, customers_optional_float)

    product_segments = validate_and_convert_data_types(product_segments, product_segments_optional_columns, 'optional', 'product segments')
    
    transport_costs = validate_and_convert_data_types(transport_costs, transport_costs_mandatory_columns, 'mandatory', 'transport costs')
    if not transport_costs is None:
        transport_costs = validate_and_convert_data_types(transport_costs, transport_costs_optional_columns, 'optional', 'transport costs')
        if not transport_costs is None:
            transport_costs = convert_to_float(transport_costs, transport_costs_optional_float, 'optional')
            transport_costs = convert_df_to_dict_excluding_nan(transport_costs, transport_costs_optional_float)

    transport_costs_rules = validate_and_convert_data_types(transport_costs_rules, transport_costs_rules_optional_columns, 'optional', 'transport costs rules')
    if not transport_costs_rules is None:
        transport_costs_rules = convert_to_float(transport_costs_rules, transport_costs_rules_optional_float, 'optional')
        transport_costs_rules = convert_df_to_dict_excluding_nan(transport_costs_rules, transport_costs_rules_optional_float)
    
    stepwise_function_weight = validate_and_convert_data_types(stepwise_function_weight, stepwise_function_weight_optional_columns, 'optional', 'stepwise function weight')
    if not stepwise_function_weight is None:
        stepwise_function_weight = convert_to_float(stepwise_function_weight, stepwise_function_weight_optional_float, 'optional')
        stepwise_function_weight = convert_df_to_dict_excluding_nan(stepwise_function_weight, stepwise_function_weight_optional_float)

    stepwise_function_volume = validate_and_convert_data_types(stepwise_function_volume, stepwise_function_volume_optional_columns, 'optional', 'stepwise function volume')
    if not stepwise_function_volume is None:
        stepwise_function_volume = convert_to_float(stepwise_function_volume, stepwise_function_volume_optional_float, 'optional')
        stepwise_function_volume = convert_df_to_dict_excluding_nan(stepwise_function_volume, stepwise_function_volume_optional_float)

    distance_limits = validate_and_convert_data_types(distance_limits, distance_limits_columns, 'optional', 'distance limits')

    if any(df is None for df in [factories, warehouses, customers, product_segments, transport_costs, transport_costs_rules, stepwise_function_weight, stepwise_function_volume, distance_limits]):
        return None
    
    url = create_url("reversenetworkdesignpluslongrun")
    
    headers = create_headers(api_key)

    payload = {
        'factories': factories,
        'warehouses': warehouses,
        'customers': customers,
        'productSegments': product_segments.to_dict(orient='records'),
        'transportCosts': transport_costs,
        'transportsCostsRules': transport_costs_rules,
        'stepwiseCostFunctionWeight': stepwise_function_weight,
        'stepwiseCostFunctionVolume': stepwise_function_volume,
        'distanceLimits': distance_limits.to_dict(orient='records'),
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "network design plus")
    if response_data is None:
        return None
    else:
        result = response_data['result']
        get_method_result = get_method(result['apiServer'], result['url'], {"authorization": f"apikey {api_key}"}, "network design plus")
        if get_method_result is None:
            return None
        else:
            open_warehouses = pd.DataFrame(get_method_result['openWarehouses'])
            factory_assignment = pd.DataFrame(get_method_result['factoryAssignment'])
            customer_assignment = pd.DataFrame(get_method_result['customerAssignment'])
            solution_kpis = pd.DataFrame(get_method_result['solutionKpis'])
            if (show_buttons and save_scenario['saveScenario']):
                create_buttons()
            if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
                logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
            return open_warehouses, factory_assignment, customer_assignment,solution_kpis
        
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



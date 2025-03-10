import os
import pandas as pd
import logging
import warnings
logging.basicConfig(level=logging.INFO)
from typing import Optional, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import exclude_nan_depending_on_dtype, remove_nonexisting_optional_columns
from sending_requests import post_method, create_headers, create_url, get_method, get_workspace_entities

def forward_location_planning(customers: pd.DataFrame, warehouses: pd.DataFrame, costs_adjustments: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Three dataframes with the information about opened warehouses, customer assignment, and solution kpis. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    #removes missing optional columns from the list and merges optional and mandatory columns, then validates data types
    customers_mandatory_columns = {'name': 'str', 'country': 'str', 'weight': 'float', 'volume': 'float', 'numberOfShipments': 'float'}
    customers_optional_columns = {'id': 'float', 'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'}
    sent_optional_columns = set(customers.columns) - set(customers_mandatory_columns.keys())
    customers_optional_columns = remove_nonexisting_optional_columns(customers_optional_columns, sent_optional_columns)
    customers_mandatory_columns.update(customers_optional_columns)
    customers = exclude_nan_depending_on_dtype(customers, customers_mandatory_columns, 'customers')

    warehouses_mandatory_columns = {'name': 'str', 'country': 'str', 'fixed': 'float', 'minWeight': 'float', 'maxWeight': 'float', 'minVolume': 'float', 'maxVolume': 'float', 'fixedCosts': 'float','costsPerWeightUnit': 'float', 'costsPerVolumeUnit': 'float'}
    warehouses_optional_columns = {'id': 'float', 'state' : 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'penaltyCostsWeight': 'float', 'penaltyCostsVolume': 'float'}
    sent_optional_columns = set(warehouses.columns) - set(warehouses_mandatory_columns.keys())
    warehouses_optional_columns = remove_nonexisting_optional_columns(warehouses_optional_columns, sent_optional_columns)
    warehouses_mandatory_columns.update(warehouses_optional_columns)
    warehouses = exclude_nan_depending_on_dtype(warehouses, warehouses_mandatory_columns, 'warehouses')

    costs_adjustments_optional_columns = {'id': 'float', 'customerCountryIso2': 'str',  'warehouseCountryIso2': 'str', 'customerName': 'str', 'warehouseName': 'str', 'adjustmentFactor': 'float', 'flatOnTop': 'float'}
    sent_optional_columns = set(costs_adjustments.columns)
    costs_adjustments_optional_columns = remove_nonexisting_optional_columns(costs_adjustments_optional_columns, sent_optional_columns)
    costs_adjustments = exclude_nan_depending_on_dtype(costs_adjustments, costs_adjustments_optional_columns, 'costs_adjustments')

    if any(df is None for df in [warehouses, customers, costs_adjustments]):
        return None
    
    url = create_url("locationplanninglongrun")
    
    headers = create_headers(api_key)

    payload = {
        'customers': customers,
        'warehouses': warehouses,
        'costsAdjustmentTransportationCostsStandard': costs_adjustments,
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "location planning")
    if response_data is None:
        return None
    else:
        result = response_data['result']
        get_method_result = get_method(result['apiServer'], result['url'], {"authorization": f"apikey {api_key}"}, "location planning")
        if get_method_result is None:
            return None
        else:
            open_warehouses = pd.DataFrame(get_method_result['openWarehouses'])
            customer_assignment = pd.DataFrame(get_method_result['customerAssignment'])
            solution_kpis = pd.DataFrame(get_method_result['solutionKpis'])
            if (show_buttons and save_scenario['saveScenario']):
                create_buttons()
            if not save_scenario['saveScenario']:
                logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
            return open_warehouses, customer_assignment,solution_kpis

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
        "minWarehouses": 5,
        "maxWarehouses": 6

    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'warehouses': warehouses_df, 'customers': customers_df, 'costsAdjustments': costs_adjustments_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_location_planning(customers: pd.DataFrame, warehouses: pd.DataFrame, costs_adjustments: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Three dataframes with the information about opened warehouses, customer assignment, and solution kpis. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    #removes missing optional columns from the list and merges optional and mandatory columns, then validates data types
    customers_mandatory_columns = {'name': 'str', 'latitude': 'float', 'longitude': 'float', 'weight': 'float', 'volume': 'float', 'numberOfShipments': 'float'}
    customers_optional_columns = {'id': 'float'}
    sent_optional_columns = set(customers.columns) - set(customers_mandatory_columns.keys())
    customers_optional_columns = remove_nonexisting_optional_columns(customers_optional_columns, sent_optional_columns)
    customers_mandatory_columns.update(customers_optional_columns)
    customers = exclude_nan_depending_on_dtype(customers, customers_mandatory_columns, 'customers')

    warehouses_mandatory_columns = {'name': 'str', 'latitude': 'float', 'longitude': 'float', 'fixed': 'float', 'minWeight': 'float', 'maxWeight': 'float', 'minVolume': 'float', 'maxVolume': 'float', 'fixedCosts': 'float','costsPerWeightUnit': 'float', 'costsPerVolumeUnit': 'float'}
    warehouses_optional_columns = {'id': 'float', 'penaltyCostsWeight': 'float', 'penaltyCostsVolume': 'float'}
    sent_optional_columns = set(warehouses.columns) - set(warehouses_mandatory_columns.keys())
    warehouses_optional_columns = remove_nonexisting_optional_columns(warehouses_optional_columns, sent_optional_columns)
    warehouses_mandatory_columns.update(warehouses_optional_columns)
    warehouses = exclude_nan_depending_on_dtype(warehouses, warehouses_mandatory_columns, 'warehouses')

    costs_adjustments_optional_columns = {'id': 'float', 'customerCountryIso2': 'str',  'warehouseCountryIso2': 'str', 'customerName': 'str', 'warehouseName': 'str', 'adjustmentFactor': 'float', 'flatOnTop': 'float'}
    sent_optional_columns = set(costs_adjustments.columns)
    costs_adjustments_optional_columns = remove_nonexisting_optional_columns(costs_adjustments_optional_columns, sent_optional_columns)
    costs_adjustments = exclude_nan_depending_on_dtype(costs_adjustments, costs_adjustments_optional_columns, 'costs_adjustments')

    if any(df is None for df in [warehouses, customers, costs_adjustments]):
        return None
    
    url = create_url("reverselocationplanninglongrun")
    
    headers = create_headers(api_key)

    payload = {
        'customers': customers,
        'warehouses': warehouses,
        'costsAdjustmentTransportationCostsStandard': costs_adjustments,
        'parameters': parameters
    }
    payload = save_scenario_check(save_scenario, payload)

    response_data = post_method(url, payload, headers, "reverse location planning")
    if response_data is None:
        return None
    else:
        result = response_data['result']
        get_method_result = get_method(result['apiServer'], result['url'], {"authorization": f"apikey {api_key}"}, "reverse location planning")
        if get_method_result is None:
            return None
        else:
            open_warehouses = pd.DataFrame(get_method_result['openWarehouses'])
            customer_assignment = pd.DataFrame(get_method_result['customerAssignment'])
            solution_kpis = pd.DataFrame(get_method_result['solutionKpis'])
            if (show_buttons and save_scenario['saveScenario']):
                create_buttons()
            if not save_scenario['saveScenario']:
                logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
            return open_warehouses, customer_assignment, solution_kpis

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
        "minWarehouses": 5,
        "maxWarehouses": 6

    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'warehouses': warehouses_df, 'customers': customers_df, 'costsAdjustments': costs_adjustments_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
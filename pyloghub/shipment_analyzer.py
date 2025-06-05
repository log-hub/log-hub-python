import os
import pandas as pd
import logging
import warnings
from typing import Optional, Dict, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import convert_dates, validate_and_convert_data_types, convert_to_float, validate_boolean, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url, get_workspace_entities, get_method

def forward_shipment_analyzer(shipments: pd.DataFrame, cost_adjustment: pd.DataFrame, consolidation: pd.DataFrame, surcharges: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform shipment analysis based on shipments, cost adjustments, consolidation settings, surcharges, and parameters.

    Parameters:
    shipments (pd.DataFrame): DataFrame containing shipment information.
        Columns and their types:
        - shipmentId (str): Unique identifier for the shipment.
        - shipmentLeg (str): The leg of the shipment.
        - fromId (str), toId (str): Identifiers for the origin and destination.
        - fromCountry (str), toCountry (str): Country codes for origin and destination.
        - fromState (str), toState (str): State information for origin and destination.
        - fromCity (str), toCity (str): City names for origin and destination.
        - fromPostalCode (str), toPostalCode (str): Postal codes for origin and destination.
        - fromStreet (str), toStreet (str): Street addresses for origin and destination.
        - fromUnLocode (str), toUnLocode (str): UN/LOCODE for origin and destination.
        - fromIataCode (str), toIataCode (str): IATA codes for origin and destination.
        - shippingDate (str), expectedDeliveryDate (str), actualDeliveryDate (str): Dates related to the shipment (Format: YYYY-MM-DD).
        - shippingMode (str): Mode of transportation (e.g., Road, Air).
        - carrier (str): Carrier information.
        - truckShipPlaneType (str): Type of transportation vehicle.
        - speedProfile (str): Speed profile used.
        - distance: Distance betwwen sender and recipient. It will be calculated if not provided
        - weight (float), volume (float), pallets (float): Shipment metrics.
        - shipmentValue (float): Value of the shipment.
        - freightCosts (float): Cost of freight.
        - benchmarkTariff (str): Benchmark tariff information.
        - surcharges (str): Any additional surcharges.

    costAdjustment (pd.DataFrame): DataFrame containing cost adjustment settings.
        Columns and their types:
        - fromIso2Country (str), toIso2Country (str): ISO country codes for adjustment applicability.
        - truckShipPlaneType (str): Type of transportation vehicle for which adjustment is applicable.
        - carrier (str): Carrier information for which adjustment is applicable.
        - benchmarkTariff (str): Benchmark tariff information.
        - factor (float): Adjustment factor.
        - flatOnTop (float): Flat fee on top of the cost.

    consolidation (pd.DataFrame): DataFrame containing consolidation settings.
        Columns and their types:
        - truckShipPlaneType (str): Type of transportation vehicle for consolidation.
        - fromIso2Country (str), toIso2Country (str): ISO country codes for consolidation applicability.
        - carrier (str): Carrier information for consolidation.
        - capacityWeight (float), capacityVolume (float), capacityPallets (float): Capacity metrics for consolidation.
        - consolidationFrequency (str): Frequency of consolidation (e.g., weekly, bi-weekly).

    surcharges (pd.DataFrame): DataFrame containing surcharges information.
        Columns and their types:
        - surcharge (str): Type of surcharge.
        - flatOnTop (float): Flat surcharge amount.

    parameters (Dict): Dictionary containing parameters for the analysis.
        Keys and their types:
        - consolidation (bool): Boolean flag to indicate if consolidation should be considered in the analysis.

    api_key (str): Log-hub API key for accessing the shipment analyzer service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: Two pandas DataFrames containing shipment analysis and transport analysis.
                                    Returns None if the process fails.
    """

    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    shipments_mandatory_columns = {'shipmentId': 'str', 'fromId': 'str', 'toId': 'str', 'shippingDate': 'str', 'weight': 'float'}
    shipments_optional_columns = {'shipmentLeg': 'str', 'fromCountry': 'str', 'toCountry': 'str', 'fromState': 'str', 'toState': 'str',
                    'fromCity': 'str', 'toCity': 'str', 'fromPostalCode': 'str', 'toPostalCode': 'str', 'fromStreet': 'str', 'toStreet': 'str',
                    'fromUnLocode': 'str', 'toUnLocode': 'str', 'fromIataCode': 'str', 'toIataCode': 'str', 'shippingMode': 'str', 'carrier': 'str',
                    'truckShipPlaneType': 'str', 'speedProfile': 'str', 'benchmarkTariff': 'str', 'surcharges': 'str', 'expectedDeliveryDate': 'str', 'actualDeliveryDate': 'str'}
    shipments_optional_floats = ['distance', 'volume', 'pallets', 'shipmentValue', 'freightCosts']

    shipments = validate_and_convert_data_types(shipments, shipments_mandatory_columns, 'mandatory', 'shipments')
    if not shipments is None:
        shipments = validate_and_convert_data_types(shipments, shipments_optional_columns, 'optional', 'shipments')
        if not shipments is None:
            shipments = convert_dates(shipments, ['shippingDate', 'expectedDeliveryDate', 'actualDeliveryDate'])
            shipments = convert_to_float(shipments, shipments_optional_floats, 'optional')
            shipments = convert_df_to_dict_excluding_nan(shipments, shipments_optional_floats)
    cost_adjustment_optional_columns = {'fromIso2Country': 'str', 'toIso2Country': 'str', 'truckShipPlaneType': 'str', 'carrier':'str', 'benchmarkTariff': 'str'}
    cost_adjustment = validate_and_convert_data_types(cost_adjustment, cost_adjustment_optional_columns, 'optional', 'cots adjustment')
    if not cost_adjustment is None:
        cost_adjustment = convert_to_float(cost_adjustment, ['factor', 'flatOnTop'], 'optional')
        cost_adjustment = convert_df_to_dict_excluding_nan(cost_adjustment, ['factor', 'flatOnTop'])
    consolidation_optional_columns = {'fromIso2Country': 'str', 'toIso2Country': 'str', 'truckShipPlaneType': 'str', 'carrier':'str', 'consolidationFrequency': 'str'}
    consolidation = validate_and_convert_data_types(consolidation, consolidation_optional_columns, 'optional', 'consolidation')
    if not consolidation is None:
        consolidation = convert_to_float(consolidation, ['capacityWeight', 'capacityVolume', 'capacityPallets'], 'optional')
        consolidation = convert_df_to_dict_excluding_nan(consolidation, ['capacityWeight', 'capacityVolume', 'capacityPallets'])
    surcharges_optional_columns = {'surcharge': 'str'}
    surcharges = validate_and_convert_data_types(surcharges, surcharges_optional_columns, 'optional', 'surcharges')
    if not surcharges is None:
        surcharges = convert_to_float(surcharges, ['flatOnTop'], 'optional')
        surcharges = convert_df_to_dict_excluding_nan(surcharges, ['flatOnTop'])

    # Validate boolean parameter
    if 'consolidation' in parameters and not validate_boolean(parameters['consolidation']):
        logging.error("Invalid type for 'consolidation' in parameters. It should be boolean.")
        return None
    if any(df is None for df in [shipments, cost_adjustment, consolidation,surcharges]):
        return None

    url = create_url("shipmentanalyzerpluslongrun")
    
    headers = create_headers(api_key)

    payload = {
        "shipments": shipments,
        "costAdjustment": cost_adjustment,
        "consolidation": consolidation,
        "surcharges": surcharges,
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "shipment analyzer plus")
    if response_data is None:
        return None
    else:
        result = response_data['result']
        get_method_result = get_method(result['apiServer'], result['url'], {"authorization": f"apikey {api_key}"}, "shipment analyzer plus")
        if get_method_result is None:
            return None
        else:
            shipments_df = pd.DataFrame(get_method_result['shipments'])
            transports_df = pd.DataFrame(get_method_result['transports'])
            if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
                create_buttons()
            if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
                logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
            return shipments_df, transports_df
           
def forward_shipment_analyzer_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'shipmentAnalyzerAddresses.xlsx')
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:AH').fillna("")
    transport_costs_adjustments_df = pd.read_excel(data_path, sheet_name='transportCostAdjustments', usecols='A:H').fillna("")
    consolidation_df = pd.read_excel(data_path, sheet_name='consolidation', usecols='A:I').fillna("")
    surcharges_df = pd.read_excel(data_path, sheet_name='surcharges', usecols='A:C').fillna("")

    parameters = {
        "consolidation": False
    }

    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }

    return {'shipments': shipments_df, 'transportCostAdjustments': transport_costs_adjustments_df, 'consolidation': consolidation_df, 'surcharges': surcharges_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_shipment_analyzer(shipments: pd.DataFrame, cost_adjustment: pd.DataFrame, consolidation: pd.DataFrame, surcharges: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Perform reverse shipment analysis based on shipments, cost adjustments, consolidation settings, surcharges, and parameters.

    Parameters:
    shipments (pd.DataFrame): DataFrame containing reverse shipment information.
        Columns and their types:
        - shipmentId (str): Unique identifier for the shipment.
        - shipmentLeg (str): The leg of the shipment.
        - fromId (str): Identifier for the origin.
        - fromLatitude (float): Latitude for the origin.
        - fromLongitude (float): Longitude for the origin.
        - toId (str): Identifier for the destination.
        - toLatitude (float): Latitude for the destination.
        - toLongitude (float): Longitude for the destination.
        - shippingDate (str): Date of shipping (Format: YYYY-MM-DD).
        - expectedDeliveryDate (str): Expected delivery date (Format: YYYY-MM-DD).
        - actualDeliveryDate (str): Actual delivery date (Format: YYYY-MM-DD).
        - shippingMode (str): Mode of transportation (e.g., Road, Air).
        - carrier (str): Carrier information.
        - truckShipPlaneType (str): Type of transportation vehicle.
        - speedProfile (str): Speed profile used.
        - distance: Distance between sender and recipient. It will be calculated if not provided.
        - weight (float): Weight of the shipment.
        - volume (float): Volume of the shipment.
        - pallets (float): Number of pallets.
        - shipmentValue (float): Value of the shipment.
        - freightCosts (float): Cost of freight.
        - benchmarkTariff (str): Benchmark tariff information.
        - surcharges (str): Any additional surcharges.

    costAdjustment (pd.DataFrame): DataFrame containing cost adjustment settings.
        [Include Columns and their types Description Here Similar to Forward Analyzer]

    consolidation (pd.DataFrame): DataFrame containing consolidation settings.
        [Include Columns and their types Description Here Similar to Forward Analyzer]

    surcharges (pd.DataFrame): DataFrame containing surcharges information.
        [Include Columns and their types Description Here Similar to Forward Analyzer]

    parameters (Dict): Dictionary containing parameters for the analysis.
        Keys and their types:
        - consolidation (bool): Boolean flag to indicate if consolidation should be considered in the analysis.

    api_key (str): API key for accessing the reverse shipment analyzer service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.
    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: Two pandas DataFrames containing reverse shipment analysis and transport analysis.
                                      The first DataFrame ('shipments') includes details such as shipment IDs, locations, dates, shipment metrics, and calculated emissions and costs.
                                      The second DataFrame ('transports') includes aggregated transport metrics such as total weights, volumes, costs, and emissions for each transport ID.
                                      Returns None if the process fails.
    """

    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    shipments_mandatory_columns = {'shipmentId': 'str', 'fromId': 'str', 'toId': 'str', 'shippingDate': 'str', 'weight': 'float', 'fromLatitude': 'float', 'fromLongitude': 'float', 'toLatitude': 'float', 'toLongitude': 'float'}
    shipments_optional_columns = {'shipmentLeg': 'str', 'fromCountry': 'str', 'toCountry': 'str', 'fromState': 'str', 'toState': 'str',
                    'fromCity': 'str', 'toCity': 'str', 'fromPostalCode': 'str', 'toPostalCode': 'str', 'fromStreet': 'str', 'toStreet': 'str',
                    'fromUnLocode': 'str', 'toUnLocode': 'str', 'fromIataCode': 'str', 'toIataCode': 'str', 'shippingMode': 'str', 'carrier': 'str',
                    'truckShipPlaneType': 'str', 'speedProfile': 'str', 'benchmarkTariff': 'str', 'surcharges': 'str', 'expectedDeliveryDate': 'str', 'actualDeliveryDate': 'str'}
    shipments_optional_floats = ['volume', 'pallets', 'shipmentValue', 'freightCosts', 'distance']

    shipments = validate_and_convert_data_types(shipments, shipments_mandatory_columns, 'mandatory', 'shipments')
    if not shipments is None:
        shipments = validate_and_convert_data_types(shipments, shipments_optional_columns, 'optional', 'shipments')
        if not shipments is None:
            shipments = convert_dates(shipments, ['shippingDate', 'expectedDeliveryDate', 'actualDeliveryDate'])
            shipments = convert_to_float(shipments, shipments_optional_floats, 'optional')
            shipments = convert_df_to_dict_excluding_nan(shipments, shipments_optional_floats)
    cost_adjustment_optional_columns = {'fromIso2Country': 'str', 'toIso2Country': 'str', 'truckShipPlaneType': 'str', 'carrier':'str', 'benchmarkTariff': 'str'}
    cost_adjustment = validate_and_convert_data_types(cost_adjustment, cost_adjustment_optional_columns, 'optional', 'cots adjustment')
    if not cost_adjustment is None:
        cost_adjustment = convert_to_float(cost_adjustment, ['factor', 'flatOnTop'], 'optional')
        cost_adjustment = convert_df_to_dict_excluding_nan(cost_adjustment, ['factor', 'flatOnTop'])
    consolidation_optional_columns = {'fromIso2Country': 'str', 'toIso2Country': 'str', 'truckShipPlaneType': 'str', 'carrier':'str', 'consolidationFrequency': 'str'}
    consolidation = validate_and_convert_data_types(consolidation, consolidation_optional_columns, 'optional', 'consolidation')
    if not consolidation is None:
        consolidation = convert_to_float(consolidation, ['capacityWeight', 'capacityVolume', 'capacityPallets'], 'optional')
        consolidation = convert_df_to_dict_excluding_nan(consolidation, ['capacityWeight', 'capacityVolume', 'capacityPallets'])
    surcharges_optional_columns = {'surcharge': 'str'}
    surcharges = validate_and_convert_data_types(surcharges, surcharges_optional_columns, 'optional', 'surcharges')
    if not surcharges is None:
        surcharges = convert_to_float(surcharges, ['flatOnTop'], 'optional')
        surcharges = convert_df_to_dict_excluding_nan(surcharges, ['flatOnTop'])

    # Validate boolean parameter
    if 'consolidation' in parameters and not validate_boolean(parameters['consolidation']):
        logging.error("Invalid type for 'consolidation' in parameters. It should be boolean.")
        return None
    if any(df is None for df in [shipments, cost_adjustment, consolidation,surcharges]):
        return None

    url = create_url("reverseshipmentanalyzerpluslongrun")
    
    headers = create_headers(api_key)

    payload = {
        "shipments": shipments,
        "costAdjustment": cost_adjustment,
        "consolidation": consolidation,
        "surcharges": surcharges,
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    
    response_data = post_method(url, payload, headers, "reverse shipment analyzer plus")
    if response_data is None:
        return None
    else:
        result = response_data['result']
        get_method_result = get_method(result['apiServer'], result['url'], {"authorization": f"apikey {api_key}"}, "shipment analyzer plus")
        if get_method_result is None:
            return None
        else:
            shipments_df = pd.DataFrame(get_method_result['shipments'])
            transports_df = pd.DataFrame(get_method_result['transports'])
            if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
                create_buttons()
            if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
                logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
            return shipments_df, transports_df
            
def reverse_shipment_analyzer_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'shipmentAnalyzerReverse.xlsx')
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:X').fillna("")
    transport_costs_adjustments_df = pd.read_excel(data_path, sheet_name='transportCostAdjustments', usecols='A:H').fillna("")
    consolidation_df = pd.read_excel(data_path, sheet_name='consolidation', usecols='A:I').fillna("")
    surcharges_df = pd.read_excel(data_path, sheet_name='surcharges', usecols='A:C').fillna("")

    parameters = {
        "consolidation": False
    }

    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'shipments': shipments_df, 'transportCostAdjustments': transport_costs_adjustments_df, 'consolidation': consolidation_df, 'surcharges': surcharges_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
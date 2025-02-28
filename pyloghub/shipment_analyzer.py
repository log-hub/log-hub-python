import os
import pandas as pd
import logging
import warnings
from typing import Optional, Dict, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import convert_dates, convert_to_string, convert_to_float, validate_boolean, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

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

    # Convert date columns to string format (YYYY-MM-DD)
    date_columns = ['shippingDate', 'expectedDeliveryDate', 'actualDeliveryDate']
    shipments = convert_dates(shipments, date_columns)

    # Convert to string
    string_columns = ['shipmentId', 'shipmentLeg', 'fromId', 'toId', 'fromCountry', 'toCountry', 'fromState', 'toState',
                    'fromCity', 'toCity', 'fromPostalCode', 'toPostalCode', 'fromStreet', 'toStreet',
                    'fromUnLocode', 'toUnLocode', 'fromIataCode', 'toIataCode', 'shippingMode', 'carrier',
                    'truckShipPlaneType', 'speedProfile', 'benchmarkTariff', 'surcharges']
    shipments = convert_to_string(shipments, string_columns)

    # Convert numeric columns to float
    numeric_columns = ['weight', 'volume', 'pallets', 'shipmentValue', 'freightCosts']
    shipments = convert_to_float(shipments, numeric_columns)
    cost_adjustment = convert_to_float(cost_adjustment, ['factor', 'flatOnTop'])
    consolidation = convert_to_float(consolidation, ['capacityWeight', 'capacityVolume', 'capacityPallets'])
    surcharges = convert_to_float(surcharges, ['flatOnTop'])
    shipments = convert_df_to_dict_excluding_nan(shipments, numeric_columns)
    cost_adjustment = convert_df_to_dict_excluding_nan(cost_adjustment, ['factor', 'flatOnTop'])
    consolidation = convert_df_to_dict_excluding_nan(consolidation, ['capacityWeight', 'capacityVolume', 'capacityPallets'])
    surcharges = convert_df_to_dict_excluding_nan(surcharges, ['flatOnTop'])

    # Validate boolean parameter
    if 'consolidation' in parameters and not validate_boolean(parameters['consolidation']):
        logging.error("Invalid type for 'consolidation' in parameters. It should be boolean.")
        return None
    if any(df is None for df in [shipments, cost_adjustment, consolidation,surcharges]):
        return None

    url = create_url("shipmentanalyzerplus")
    
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
        shipments_df = pd.DataFrame(response_data['shipments'])
        transports_df = pd.DataFrame(response_data['transports'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return shipments_df, transports_df
           
def forward_shipment_analyzer_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'shipmentAnalyzerAddresses.xlsx')
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:AG').fillna("")
    transport_costs_adjustments_df = pd.read_excel(data_path, sheet_name='transportCostAdjustments', usecols='A:H').fillna("")
    consolidation_df = pd.read_excel(data_path, sheet_name='consolidation', usecols='A:I').fillna("")
    surcharges_df = pd.read_excel(data_path, sheet_name='surcharges', usecols='A:C').fillna("")

    parameters = {
        "consolidation": False
    }

    return {'shipments': shipments_df, 'transportCostAdjustments': transport_costs_adjustments_df, 'consolidation': consolidation_df, 'surcharges': surcharges_df, 'parameters': parameters}


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

    # Convert data types according to the schema
    date_columns = ['shippingDate', 'expectedDeliveryDate', 'actualDeliveryDate']
    shipments = convert_dates(shipments, date_columns)

    string_columns = ['shipmentId', 'shipmentLeg', 'fromId', 'toId', 'shippingMode', 'carrier', 'truckShipPlaneType', 'speedProfile', 'benchmarkTariff', 'surcharges']
    shipments = convert_to_string(shipments, string_columns)

    float_columns = ['fromLatitude', 'fromLongitude', 'toLatitude', 'toLongitude', 'weight', 'volume', 'pallets', 'shipmentValue', 'freightCosts']
    shipments = convert_to_float(shipments, float_columns)

    cost_adjustment = convert_to_float(cost_adjustment, ['factor', 'flatOnTop'])
    consolidation = convert_to_float(consolidation, ['capacityWeight', 'capacityVolume', 'capacityPallets'])
    surcharges = convert_to_float(surcharges, ['flatOnTop'])
    shipments = convert_df_to_dict_excluding_nan(shipments, float_columns)
    cost_adjustment = convert_df_to_dict_excluding_nan(cost_adjustment, ['factor', 'flatOnTop'])
    consolidation = convert_df_to_dict_excluding_nan(consolidation, ['capacityWeight', 'capacityVolume', 'capacityPallets'])
    surcharges = convert_df_to_dict_excluding_nan(surcharges, ['flatOnTop'])

    # Validate boolean parameter
    if 'consolidation' in parameters and not validate_boolean(parameters['consolidation']):
        logging.error("Invalid type for 'consolidation' in parameters. It should be boolean.")
        return None
    if any(df is None for df in [shipments, cost_adjustment, consolidation,surcharges]):
        return None

    url = create_url("reverseshipmentanalyzerplus")
    
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
        shipments_df = pd.DataFrame(response_data['shipments'])
        transports_df = pd.DataFrame(response_data['transports'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return shipments_df, transports_df
            
def reverse_shipment_analyzer_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'shipmentAnalyzerReverse.xlsx')
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:W').fillna("")
    transport_costs_adjustments_df = pd.read_excel(data_path, sheet_name='transportCostAdjustments', usecols='A:H').fillna("")
    consolidation_df = pd.read_excel(data_path, sheet_name='consolidation', usecols='A:I').fillna("")
    surcharges_df = pd.read_excel(data_path, sheet_name='surcharges', usecols='A:C').fillna("")

    parameters = {
        "consolidation": False
    }
    return {'shipments': shipments_df, 'transportCostAdjustments': transport_costs_adjustments_df, 'consolidation': consolidation_df, 'surcharges': surcharges_df, 'parameters': parameters}
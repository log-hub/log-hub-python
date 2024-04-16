import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple


def forward_shipment_analyzer(shipments: pd.DataFrame, costAdjustment: pd.DataFrame, consolidation: pd.DataFrame, surcharges: pd.DataFrame, parameters: Dict, api_key: str) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
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

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: Two pandas DataFrames containing shipment analysis and transport analysis.
                                    Returns None if the process fails.
    """

    def convert_dates(df, date_columns):
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
        return df

    # Convert date columns to string format (YYYY-MM-DD)
    date_columns = ['shippingDate', 'expectedDeliveryDate', 'actualDeliveryDate']
    shipments = convert_dates(shipments, date_columns)

    def convert_to_string(df, string_columns):
        for col in string_columns:
            df[col] = df[col].astype(str)
        return df

    def convert_to_float(df, float_columns):
        for col in float_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def validate_boolean(value):
        return isinstance(value, bool)

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
    costAdjustment = convert_to_float(costAdjustment, ['factor', 'flatOnTop'])
    consolidation = convert_to_float(consolidation, ['capacityWeight', 'capacityVolume', 'capacityPallets'])
    surcharges = convert_to_float(surcharges, ['flatOnTop'])

    # Validate boolean parameter
    if 'consolidation' in parameters and not validate_boolean(parameters['consolidation']):
        logging.error("Invalid type for 'consolidation' in parameters. It should be boolean.")
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/shipmentanalyzerplus"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        "shipments": shipments.to_dict(orient='records'),
        "costAdjustment": costAdjustment.to_dict(orient='records'),
        "consolidation": consolidation.to_dict(orient='records'),
        "surcharges": surcharges.to_dict(orient='records'),
        "parameters": parameters
    }
    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                shipments_df = pd.DataFrame(response_data['shipments'])
                transports_df = pd.DataFrame(response_data['transports'])
                return shipments_df, transports_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in shipment analyzer API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None


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


def reverse_shipment_analyzer(shipments: pd.DataFrame, costAdjustment: pd.DataFrame, consolidation: pd.DataFrame, surcharges: pd.DataFrame, parameters: Dict, api_key: str) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
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

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: Two pandas DataFrames containing reverse shipment analysis and transport analysis.
                                      The first DataFrame ('shipments') includes details such as shipment IDs, locations, dates, shipment metrics, and calculated emissions and costs.
                                      The second DataFrame ('transports') includes aggregated transport metrics such as total weights, volumes, costs, and emissions for each transport ID.
                                      Returns None if the process fails.
    """

    # Conversion functions (similar to forward_shipment_analyzer)
    def convert_dates(df, date_columns):
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
        return df

    def convert_to_string(df, string_columns):
        for col in string_columns:
            df[col] = df[col].astype(str)
        return df

    def convert_to_float(df, float_columns):
        for col in float_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def validate_boolean(value):
        return isinstance(value, bool)

    # Convert data types according to the schema
    date_columns = ['shippingDate', 'expectedDeliveryDate', 'actualDeliveryDate']
    shipments = convert_dates(shipments, date_columns)

    string_columns = ['shipmentId', 'shipmentLeg', 'fromId', 'toId', 'shippingMode', 'carrier', 'truckShipPlaneType', 'speedProfile', 'benchmarkTariff', 'surcharges']
    shipments = convert_to_string(shipments, string_columns)

    float_columns = ['fromLatitude', 'fromLongitude', 'toLatitude', 'toLongitude', 'weight', 'volume', 'pallets', 'shipmentValue', 'freightCosts']
    shipments = convert_to_float(shipments, float_columns)

    # Convert and validate other dataframes as in forward_shipment_analyzer...

    # Validate boolean parameter
    if 'consolidation' in parameters and not validate_boolean(parameters['consolidation']):
        logging.error("Invalid type for 'consolidation' in parameters. It should be boolean.")
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reverseshipmentanalyzerplus"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        "shipments": shipments.to_dict(orient='records'),
        "costAdjustment": costAdjustment.to_dict(orient='records'),
        "consolidation": consolidation.to_dict(orient='records'),
        "surcharges": surcharges.to_dict(orient='records'),
        "parameters": parameters
    }

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                shipments_df = pd.DataFrame(response_data['shipments'])
                transports_df = pd.DataFrame(response_data['transports'])
                return shipments_df, transports_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in shipment analyzer API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

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
import os
import requests
import numpy as np
import pandas as pd
import time
import logging
from typing import Optional
import warnings

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
        for _, row in df.iterrows():
            record = {}
            for column, value in row.items():
                if pd.notna(value) or column not in columns_to_check:
                    record[column] = value
            records.append(record)
        return records

def forward_freight_matrix(shipments_df: pd.DataFrame, matrix_id: str, api_key: str) -> Optional[pd.DataFrame]:
    """
    Calculate the freight matrix for a list of shipments provided in a pandas DataFrame.

    Parameters:
    shipments_df (pd.DataFrame): A pandas DataFrame containing the shipment details. Each row represents a unique shipment, and the columns include:

    - shipmentId (str): A unique identifier for the shipment. 
    - shipmentDate (str): The scheduled date and time of the shipment in UTC, in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
    - fromLocationId (str): Identifier for the origin location.
    - fromCountry (str): ISO country code for the origin location.
    - fromState (str): State or region code for the origin location. 
    - fromCity (str): City name of the origin location. 
    - fromPostalCode (str): Postal code of the origin location. Increases address accuracy.
    - fromStreet (str): Street address of the origin location. Increases address accuracy.
    - fromZone (str): A logistics zone or area at the origin. Used for categorizing regions for shipping purposes, which can impact cost.
    - toLocationId (str): Identifier for the destination location. 
    - toCountry (str): ISO country code for the destination location. 
    - toState (str): State or region code for the destination location. 
    - toCity (str): City name of the destination location. 
    - toPostalCode (str): Postal code of the destination location. Increases address accuracy.
    - toStreet (str): Street address of the destination location. Increases address accuracy.
    - toZone (str): A logistics zone or area at the destination. Used to categorize regions for shipping purposes, impacting delivery strategies and costs.
    - distance (float): The total distance between the origin and destination locations in kilometers or miles. 
    - weight (float): The total weight of the shipment in kilograms or pounds. Make sure that it is aligned with the dimension that is used in the freight matrix.
    - volume (float): The total volume of the shipment in cubic meters or cubic feet. Make sure that it is aligned with the dimension that is used in the freight matrix.
    - pallets (int): The number of pallets used for the shipment. Make sure that it is aligned with the dimension that is used in the freight matrix.
    - loadingMeters (float): The total space in meters required by the shipment on the transport vehicle. Make sure that it is aligned with the dimension that is used in the freight matrix.

    matrix_id (str): The Freight Matrix ID from a matrix that was created on the Log-hub Platform.
    api_key (str): The Log-hub API key for accessing the freight matrix service.

    Returns:
    pd.DataFrame: A pandas DataFrame containing evaluated shipments with additional
                  details such as fromLatitude, fromLongitude, toLatitude, toLongitude, costs, etc.
                  Returns None if the process fails.
    """
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/freightmatrix"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    
    float_columns = ['distance', 'weight', 'volume', 'pallets', 'loadingMeters']
    for column in float_columns:
        if column in shipments_df.columns:
            shipments_df[column] = pd.to_numeric(shipments_df[column], errors='coerce')

    # Convert DataFrame to list of dicts for the payload, excluding NaN values in specified columns
    shipments_list = convert_df_to_dict_excluding_nan(shipments_df, float_columns)
    
    payload = {
        "shipments": shipments_list,
        "matrix": {"matrixId": matrix_id}
    }

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                evaluated_shipments = pd.DataFrame(response.json().get('evaluatedShipments', []))
                return evaluated_shipments
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in freight matrix API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
                
    logging.error("Max retries exceeded.")
    return None



def forward_freight_matrix_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'freightMatrixAddresses.xlsx')
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:U', dtype={'shipmentId': str, 'shipmentDate': str, 'fromLocationId': str, 'toLocationId': str, 'fromPostalCode': str, 'toPostalCode': str, 'distance': float, 'weight': float, 'volume': float, 'pallets': float, 'loadingMeters': float})
    return {'shipments': shipments_df}


def reverse_freight_matrix(shipments_df: pd.DataFrame, matrix_id: str, api_key: str) -> Optional[pd.DataFrame]:
    """
    Calculate the reverse freight matrix for a list of shipments provided in a pandas DataFrame.
    
    Parameters:
    shipments_df (pd.DataFrame): A pandas DataFrame containing the shipment details for reverse logistics. Each row represents a unique shipment, and the columns include:
        - shipmentId (str): A unique identifier for the shipment.
        - shipmentDate (str): The scheduled date and time of the shipment in UTC, in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
        - fromLocationId (str): Identifier for the origin location.
        - fromLatitude (float): Latitude of the origin location.
        - fromLongitude (float): Longitude of the origin location.
        - fromZone (str): A logistics zone or area at the origin, impacting shipping strategies and costs.
        - toLocationId (str): Identifier for the destination location.
        - toLatitude (float): Latitude of the destination location.
        - toLongitude (float): Longitude of the destination location.
        - toZone (str): A logistics zone or area at the destination, impacting delivery strategies and costs.
        - distance (float): The total distance between the origin and destination locations in kilometers or miles.
        - weight (float): The total weight of the shipment in kilograms or pounds, critical for cost calculations.
        - volume (float): The total volume of the shipment in cubic meters or cubic feet, affecting space utilization.
        - pallets (int): The number of pallets used for the shipment, influencing handling requirements.
        - loadingMeters (float): The total space required by the shipment on the transport vehicle, impacting vehicle utilization.

    matrix_id (str): The Freight Matrix ID from a matrix that was created on the Log-hub Platform.
    api_key (str): The Log-hub API key for accessing the reverse freight matrix service.

    Returns:
    pd.DataFrame: A pandas DataFrame containing evaluated shipments with additional
                  details such as costs, weight class, distance class, and price per unit. Returns None if the process fails.
    """
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversefreightmatrix"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    
    float_columns = ['distance', 'weight', 'volume', 'pallets', 'loadingMeters']
    for column in float_columns:
        if column in shipments_df.columns:
            shipments_df[column] = pd.to_numeric(shipments_df[column], errors='coerce')

    # Convert DataFrame to list of dicts for the payload, excluding NaN values in specified columns
    shipments_list = convert_df_to_dict_excluding_nan(shipments_df, float_columns)
    
    payload = {
        "shipments": shipments_list,
        "matrix": {"matrixId": matrix_id}
    }

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                evaluated_shipments = pd.DataFrame(response.json().get('evaluatedShipments', []))
                return evaluated_shipments
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in reverse freight matrix API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def reverse_freight_matrix_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'freightMatrixReverse.xlsx')
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:O', dtype={'shipmentId': str, 'shipmentDate': str, 'fromLocationId': str, 'toLocationId': str, 'weight': float, 'volume': float, 'pallets': float, 'loadingMeters': float})
    return {'shipments': shipments_df}
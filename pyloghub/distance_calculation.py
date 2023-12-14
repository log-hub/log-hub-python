import os
import requests
import pandas as pd
import time
import logging
from typing import Optional, Dict
import warnings

logging.basicConfig(level=logging.INFO)

def forward_distance_calculation(address_pairs: pd.DataFrame, parameters: Dict, api_key: str) -> Optional[pd.DataFrame]:
    """
    Calculate distances and durations between pairs of addresses.

    This function takes a DataFrame of address pairs (sender and recipient) and a set of parameters,
    along with an API key, and performs distance calculation using the Log-hub distance calculation service. 
    The function handles batching and rate limiting by the API.

    Parameters:
    address_pairs (pd.DataFrame): A pandas DataFrame containing pairs of addresses.
        Each row should contain:
        - senderCountry (str): Sender country code. Must have at least 1 character.
        - senderState (str): Sender state code.
        - senderPostalCode (str): Sender postal code.
        - senderCity (str): Sender city name.
        - senderStreet (str): Sender street name with house number.
        - recipientCountry (str): Recipient country code. Must have at least 1 character.
        - recipientState (str): Recipient state code.
        - recipientPostalCode (str): Recipient postal code.
        - recipientCity (str): Recipient city name.
        - recipientStreet (str): Recipient street name with house number.

    parameters (Dict): A dictionary containing parameters like distanceUnit (enum: "km" or "mi"),
                        durationUnit (enum: "min" or "sec" or "h"), and vehicleType (enum: "truck" or "car").

    api_key (str): The Log-hub API key for accessing the distance calculation service.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the results of the distance calculations. 
                  Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'senderCountry': 'str', 'senderState': 'str', 'senderPostalCode': 'str',
            'senderCity': 'str', 'senderStreet': 'str', 'recipientCountry': 'str',
            'recipientState': 'str', 'recipientPostalCode': 'str',
            'recipientCity': 'str', 'recipientStreet': 'str'
        }
        for col, dtype in required_columns.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except Exception as e:
                    logging.error(f"Data type conversion failed for column '{col}': {e}")
                    return None
            else:
                logging.error(f"Missing required column: {col}")
                return None
        return df

    # Validate and convert data types
    address_pairs = validate_and_convert_data_types(address_pairs)
    if address_pairs is None:
        return None

    url = "https://production.supply-chain-apps.log-hub.com/api/applications/v1/distancecalculation"
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    batch_size = 5000
    max_retries = 3

    def process_batch(batch):
        """
        Process a batch of address pairs for distance calculation.

        This function sends a batch of address pairs along with parameters to the distance calculation
        API and handles potential rate limiting by implementing retries with a delay.

        Parameters:
        batch (dict): A batch of address pairs and parameters in the required JSON format for the API.

        Returns:
        requests.Response: The response from the Log-hub distance calculation API.
        """
        for attempt in range(max_retries):
            try:
                response = requests.post(url, json=batch, headers=headers)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 10))
                    logging.info(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)
                else:
                    logging.error(f"Error in distance calculation API: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(10)  # Fallback in case of request failure
        return None

    results = []
    for start in range(0, len(address_pairs), batch_size):
        end = start + batch_size
        batch = address_pairs.iloc[start:end].to_dict(orient='records')
        response = process_batch({"addresses": batch, "parameters": parameters})
        if response:
            response_data = response.json()
            if isinstance(response_data, list):
                results.extend(response_data)
            else:
                logging.error("Unexpected response format from the API.")
        else:
            logging.error(f"Failed to process batch {start}-{end} after multiple retries.")

    return pd.DataFrame(results)


def forward_distance_calculation_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'DistanceCalcSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:J')

    parameters = {
        "distanceUnit": "km",
        "durationUnit": "min",
        "vehicleType": "car"
    }
    return {'address_data': addresses_df, 'parameters': parameters}



def reverse_distance_calculation(geocodes: pd.DataFrame, parameters: Dict, api_key: str) -> Optional[pd.DataFrame]:
    """
    Calculate distances and durations between pairs of locations based on coordinates.

    This function takes a DataFrame of geocode pairs (sender and recipient) with their locations and coordinates,
    a set of parameters, along with an API key, and performs reverse distance calculation using the 
    Log-hub reverse distance calculation service. The function handles batching and rate limiting by the API.

    Parameters:
    geocodes (pd.DataFrame): A pandas DataFrame containing pairs of geocodes with sender and recipient information.
        Each row should contain:
        - senderLocation (str): Sender location. Must have at least 1 character.
        - senderLatitude (float): Sender latitude.
        - senderLongitude (float): Sender longitude.
        - recipientLocation (str): Recipient location. Must have at least 1 character.
        - recipientLatitude (float): Recipient latitude.
        - recipientLongitude (float): Recipient longitude.

    parameters (Dict): A dictionary containing parameters like distanceUnit (enum: "km" or "mi"),
                        durationUnit (enum: "min" or "sec" or "h"), and vehicleType (enum: "truck" or "car").

    api_key (str): The Log-hub API key for accessing the reverse distance calculation service.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the results of the reverse distance calculations.
                  Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'senderLocation': 'str', 'senderLatitude': 'float', 'senderLongitude': 'float',
            'recipientLocation': 'str', 'recipientLatitude': 'float', 'recipientLongitude': 'float'
        }
        for col, dtype in required_columns.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
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


    url = "https://production.supply-chain-apps.log-hub.com/api/applications/v1/reversedistancecalculation"
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    batch_size = 5000
    max_retries = 3

    def process_batch(batch):
        for attempt in range(max_retries):
            try:
                response = requests.post(url, json=batch, headers=headers)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 15))
                    logging.info(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)
                else:
                    logging.error(f"Error in reverse distance calculation API: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(10)
        return None

    results = []
    for start in range(0, len(geocodes), batch_size):
        end = start + batch_size
        batch = geocodes.iloc[start:end].to_dict(orient='records')
        response = process_batch({"geocodes": batch, "parameters": parameters})
        if response:
            response_data = response.json()
            if isinstance(response_data, list):
                results.extend(response_data)
            else:
                logging.error("Unexpected response format from the API.")
        else:
            logging.error(f"Failed to process batch {start}-{end} after multiple retries.")

    return pd.DataFrame(results)


def reverse_distance_calculation_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'DistanceCalcSampleDataReverse.xlsx')
    geocode_data_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:F')

    parameters = {
        "distanceUnit": "km",
        "durationUnit": "min",
        "vehicleType": "car"
    }
    return {'geocode_data': geocode_data_df, 'parameters': parameters}
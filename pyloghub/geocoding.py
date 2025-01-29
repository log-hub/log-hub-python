import os
import requests
import pandas as pd
import time
import logging
from typing import Optional
import warnings
logging.basicConfig(level=logging.INFO)


def forward_geocoding(addresses: pd.DataFrame, api_key: str) -> Optional[pd.DataFrame]:
    """
    Perform forward geocoding on a list of addresses.

    This function takes a DataFrame of addresses and an API key, and performs forward
    geocoding using the Log-hub geocoding service. The function handles batching and 
    rate limiting by the API.

    Parameters:
    addresses (pd.DataFrame): A pandas DataFrame containing the addresses to be geocoded.
        Required columns and their types:
        - country (str): Country code. Must have at least 1 character.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - searchString (str): Key location details. Information such as country, state, city, street, and zip code, although the zip code cannot be the first entry.

    api_key (str): The Log-hub API key for accessing the geocoding service.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the original address information along 
                  with the geocoded results. Includes latitude and longitude for each address.
                  Returns None if the process fails.
    """
    
    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        string_columns = ['country', 'state', 'postalCode', 'city', 'street', 'searchString']
        for col in string_columns:
            if col in df.columns:
                try:
                    df[col] = df[col].astype(str)
                except Exception as e:
                    logging.error(f"Data type conversion failed for column '{col}': {e}")
                    return None
            else:
                logging.error(f"Missing required column: {col}")
                return None
        return df

    # Validate and convert data types
    addresses = validate_and_convert_data_types(addresses)
    if addresses is None:
        return None

    addresses = addresses.fillna("")
    
    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/geocoding"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    batch_size = 5000
    max_retries = 3

    def process_batch(batch):
        """
        Process a batch of addresses for geocoding.

        This function sends a batch of addresses to the geocoding API and handles
        potential rate limiting by implementing retries with a delay.

        Parameters:
        batch (dict): A batch of addresses in the required JSON format for the API.

        Returns:
        requests.Response: The response from the Log-hub geocoding API.
        """
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
                    logging.error(f"Error in geocoding API: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(10)  # Fallback in case of request failure
        return None

    results = []
    for start in range(0, len(addresses), batch_size):
        end = start + batch_size
        batch = addresses.iloc[start:end].to_dict(orient='records')
        response = process_batch({"addresses": batch})
        if response:
            results.extend(response.json().get("geocodes", []))
        else:
            logging.error(f"Failed to process batch {start}-{end} after multiple retries.")

    return pd.DataFrame(results)


def forward_geocoding_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'GeocodingSampleDataAddresses.xlsx')
    addresses_df = pd.read_excel(data_path, sheet_name='addresses', usecols='A:F').fillna("")
    return {'addresses': addresses_df}


def reverse_geocoding(geocodes: pd.DataFrame, api_key: str) -> Optional[pd.DataFrame]:
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
    batch_size = 5000
    max_retries = 3

    def process_batch(batch):
        """
        Process a batch of geocodes for reverse geocoding.

        This function sends a batch of geocodes to the reverse geocoding API and handles
        potential rate limiting by implementing retries with a delay.

        Parameters:
        batch (dict): A batch of geocodes in the required JSON format for the API.

        Returns:
        requests.Response: The response from the Log-hub reverse geocoding API.
        """
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
                    logging.error(f"Error in reverse geocoding API: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(10)  # Fallback in case of request failure
        return None

    results = []
    for start in range(0, len(geocodes), batch_size):
        end = start + batch_size
        batch = geocodes.iloc[start:end].to_dict(orient='records')
        response = process_batch({"geocodes": batch})
        if response:
            results.extend(response.json().get("addresses", []))
        else:
            logging.error(f"Failed to process batch {start}-{end} after multiple retries.")

    return pd.DataFrame(results)


def reverse_geocoding_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'GeocodingSampleDataReverse.xlsx')
    geocodes_df = pd.read_excel(data_path, sheet_name='coordinates', usecols='A:B')
    return {'geocodes': geocodes_df}
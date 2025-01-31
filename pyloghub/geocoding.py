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

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json={'addresses': addresses.to_dict(orient='records')}, headers=headers)
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

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json={"geocodes": geocodes.to_dict(orient='records')}, headers=headers)
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
    return {'geocodes': geocodes_df}

if __name__ == "__main__":

    api_key = "14d872084c972dd5087bee9b6fa1593a5061a2e7"

    sample_for = forward_geocoding_sample_data()
    out_for = forward_geocoding(sample_for['addresses'],api_key)

    sample_rev = reverse_geocoding_sample_data()
    out_rev = reverse_geocoding(sample_rev['geocodes'], api_key)

    
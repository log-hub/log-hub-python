import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple
from save_to_platform import save_scenario_check, get_app_name

def reverse_supply_chain_map_polyline(polyline: pd.DataFrame, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a polyline on the map.

    This function takes a DataFrame of polyline with its latitude and longitude pairs and layer, along with an API key, 
    and creates a polyline using the Log-hub Supply Chain Map service. 

    Parameters:
    coordinates (pd.DataFrame): A pandas DataFrame containing coordinates with their layer, quantity and descriptions.
        Each row should contain:
        - id (number): Identifier.
        - polyline (str): Polyline name.
        - latitude (number): Latitude of the polyline.
        - longitude (number): Longitude of the polyline.
        - layer (str): Layer that polyline is going to be assigned to.
        

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the polylines. Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'polyline': 'str', 'latitude':'float', 'longitude': 'float', 'layer': 'str'
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
    polyline = validate_and_convert_data_types(polyline)
    if polyline is None:
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversesupplychainmappolyline"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "polylineData": polyline.to_dict(orient='records'),
    }
    app_name = get_app_name(url)
    payload = save_scenario_check(save_scenario, payload, app_name)
    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                polyline_result_df = pd.DataFrame(response_data['polylineData'])
                return polyline_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in supply chain map polylines API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def reverse_supply_chain_map_polyline_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapPolyline.xlsx')
    polyline_df = pd.read_excel(data_path, sheet_name='polyline', usecols='A:E')

    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        "mergeWithExistingScenario": False,
        'scenarioName': 'Your scenario name'
    }
    return {'polyline': polyline_df, 'saveScenarioParameters': save_scenario}

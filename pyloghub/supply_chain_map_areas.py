import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple
from pyloghub.save_to_platform import save_scenario_check, get_app_name

def forward_supply_chain_map_areas(areas: pd.DataFrame, parameters: dict, api_key: str, save_scenario = {}) -> Optional[pd.DataFrame]:
    """
    Creates a map of areas based on the given area information.

    This function takes a DataFrame of areas with their country, region and center latitude and longitude, along with an API key, 
    and creates a map of areas using the Log-hub Supply Chain Map service. 

    Parameters:
    areas (pd.DataFrame): A pandas DataFrame containing areas information.
        Each row should contain:
        - id (number): Identifier.
        - searchId (str): Area search id.
        - country (str):  Country name or country code of the area.
        - region (str): Region name.
        - name (str): Area name.
        - layer (str): Layer name for the area.
        - quantity (number): Numerical value that can be used to determine the color of an area on the map.
        - continent (str): Country and area continent.
        - countryRegionOne, countryRegionTwo (str): Continent's subregion and second subregion where country is located.
        - countryName (str): Country name.
        - centerLat, centerLong (number): Area's center point latitude and longitude.
        - population (number): Area population.
        - areaKm2 (number): Area in km2

    parameters (dict): A dictionary containg parameter 'detailLevel' (boolean). 

    api_key (str): The Log-hub API key for accessing the center of gravity plus service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the passed area information and its length [km]. Returns None if the process fails.
    """

    def validate_and_convert_data_types(df):
        """
        Validate and convert the data types of the DataFrame columns.
        Log an error message if a required column is missing or if conversion fails.
        """
        required_columns = {
            'id': 'float', 'searchId': 'str', 'country': 'str', 'region': 'str', 'name': 'str', 'layer': 'str', 'quantity': 'float', 'continent': 'str', 'countryRegionOne': 'str', 'countryRegionTwo': 'str', 'countryName': 'str', 'centerLat': 'float', 'centerLong': 'float', 'population': 'float', 'areaKm2': 'float'
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
    areas = validate_and_convert_data_types(areas)
    if areas is None:
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/supplychainmapareas"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }
    payload = {
        "areaData": areas.to_dict(orient='records'),
        "parameters": parameters
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
                area_result_df = pd.DataFrame(response_data['areaResult'])
                return area_result_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in supply chain map areas API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_supply_chain_map_areas_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MapAreas.xlsx')
    areas_df = pd.read_excel(data_path, sheet_name='areas', usecols='A:O')

    parameters={
        'detailLevel': False
    }
    save_scenario = {
        'saveScenario': True,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'mergeWithExistingScenario': False,
        'scenarioName': 'Your scenario name'
    }

    return {'areas': areas_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

import os
import pandas as pd
import warnings
from typing import Optional
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url

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

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the passed area information and its length [km]. Returns None if the process fails.
    """

    required_columns = {
            'id': 'float', 'searchId': 'str', 'country': 'str', 'region': 'str', 'name': 'str', 'layer': 'str', 'quantity': 'float', 'continent': 'str', 'countryRegionOne': 'str', 'countryRegionTwo': 'str', 'countryName': 'str', 'centerLat': 'float', 'centerLong': 'float', 'population': 'float', 'areaKm2': 'float'
        }

    # Validate and convert data types
    areas = validate_and_convert_data_types(areas, required_columns)
    if areas is None:
        return None

    url = create_url("supplychainmapareas")
    
    headers = create_headers(api_key)
    payload = {
        "areaData": areas.to_dict(orient='records'),
        "parameters": parameters
    }
    
    payload = save_scenario_check(save_scenario, payload, "supplychainmapareas")
    
    response_data = post_method(url, payload, headers, "supply chain map areas")
    if response_data is None:
        return None
    else:
        areas_df = pd.DataFrame(response_data['areaResult'])
        return areas_df

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
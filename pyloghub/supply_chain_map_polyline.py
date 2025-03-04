import os
import pandas as pd
import warnings
from typing import Optional
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url

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
        

    api_key (str): The Log-hub API key for accessing the supply chain map service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'mergeWithExistingScenario (boolean), 'workspaceId' (str) and 'scenarioName' (str).

    Returns:
    pd.DataFrame: A pandas DataFrame containg the polylines. Returns None if the process fails.
    """

    mandatory_columns = {
            'polyline': 'str', 'latitude':'float', 'longitude': 'float'
        }
    optional_columns = {'id': 'float', 'layer': 'str'}

    # Validate and convert data types
    polyline = validate_and_convert_data_types(polyline, mandatory_columns, 'mandatory')
    if not polyline is None:
        polyline = validate_and_convert_data_types(polyline, optional_columns, 'optional')
    if polyline is None:
        return None

    url = create_url("reversesupplychainmappolyline")
    
    headers = create_headers(api_key)
    payload = {
        "polylineData": polyline.to_dict(orient='records'),
    }
    
    payload = save_scenario_check(save_scenario, payload, "reversesupplychainmappolyline")
    
    response_data = post_method(url, payload, headers, "supplychain map polyline")
    if response_data is None:
        return None
    else:
        polyline_df = pd.DataFrame(response_data['polylineData'])
        return polyline_df


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

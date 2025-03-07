import os
import pandas as pd
from typing import Optional
import warnings
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import convert_df_to_dict_excluding_nan, convert_to_float, validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url

def forward_freight_matrix_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'freightMatrixAddresses.xlsx')
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:U', dtype={'shipmentId': str, 'shipmentDate': str, 'fromLocationId': str, 'toLocationId': str, 'fromPostalCode': str, 'toPostalCode': str, 'distance': str, 'weight': float, 'volume': float, 'pallets': float, 'loadingMeters': float})

    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'shipments': shipments_df, 'saveScenarioParameters': save_scenario}
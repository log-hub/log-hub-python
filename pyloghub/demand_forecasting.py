import os
import pandas as pd
import warnings
from typing import Optional
import logging
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types, convert_dates
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def demand_forecasting(past_demand_data: pd.DataFrame, future_impact_factors: pd.DataFrame, sku_parameters: pd.DataFrame, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[pd.DataFrame]:
    """
    Perform demand forecasting based on past demand data, future impact factors and sku parameters.
    Parameters:
    past_demand_data (pd.DataFrame): DataFrame containing the historical demand information for each SKU.
        Columns:
        - sku (str): Unique identifier for each SKU.
        - date (str): A timestamp of each demand observation.
        - demand (number): Past demand value for the SKU on the specified date.
        - [futureImpactFactor1, futureImpactFactor2, futureImpactFactor3] (str): Custom columns representing external factors that may affect demand. There can be more than three columns, depending on the number of known external factors. Supported data types are Binary Indicators (0 or 1 values indicating the absence or presence of an event e.g., promotion) and Continuous Variables (numeric values representing the intensity of an impact factor e.g., promotional spend).

    future_impact_factors (pd.DataFrame): DataFrame providing future values for the impact factors (external regressors) defined in the past_demand_data.
        Columns:
        - sku (str): Unique identifier for each SKU.
        - date (str): A timestamp of each demand observation.
        - [futureImpactFactor1, futureImpactFactor2, futureImpactFactor3] (str): Custom columns representing external factors that may affect demand. There can be more than three columns, depending on the number of known external factors. Supported data types are Binary Indicators (0 or 1 values indicating the absence or presence of an event e.g., promotion) and Continuous Variables (numeric values representing the intensity of an impact factor e.g., promotional spend).

    sku_parameters (pd.DataFrame): DataFrame containing SKU-specific parameters that customize the forecasting model for each product.
        Columns:
        - sku (str): Unique identifier for each SKU.
        - forecastPeriods (number): Defining how many periods into the future should be forecasted. Each period is one day.
        - demandFrequency (str): Showing if the demand is daily, weekly, monthly or yearly.
        - lowerTrendLimit (str): A minimum expected demand level.
        - upperTrendLimit (str): A maximum expected demand level.
        - seasonality (str): Defining a seasonality pattern. Allowed entries are weekly, monthly or yearly.
        - seasonalityType (str): Specifying how seasonal components interact with the trend. Allowed values are 'additive' and 'multiplicative'
        - confidenceInterval (str): determining the level of certanty that the demand will fall within a specific range.
        - [futureImpactFactor1, futureImpactFactor2, futureImpactFactor3] (str): Custom columns representing external factors that may affect demand. There can be more than three columns, depending on the number of known external factors. Supported data types are Binary Indicators (0 or 1 values indicating the absence or presence of an event e.g., promotion) and Continuous Variables (numeric values representing the intensity of an impact factor e.g., promotional spend).

    api_key (str): Log-hub API key for accessing the demand forecasting service.
    
    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                            'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                            'scenarioName' (str).
    
    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    pd.DataFrame: A DataFrame containing demands prediction. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    # Define expected columns and data types for each DataFrame
    past_demand_data_mandatory_columns = {'sku': 'str', 'date': 'str', 'demand': 'float'}
    past_demand_data_optional_columns = {'futureImpactFactor1': 'str', 'futureImpactFactor2': 'str', 'futureImpactFactor3': 'str'}
    future_impact_factors_optional_columns = {'sku': 'str', 'date': 'str', 'futureImpactFactor1': 'str', 'futureImpactFactor2': 'str', 'futureImpactFactor3': 'str'}
    sku_parameters_mandatory_columns = {'sku': 'str', 'forecastPeriods': 'float'}
    sku_parameters_optional_columns = {'demandFrequency': 'str', 'lowerTrendLimit':'str', 'upperTrendLimit': 'str', 'seasonality': 'str', 'seasonalityType': 'str', 'confidenceInterval': 'str', 'futureImpactFactor1': 'str', 'futureImpactFactor2': 'str', 'futureImpactFactor3': 'str'}

    # Perform validation and conversion for each DataFrame
    past_demand_data = validate_and_convert_data_types(past_demand_data, past_demand_data_mandatory_columns, 'mandatory', 'past demand data')
    if not past_demand_data is None:
        past_demand_data = validate_and_convert_data_types(past_demand_data, past_demand_data_optional_columns, 'optional', 'past demand data')
    future_impact_factors = validate_and_convert_data_types(future_impact_factors, future_impact_factors_optional_columns, 'optional', 'future impact factors')
    sku_parameters = validate_and_convert_data_types(sku_parameters, sku_parameters_mandatory_columns, 'mandatory''future impact factors')
    if not sku_parameters is None:
        sku_parameters = validate_and_convert_data_types(sku_parameters, sku_parameters_optional_columns, 'optional', 'sku parameters')
    if not any(df is None for df in [past_demand_data, future_impact_factors]):
        past_demand_data = convert_dates(past_demand_data, ['date'])
        if 'date' in future_impact_factors.columns:
            future_impact_factors = convert_dates(future_impact_factors, ['date'])

    # Exit if any DataFrame validation failed
    if any(df is None for df in [past_demand_data, future_impact_factors, sku_parameters]):
        return None

    url = create_url("demandforecasting")
    
    headers = create_headers(api_key)

    payload = {
        "pastDemandData": past_demand_data.to_dict(orient='records'),
        "futureImpactFactors": future_impact_factors.to_dict(orient='records'),
        "skuParameters": sku_parameters.to_dict(orient='records'),
    }

    payload = save_scenario_check(save_scenario, payload)
    
    response_data = post_method(url, payload, headers, "demand forecasting")
    if response_data is None:
        return None
    else:
        prediction_df = pd.DataFrame(response_data['prediction'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return prediction_df
            

def demand_forecasting_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'demandForecasting.xlsx')
    past_demand_data_df = pd.read_excel(data_path, sheet_name='pastDemandData', usecols='A:G').fillna("")
    future_impact_factors_df = pd.read_excel(data_path, sheet_name='futureImpactFactors', usecols='A:F').fillna("")
    sku_parameters_df = pd.read_excel(data_path, sheet_name='skuParameters', usecols='A:L').fillna("")

    return {'pastDemandData': past_demand_data_df, 'futureImpactFactors': future_impact_factors_df, 'skuParameters': sku_parameters_df}

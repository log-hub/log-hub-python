import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional

def convert_dates(df, date_columns):
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
        return df
    
def validate_and_convert_data_types(df, required_columns):
    """
    Validate and convert the data types of the DataFrame columns.
    Log an error message if a required column is missing or if conversion fails.
    """
    for col, dtype in required_columns.items():
        if col not in df.columns:
            logging.error(f"Missing required column: {col}")
            return None
        try:
            df[col] = df[col].astype(dtype)
        except Exception as e:
            logging.error(f"Data type conversion failed for column '{col}': {e}")
            return None
    return df

def demand_forecasting(past_demand_data: pd.DataFrame, future_impact_factors: pd.DataFrame, sku_parameters: pd.DataFrame, api_key: str) -> Optional[pd.DataFrame]:
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

    Returns:
    pd.DataFrame: A DataFrame containing demands prediction. Returns None if the process fails.
    """
    # Define expected columns and data types for each DataFrame
    past_demand_data_columns = {
        'sku': 'str', 'date': 'str', 'demand': 'float', 'futureImpactFactor1': 'str', 'futureImpactFactor2': 'str', 'futureImpactFactor3': 'str'
    }
    future_impact_factors_columns = {
        'sku': 'str', 'date': 'str', 'futureImpactFactor1': 'str', 'futureImpactFactor2': 'str', 'futureImpactFactor3': 'str'
    }
    sku_parameters_columns = {
        'sku': 'str', 'forecastPeriods': 'float', 'demandFrequency': 'str', 'lowerTrendLimit':'str', 'upperTrendLimit': 'str', 'seasonality': 'str', 'seasonalityType': 'str', 'confidenceInterval': 'str', 'futureImpactFactor1': 'str', 'futureImpactFactor2': 'str', 'futureImpactFactor3': 'str'
    }

    # Perform validation and conversion for each DataFrame
    past_demand_data = validate_and_convert_data_types(past_demand_data, past_demand_data_columns)
    future_impact_factors = validate_and_convert_data_types(future_impact_factors, future_impact_factors_columns)
    sku_parameters = validate_and_convert_data_types(sku_parameters, sku_parameters_columns)
    past_demand_data = convert_dates(past_demand_data, ['date'])
    future_impact_factors = convert_dates(future_impact_factors, ['date'])

    # Exit if any DataFrame validation failed
    if any(df is None for df in [past_demand_data, future_impact_factors, sku_parameters]):
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net/"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/demandforecasting"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        "pastDemandData": past_demand_data.to_dict(orient='records'),
        "futureImpactFactors": future_impact_factors.to_dict(orient='records'),
        "skuParameters": sku_parameters.to_dict(orient='records'),
    }
    
    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                prediction_df = pd.DataFrame(response_data['prediction'])
                return prediction_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in demand forecasting API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def demand_forecasting_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'demandForecasting.xlsx')
    past_demand_data_df = pd.read_excel(data_path, sheet_name='pastDemandData', usecols='A:G').fillna("")
    future_impact_factors_df = pd.read_excel(data_path, sheet_name='futureImpactFactors', usecols='A:F').fillna("")
    sku_parameters_df = pd.read_excel(data_path, sheet_name='skuParameters', usecols='A:L').fillna("")

    return {'pastDemandData': past_demand_data_df, 'futureImpactFactors': future_impact_factors_df, 'skuParameters': sku_parameters_df}


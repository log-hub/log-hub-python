import os
import requests
import pandas as pd
import time
import logging
import warnings
from typing import Optional, Dict, Tuple

def forward_transport_optimization_plus(vehicles: pd.DataFrame, jobs: pd.DataFrame, timeWindowProfiles: pd.DataFrame, breaks: pd.DataFrame, parameters: Dict, api_key: str) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Perform transport optimization based on vehicles, jobs, time window profiles, and breaks.

    Parameters:
    vehicles (pd.DataFrame): DataFrame containing vehicle information.
        Columns:
        - vehicleTypeId (str): Vehicle Type Id.
        - availableVehicles (int): Available Vehicles.
        - [startId, endId] (str): Start and End Ids.
        - [startCountry, endCountry] (str): Start and End Country.
        - [startState, endState] (str): Start and End State.
        - [startPostalCode, endPostalCode] (str): Start and End Postal Codes.
        - [startCity, endCity] (str): Start and End City.
        - [startStreet, endStreet] (str): Start and End Street.
        - maxWeight (float): Maximum Weight.
        - maxVolume (float): Maximum Volume.
        - maxPallets (int): Maximum Pallets.
        - maxStops (int): Maximum Stops.
        - timeWindowStart, timeWindowEnd (str): Time Window Start and End (ISO 8601 format).
        - profile (str): Profile.
        - speedFactor (float): Speed Factor.
        - fixed, perHour, perKilometer, costPerStop (float): Fixed and Costs Per Hour, Kilometer and Stop.
        - minimumTravelTime, maxTravelTime (float): Minimum and Maximum Travel Time.
        - max_distance (float): Maximum number of kilometers that vehicle can drive per route.
        - maximumDistanceBetweenStops (float): Maximum number of kilometers that vehicle can drive between each stop.
        - breakId (str): Break Id.

    jobs (pd.DataFrame): DataFrame containing job information.
        Columns:
        - shipmentId (str): Shipment Id.
        - [fromName, toName] (str): From and To Names.
        - [fromCountry, toCountry] (str): From and To Countries.
        - [fromState, toState] (str): From and To States.
        - [fromPostalCode, toPostalCode] (str): From and To Postal Codes.
        - [fromCity, toCity] (str): From and To Cities.
        - [fromStreet, toStreet] (str): From and To Streets.
        - [senderStopDuration, recipientStopDuration] (float): Sender and Recipient Stop Durations.
        - [senderTimeWindowProfile, recipientTimeWindowProfile] (str): Sender and Recipient Time Window Profiles.
        - weight, volume (float): Weight and Volume.
        - pallets (int): Pallets.
        - vehicleTypeId (str): Vehicle Type Id.
        - external_costs (number): External costs for order.

    timeWindowProfiles (pd.DataFrame): DataFrame containing time window profile information.
        Columns:
        - timeWindowProfileId (str): Time Window Profile Id.
        - timeWindowProfileStart, timeWindowProfileEnd (str): Time Window Profile Start and End (ISO 8601 format).

    breaks (pd.DataFrame): DataFrame containing break information.
        Columns:
        - breakId (str): Break Id.
        - earliestBreakStart, latestBreakStart (str): Earliest and Latest Break Start (ISO 8601 format).
        - earliestRelativeBreakStart, latestRelativeBreakStart (str): Earliest and Latest Relative Break Start (ISO 8601 format).
        - breakDuration (float): Break Duration.

    parameters (Dict): Dictionary containing parameters like durationUnit and distanceUnit.
    api_key (str): Log-hub API key for accessing the transport optimization service.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Three pandas DataFrames containing route overview, route details, 
                                                     and external orders. Returns None if the process fails.
    """

    def convert_timestamps(df):
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return df

    # Convert datetime columns in each DataFrame to string format (ISO 8601)
    vehicles = convert_timestamps(vehicles)
    jobs = convert_timestamps(jobs)
    timeWindowProfiles = convert_timestamps(timeWindowProfiles)
    breaks = convert_timestamps(breaks)

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

    # Define expected columns and data types for each DataFrame
    vehicle_columns = {
        'vehicleTypeId': 'str', 'availableVehicles': 'int', 'startId': 'str', 
        'startCountry': 'str', 'startState': 'str', 'startPostalCode': 'str', 
        'startCity': 'str', 'startStreet': 'str', 'endId': 'str', 
        'endCountry': 'str', 'endState': 'str', 'endPostalCode': 'str', 
        'endCity': 'str', 'endStreet': 'str', 'maxWeight': 'float', 
        'maxVolume': 'float', 'maxPallets': 'int', 'maxStops': 'int', 
        'timeWindowStart': 'str', 'timeWindowEnd': 'str', 'profile': 'str', 
        'speedFactor': 'float', 'fixed': 'float', 'perHour': 'float', 'perKilometer': 'float', 'costPerStop': 'float', 'minimumTravelTime': 'float', 'maxTravelTime': 'float', 'max_distance': 'float', 'maximumDistanceBetweenStops': 'float', 'breakId': 'str'
    }
    job_columns = {
        'shipmentId': 'str', 'fromName': 'str', 'fromCountry': 'str', 
        'fromState': 'str', 'fromPostalCode': 'str', 'fromCity': 'str', 
        'fromStreet': 'str', 'senderStopDuration': 'float', 
        'senderTimeWindowProfile': 'str', 'toName': 'str', 'toCountry': 'str', 
        'toState': 'str', 'toPostalCode': 'str', 'toCity': 'str', 
        'toStreet': 'str', 'recipientStopDuration': 'float', 
        'recipientTimeWindowProfile': 'str', 'weight': 'float', 
        'volume': 'float', 'pallets': 'int', 'vehicleTypeId': 'str', 'external_costs': 'float'
    }
    timeWindowProfile_columns = {
        'timeWindowProfileId': 'str', 'timeWindowProfileStart': 'str', 
        'timeWindowProfileEnd': 'str'
    }
    break_columns = {
        'breakId': 'str', 'earliestBreakStart': 'str', 'latestBreakStart': 'str', 'earliestRelativeBreakStart': 'str', 'latestRelativeBreakStart': 'str', 'breakDuration': 'float'
    }

    # Perform validation and conversion for each DataFrame
    vehicles = validate_and_convert_data_types(vehicles, vehicle_columns)
    jobs = validate_and_convert_data_types(jobs, job_columns)
    timeWindowProfiles = validate_and_convert_data_types(timeWindowProfiles, timeWindowProfile_columns)
    breaks = validate_and_convert_data_types(breaks, break_columns)

    # Exit if any DataFrame validation failed
    if any(df is None for df in [vehicles, jobs, timeWindowProfiles, breaks]):
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/transportoptimizationplus"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        "vehicles": vehicles.to_dict(orient='records'),
        "jobs": jobs.to_dict(orient='records'),
        "timeWindowProfiles": timeWindowProfiles.to_dict(orient='records'),
        "breaks": breaks.to_dict(orient='records'),
        "parameters": parameters
    }
    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                route_overview_df = pd.DataFrame(response_data['routeOverview'])
                route_details_df = pd.DataFrame(response_data['routeDetails'])
                external_orders_df = pd.DataFrame(response_data['externalOrders'])
                return route_overview_df, route_details_df, external_orders_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in transport optimization API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def forward_transport_optimization_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'transportPlusAddresses.xlsx')
    vehicles_df = pd.read_excel(data_path, sheet_name='vehicles', usecols='A:AF', dtype={'startState': str, 'startPostalCode': str, 'endState': str, 'endPostalCode': str, 'maxTravelTime': int}).fillna("")
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:W').fillna("")
    time_window_profiles_df = pd.read_excel(data_path, sheet_name='timeWindowProfile', usecols='A:D').fillna("")
    breaks_df = pd.read_excel(data_path, sheet_name='breaks', usecols='A:G').fillna("")

    parameters = {
        "durationUnit": "min",
        "distanceUnit": "km"
    }
    return {'vehicles': vehicles_df, 'shipments': shipments_df, 'timeWindowProfiles': time_window_profiles_df, 'breaks': breaks_df, 'parameters': parameters}


def reverse_transport_optimization_plus(vehicles: pd.DataFrame, jobs: pd.DataFrame, timeWindowProfiles: pd.DataFrame, breaks: pd.DataFrame, parameters: Dict, api_key: str) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Perform reverse transport optimization based on vehicles, jobs, time window profiles, and breaks.

    Parameters:
    vehicles (pd.DataFrame): DataFrame containing vehicle information with latitude and longitude.
        Columns:
        - vehicleTypeId (str): Vehicle Type Id.
        - availableVehicles (int): Number of available vehicles.
        - [startId, endId] (str): Start and End Ids.
        - [startLatitude, endLatitude] (float): Start and End Latitude.
        - [startLongitude, endLongitude] (float): Start and End Longitude.
        - maxWeight (float): Maximum Weight.
        - maxVolume (float): Maximum Volume.
        - maxPallets (int): Maximum Pallets.
        - maxStops (int): Maximum Stops.
        - timeWindowStart, timeWindowEnd (str): Time Window Start and End (ISO 8601 format).
        - profile (str): Profile.
        - speedFactor (float): Speed Factor.
        - fixed, perHour, perKilometer, costPerStop (float): Fixed and Costs Per Hour, Kilometer and Stop.
        - minimumTravelTime, maxTravelTime (float): Minimum and Maximum Travel Time.
        - max_distance (float): Maximum number of kilometers that vehicle can drive per route.
        - maximumDistanceBetweenStops (float): Maximum number of kilometers that vehicle can drive between each stop.
        - breakId (str): Break Id.

    jobs (pd.DataFrame): DataFrame containing job information with latitude and longitude.
        Columns:
        - shipmentId (str): Shipment Id.
        - [fromName, toName] (str): From and To Names.
        - [fromLatitude, toLatitude] (float): From and To Latitude.
        - [fromLongitude, toLongitude] (float): From and To Longitude.
        - [senderStopDuration, recipientStopDuration] (float): Sender and Recipient Stop Durations.
        - [senderTimeWindowProfile, recipientTimeWindowProfile] (str): Sender and Recipient Time Window Profiles.
        - weight, volume (float): Weight and Volume.
        - pallets (int): Pallets.
        - vehicleTypeId (str): Vehicle Type Id.
        - external_costs (number): External costs for order.

    timeWindowProfiles (pd.DataFrame): DataFrame containing time window profile information.
        Columns:
        - timeWindowProfileId (str): Time Window Profile Id.
        - timeWindowProfileStart, timeWindowProfileEnd (str): Time Window Profile Start and End (ISO 8601 format).

    breaks (pd.DataFrame): DataFrame containing break information.
        Columns:
        - breakId (str): Break Id.
        - earliestBreakStart, latestBreakStart (str): Earliest and Latest Break Start (ISO 8601 format).
        - earliestRelativeBreakStart (str): Minimum driving time before the break can start (ISO 8601 format).
        - latestRelativeBreakTime (str): Maximum driving time until the break must start (ISO 8601 format).
        - breakDuration (float): Break Duration.

    parameters (Dict): Dictionary containing parameters like durationUnit and distanceUnit.
    api_key (str): Log-hub API key for accessing the reverse transport optimization service.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Three pandas DataFrames containing route overview, route details, 
                                                     and external orders. Returns None if the process fails.
    """

    def convert_timestamps(df):
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return df

    # Convert datetime columns in each DataFrame to string format (ISO 8601)
    vehicles = convert_timestamps(vehicles)
    jobs = convert_timestamps(jobs)
    timeWindowProfiles = convert_timestamps(timeWindowProfiles)
    breaks = convert_timestamps(breaks)

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

    # Define expected columns and data types for each DataFrame
    vehicle_columns = {
        'vehicleTypeId': 'str', 'availableVehicles': 'int', 'startId': 'str', 
        'startLatitude': 'float', 'startLongitude': 'float', 'endId': 'str', 
        'endLatitude': 'float', 'endLongitude': 'float', 'maxWeight': 'float', 
        'maxVolume': 'float', 'maxPallets': 'int', 'maxStops': 'int', 
        'timeWindowStart': 'str', 'timeWindowEnd': 'str', 'profile': 'str', 
        'speedFactor': 'float', 'fixed': 'float', 'perHour': 'float',  'perKilometer': 'float', 'costPerStop': 'float', 'minimumTravelTime': 'float', 'maxTravelTime': 'float', 'max_distance': 'float', 'maximumDistanceBetweenStops': 'float', 'breakId': 'str'
    }
    job_columns = {
        'shipmentId': 'str', 'fromName': 'str', 'fromLatitude': 'float', 
        'fromLongitude': 'float', 'senderStopDuration': 'float', 
        'senderTimeWindowProfile': 'str', 'toName': 'str', 'toLatitude': 'float', 
        'toLongitude': 'float', 'recipientStopDuration': 'float', 
        'recipientTimeWindowProfile': 'str', 'weight': 'float', 
        'volume': 'float', 'pallets': 'int', 'vehicleTypeId': 'str', 'external_costs': 'float'
    }
    timeWindowProfile_columns = {
        'timeWindowProfileId': 'str', 'timeWindowProfileStart': 'str', 
        'timeWindowProfileEnd': 'str'
    }
    break_columns = {
        'breakId': 'str', 'earliestBreakStart': 'str', 'latestBreakStart': 'str', 'earliestRelativeBreakStart': 'str', 'latestRelativeBreakStart': 'str', 'breakDuration': 'float'
    }

    # Perform validation and conversion for each DataFrame
    vehicles = validate_and_convert_data_types(vehicles, vehicle_columns)
    jobs = validate_and_convert_data_types(jobs, job_columns)
    timeWindowProfiles = validate_and_convert_data_types(timeWindowProfiles, timeWindowProfile_columns)
    breaks = validate_and_convert_data_types(breaks, break_columns)

    # Exit if any DataFrame validation failed
    if any(df is None for df in [vehicles, jobs, timeWindowProfiles, breaks]):
        return None

    DEFAULT_LOG_HUB_API_SERVER = "https://production.supply-chain-apps.log-hub.com"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/reversetransportoptimizationplus"
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    payload = {
        "vehicles": vehicles.to_dict(orient='records'),
        "jobs": jobs.to_dict(orient='records'),
        "timeWindowProfiles": timeWindowProfiles.to_dict(orient='records'),
        "breaks": breaks.to_dict(orient='records'),
        "parameters": parameters
    }
    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                route_overview_df = pd.DataFrame(response_data['routeOverview'])
                route_details_df = pd.DataFrame(response_data['routeDetails'])
                external_orders_df = pd.DataFrame(response_data['externalOrders'])
                return route_overview_df, route_details_df, external_orders_df
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in reverse transport optimization API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None


def reverse_transport_optimization_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'transportPlusReverse.xlsx')
    vehicles_df = pd.read_excel(data_path, sheet_name='vehicles', usecols='A:Z', dtype={'maxTravelTime': int}).fillna("")
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:Q').fillna("")
    time_window_profiles_df = pd.read_excel(data_path, sheet_name='timeWindowProfiles', usecols='A:D').fillna("")
    breaks_df = pd.read_excel(data_path, sheet_name='breaks', usecols='A:G').fillna("")

    parameters = {
        "durationUnit": "min",
        "distanceUnit": "km"
    }
    return {'vehicles': vehicles_df, 'shipments': shipments_df, 'timeWindowProfiles': time_window_profiles_df, 'breaks': breaks_df, 'parameters': parameters}

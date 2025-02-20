import os

import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import convert_timestamps, validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url

def forward_transport_optimization_plus(vehicles: pd.DataFrame, jobs: pd.DataFrame, timeWindowProfiles: pd.DataFrame, breaks: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Three pandas DataFrames containing route overview, route details, 
                                                     and external orders. Returns None if the process fails.
    """

    # Convert datetime columns in each DataFrame to string format (ISO 8601)
    vehicles = convert_timestamps(vehicles)
    jobs = convert_timestamps(jobs)
    timeWindowProfiles = convert_timestamps(timeWindowProfiles)
    breaks = convert_timestamps(breaks)

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

    url = create_url("transportoptimizationplus")
    
    headers = create_headers(api_key)

    payload = {
        "vehicles": vehicles.to_dict(orient='records'),
        "jobs": jobs.to_dict(orient='records'),
        "timeWindowProfiles": timeWindowProfiles.to_dict(orient='records'),
        "breaks": breaks.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    
    response_data = post_method(url, payload, headers, "transport optimization plus")
    if response_data is None:
        return None
    else:
        route_overview_df = pd.DataFrame(response_data['routeOverview'])
        route_details_df = pd.DataFrame(response_data['routeDetails'])
        external_orders_df = pd.DataFrame(response_data['externalOrders'])
        return route_overview_df, route_details_df, external_orders_df
           
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
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'vehicles': vehicles_df, 'shipments': shipments_df, 'timeWindowProfiles': time_window_profiles_df,
             'breaks': breaks_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_transport_optimization_plus(vehicles: pd.DataFrame, jobs: pd.DataFrame, timeWindowProfiles: pd.DataFrame, breaks: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Three pandas DataFrames containing route overview, route details, 
                                                     and external orders. Returns None if the process fails.
    """

    # Convert datetime columns in each DataFrame to string format (ISO 8601)
    vehicles = convert_timestamps(vehicles)
    jobs = convert_timestamps(jobs)
    timeWindowProfiles = convert_timestamps(timeWindowProfiles)
    breaks = convert_timestamps(breaks)

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

    url  =create_url("reversetransportoptimizationplus")
    
    headers = create_headers(api_key)
    payload = {
        "vehicles": vehicles.to_dict(orient='records'),
        "jobs": jobs.to_dict(orient='records'),
        "timeWindowProfiles": timeWindowProfiles.to_dict(orient='records'),
        "breaks": breaks.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "reverse transport optimization plus")
    if response_data is None:
        return None
    else:
        route_overview_df = pd.DataFrame(response_data['routeOverview'])
        route_details_df = pd.DataFrame(response_data['routeDetails'])
        external_orders_df = pd.DataFrame(response_data['externalOrders'])
        return route_overview_df, route_details_df, external_orders_df

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
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'vehicles': vehicles_df, 'shipments': shipments_df, 'timeWindowProfiles': time_window_profiles_df,
             'breaks': breaks_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

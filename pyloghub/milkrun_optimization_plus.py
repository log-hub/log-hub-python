import os
import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import logging
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import convert_timestamps, validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_milkrun_optimization_plus(depots: pd.DataFrame, vehicles: pd.DataFrame, jobs: pd.DataFrame, timeWindowProfiles: pd.DataFrame, breaks: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Perform milkrun optimization based on depots, vehicles, jobs, time window profiles, and breaks.

    This function takes five DataFrames representing depots, vehicles, jobs, time window profiles, and breaks, 
    along with a parameters dictionary and an API key. It performs milkrun optimization using the Log-hub service.

    Parameters:
    depots (pd.DataFrame): DataFrame containing depot information.
        Columns:
        - country (str): Country code.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - depotId (str): Depot Id.
        - processingTimeAtTheDepo (number): Loading or unloading time at depot.

    vehicles (pd.DataFrame): DataFrame containing vehicle information.
        Columns:
        - vehicleTypeId (str): Vehicle Type Id.
        - availableVehicles (number): Available Vehicles.
        - startDepot (str): Start Depot.
        - endDepot (str): End Depot.
        - maxWeight (number): Maximum Weight.
        - maxVolume (number): Maximum Volume.
        - maxPallets (number): Maximum Pallets.
        - maxStops (number): Max Stops.
        - timeWindowStart (str): Time Window Start (ISO 8601 format).
        - timeWindowEnd (str): Time Window End (ISO 8601 format).
        - profile (str): Profile.
        - speedFactor (number): Speed Factor.
        - fixed (number): Fixed cost.
        - perHour (number): Cost per hour.
        - perKilometer (number): Cost per kilometer.
        - costPerStop (number): Cost per stop.
        - minimumTravelTime (number): Min travel time.
        - maxTravelTime (number): Max Travel Time.
        - max_distance (number): Maximum number of kilometers that vehicle can drive per route.
        - maximumDistanceBetweenStops (number): Maximum number of kilometers that vehicle can drive between each stop.
        - breakId (str): Break Id.

    jobs (pd.DataFrame): DataFrame containing job information.
        Columns:
        - country (str): Country code.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - orderId (str): Order Id.
        - weight (number): Weight.
        - volume (number): Volume.
        - pallets (number): Pallets.
        - pickupDelivery (str): Pickup/Delivery.
        - vehicleTypeId (str): Vehicle Type Id.
        - stopDuration (number): Stop Duration.
        - timeWindowProfile (str): Time Window Profile.
        - stopDurationAtDepo (number): Loading/Unloading Time at Depot.
        - external_costs (number): External costs for order.

    timeWindowProfiles (pd.DataFrame): DataFrame containing time window profile information.
        Columns:
        - timeWindowProfileId (str): Time Window Profile Id.
        - timeWindowProfileStart (str): Time Window Profile Start (ISO 8601 format).
        - timeWindowProfileEnd (str): Time Window Profile End (ISO 8601 format).

    breaks (pd.DataFrame): DataFrame containing break information.
        Columns:
        - breakId (str): Break Id.
        - earliestBreakStart (str): Earliest Break Start (ISO 8601 format).
        - latestBreakStart (str): Latest Break Start (ISO 8601 format).
        - earliestRelativeBreakStart (str): Minimum driving time before the break can start (ISO 8601 format).
        - latestRelativeBreakTime (str): Maximum driving time until the break must start (ISO 8601 format).
        - breakDuration (number): Break Duration.

    parameters (Dict): Dictionary containing parameters like durationUnit.

    api_key (str): Log-hub API key for accessing the milkrun optimization service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Three pandas DataFrames containing route overview, route details, 
                                                     and external orders. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    # Convert datetime columns in each DataFrame to string format (ISO 8601)
    depots = convert_timestamps(depots)
    vehicles = convert_timestamps(vehicles)
    jobs = convert_timestamps(jobs)
    timeWindowProfiles = convert_timestamps(timeWindowProfiles)
    breaks = convert_timestamps(breaks)

    # Define expected columns and data types for each DataFrame
    depot_columns = {
        'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 
        'street': 'str', 'depotId': 'str', 'processingTimeAtTheDepo': 'float'
    }
    vehicle_columns = {
        'vehicleTypeId': 'str', 'availableVehicles': 'int', 'startDepot': 'str', 
        'endDepot': 'str', 'maxWeight': 'float', 'maxVolume': 'float', 
        'maxPallets': 'int', 'maxStops': 'int', 'timeWindowStart': 'str', 
        'timeWindowEnd': 'str', 'profile': 'str', 'speedFactor': 'float', 
        'fixed': 'float', 'perHour': 'float', 'perKilometer': 'float', 'costPerStop': 'float', 'minimumTravelTime':'float', 'maxTravelTime': 'float', 'max_distance': 'float', 'maximumDistanceBetweenStops': 'float', 'breakId': 'str'
    }   
    job_columns = {
        'country': 'str', 'state': 'str', 'postalCode': 'str', 'city': 'str', 
        'street': 'str', 'orderId': 'str', 'weight': 'float', 'volume': 'float', 
        'pallets': 'int', 'pickupDelivery': 'str', 'depotId': 'str', 'vehicleTypeId': 'str', 
        'stopDuration': 'float', 'timeWindowProfile': 'str', 'stopDurationAtDepo': 'float', 'external_costs':'float'
    }
    timeWindowProfile_columns = {
        'timeWindowProfileId': 'str', 'timeWindowProfileStart': 'str', 
        'timeWindowProfileEnd': 'str'
    } 
    break_columns = {
        'breakId': 'str', 'earliestBreakStart': 'str', 'latestBreakStart': 'str', 'earliestRelativeBreakStart':'str', 'latestRelativeBreakStart': 'str', 'breakDuration': 'float'
    }

    # Perform validation and conversion for each DataFrame
    depots = validate_and_convert_data_types(depots, depot_columns)
    vehicles = validate_and_convert_data_types(vehicles, vehicle_columns)
    jobs = validate_and_convert_data_types(jobs, job_columns)
    timeWindowProfiles = validate_and_convert_data_types(timeWindowProfiles, timeWindowProfile_columns)
    breaks = validate_and_convert_data_types(breaks, break_columns)

    # Exit if any DataFrame validation failed
    if any(df is None for df in [depots, vehicles, jobs, timeWindowProfiles, breaks]):
        return None

    url = create_url("milkrunoptimizationplus")
    
    headers = create_headers(api_key)

    payload = {
        "depots": depots.to_dict(orient='records'),
        "vehicles": vehicles.to_dict(orient='records'),
        "jobs": jobs.to_dict(orient='records'),
        "timeWindowProfiles": timeWindowProfiles.to_dict(orient='records'),
        "breaks": breaks.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "milkrun optimization plus")
    if response_data is None:
        return None
    else:
        route_overview_df = pd.DataFrame(response_data['routeOverview'])
        route_details_df = pd.DataFrame(response_data['routeDetails'])
        external_orders_df = pd.DataFrame(response_data['externalOrders'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return route_overview_df, route_details_df, external_orders_df

def forward_milkrun_optimization_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MilkrunPlusSampleDataAddresses.xlsx')
    depots_df = pd.read_excel(data_path, sheet_name='depots', usecols='A:H', dtype={'postalCode': str})
    vehicles_df = pd.read_excel(data_path, sheet_name='vehicles', usecols='A:V', dtype={'maxTravelTime': int})
    jobs_df = pd.read_excel(data_path, sheet_name='jobs', usecols='A:Q', dtype={'postalCode': str})
    time_window_profiles_df = pd.read_excel(data_path, sheet_name='timeWindowProfiles', usecols='A:D')
    breaks_df = pd.read_excel(data_path, sheet_name='breaks', usecols='A:G')

    parameters = {
        "durationUnit": "min"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'depots': depots_df, 'vehicles': vehicles_df, 'jobs': jobs_df, 'timeWindowProfiles': time_window_profiles_df, 'breaks': breaks_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}


def reverse_milkrun_optimization_plus(depots: pd.DataFrame, vehicles: pd.DataFrame, jobs: pd.DataFrame, timeWindowProfiles: pd.DataFrame, breaks: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Perform reverse milkrun optimization based on depots, vehicles, jobs, time window profiles, and breaks.

    This function takes five DataFrames representing depots, vehicles, jobs, time window profiles, and breaks, 
    along with a parameters dictionary and an API key. It performs reverse milkrun optimization using the Log-hub service.

    Parameters:
    depots (pd.DataFrame): DataFrame containing depot information, with columns:
        - depotId (str): Depot Id.
        - latitude (float): Latitude of the depot.
        - longitude (float): Longitude of the depot.
        - processingTimeAtTheDepo (number): Loading or unloading time at depot.

    vehicles (pd.DataFrame): DataFrame containing vehicle information, with columns:
        - vehicleTypeId (str): Vehicle Type Id.
        - availableVehicles (int): Available Vehicles.
        - startDepot (str): Start Depot.
        - endDepot (str): End Depot.
        - maxWeight (float): Maximum Weight.
        - maxVolume (float): Maximum Volume.
        - maxPallets (int): Maximum Pallets.
        - maxStops (int): Max Stops.
        - timeWindowStart (str): Time Window Start (ISO 8601 format).
        - timeWindowEnd (str): Time Window End (ISO 8601 format).
        - profile (str): Profile.
        - speedFactor (float): Speed Factor.
        - fixed (float): Fixed cost.
        - perHour (float): Cost per hour.
        - perKilometer (float): Cost per kilometer.
        - costPerStop (float): Cost per stop.
        - minimumTravelTime (float): Min travel time.
        - maxTravelTime (float): Max Travel Time.
        - max_distance (float): Maximum distance that vehicle can drive per route.
        - maximumDistanceBetweenStops (float): Maximum distance that vehicle can drive between two stops.
        - breakId (str): Break Id.

    jobs (pd.DataFrame): DataFrame containing job information, with columns:
        - orderId (str): Order Id.
        - latitude (float): Latitude of the job location.
        - longitude (float): Longitude of the job location.
        - depotId (str): Depot Id.
        - weight (float): Weight.
        - volume (float): Volume.
        - pallets (int): Pallets.
        - pickupDelivery (str): Pickup/Delivery.
        - depotId (str): Depot Id.
        - vehicleTypeId (str): Vehicle Type Id.
        - stopDuration (float): Stop Duration.
        - timeWindowProfile (str): Time Window Profile.
        - stopDurationAtDepo (float): Loading/Unloading Time at Depot.
        - external_costs (float): External costs.

    timeWindowProfiles (pd.DataFrame): DataFrame containing time window profile information, with columns:
        - timeWindowProfileId (str): Time Window Profile Id.
        - timeWindowProfileStart (str): Time Window Profile Start (ISO 8601 format).
        - timeWindowProfileEnd (str): Time Window Profile End (ISO 8601 format).

    breaks (pd.DataFrame): DataFrame containing break information, with columns:
        - breakId (str): Break Id.
        - earliestBreakStart (str): Earliest Break Start (ISO 8601 format).
        - latestBreakStart (str): Latest Break Start (ISO 8601 format).
        - earliestRelativeBreakStart (str): Earliest Relative Break Start (ISO 8601 format).
        - latestRelativeBreakStart (str): Latest Relative Break Start (ISO 8601 format).
        - breakDuration (float): Break Duration.

    parameters (Dict): Dictionary containing parameters like durationUnit.

    api_key (str): Log-hub API key for accessing the reverse milkrun optimization service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Three pandas DataFrames containing route overview, route details, 
                                                     and external orders. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    # Convert datetime columns in each DataFrame to string format (ISO 8601)
    depots = convert_timestamps(depots)
    vehicles = convert_timestamps(vehicles)
    jobs = convert_timestamps(jobs)
    timeWindowProfiles = convert_timestamps(timeWindowProfiles)
    breaks = convert_timestamps(breaks)

    # Define expected columns and data types for each DataFrame
    depot_columns = {
        'latitude': 'float', 'longitude': 'float', 'depotId': 'str', 'processingTimeAtTheDepo': 'float'
    }
    vehicle_columns = {
        'vehicleTypeId': 'str', 'availableVehicles': 'int', 'startDepot': 'str', 'endDepot': 'str',
        'maxWeight': 'float', 'maxVolume': 'float', 'maxPallets': 'int', 'maxStops': 'int',
        'timeWindowStart': 'str', 'timeWindowEnd': 'str', 'profile': 'str', 'speedFactor': 'float',
        'fixed': 'float', 'perHour': 'float', 'perKilometer': 'float', 'costPerStop': 'float', 'minimumTravelTime': 'float', 'maxTravelTime': 'float', 'max_distance': 'float', 'maximumDistanceBetweenStops': 'float', 'breakId': 'str'
    }
    job_columns = {
        'latitude': 'float', 'longitude': 'float', 'depotId': 'str', 'orderId': 'str',
        'weight': 'float', 'volume': 'float', 'pallets': 'int', 'pickupDelivery': 'str',
        'vehicleTypeId': 'str', 'stopDuration': 'float', 'timeWindowProfile': 'str', 
        'stopDurationAtDepo': 'float', 'external_costs': 'float'
    }
    timeWindowProfile_columns = {
        'timeWindowProfileId': 'str', 'timeWindowProfileStart': 'str', 'timeWindowProfileEnd': 'str'
    }
    break_columns = {
        'breakId': 'str', 'earliestBreakStart': 'str', 'latestBreakStart': 'str', 'earliestRelativeBreakStart': 'str', 'latestRelativeBreakStart': 'str', 'breakDuration': 'float'
    }

    # Perform validation and conversion for each DataFrame
    depots = validate_and_convert_data_types(depots, depot_columns)
    vehicles = validate_and_convert_data_types(vehicles, vehicle_columns)
    jobs = validate_and_convert_data_types(jobs, job_columns)
    timeWindowProfiles = validate_and_convert_data_types(timeWindowProfiles, timeWindowProfile_columns)
    breaks = validate_and_convert_data_types(breaks, break_columns)

    # Exit if any DataFrame validation failed
    if any(df is None for df in [depots, vehicles, jobs, timeWindowProfiles, breaks]):
        return None

    url = create_url("reversemilkrunoptimizationplus")
    
    headers = create_headers(api_key)

    payload = {
        "depots": depots.to_dict(orient='records'),
        "vehicles": vehicles.to_dict(orient='records'),
        "jobs": jobs.to_dict(orient='records'),
        "timeWindowProfiles": timeWindowProfiles.to_dict(orient='records'),
        "breaks": breaks.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "reverse milkrun optimization plus")
    if response_data is None:
        return None
    else:
        route_overview_df = pd.DataFrame(response_data['routeOverview'])
        route_details_df = pd.DataFrame(response_data['routeDetails'])
        external_orders_df = pd.DataFrame(response_data['externalOrders'])
        if (show_buttons and save_scenario['saveScenario']):
            create_buttons()
        if not save_scenario['saveScenario']:
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return route_overview_df, route_details_df, external_orders_df

def reverse_milkrun_optimization_plus_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MilkrunPlusSampleDataReverse.xlsx')
    depots_df = pd.read_excel(data_path, sheet_name='depots', usecols='A:E', dtype={'postalCode': str})
    vehicles_df = pd.read_excel(data_path, sheet_name='vehicles', usecols='A:V', dtype={'maxTravelTime': int})
    jobs_df = pd.read_excel(data_path, sheet_name='jobs', usecols='A:N', dtype={'postalCode': str})
    time_window_profiles_df = pd.read_excel(data_path, sheet_name='timeWindowProfiles', usecols='A:D')
    breaks_df = pd.read_excel(data_path, sheet_name='breaks', usecols='A:G')

    parameters = {
        "durationUnit": "min"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'depots': depots_df, 'vehicles': vehicles_df, 'jobs': jobs_df, 'timeWindowProfiles': time_window_profiles_df, 'breaks': breaks_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
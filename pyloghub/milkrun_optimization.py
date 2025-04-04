import os
import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import logging
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import validate_and_convert_data_types
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_milkrun_optimization(depots: pd.DataFrame, vehicle_types: pd.DataFrame, pickup_and_delivery: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Perform milkrun optimization based on depots, vehicle types, and pickup and delivery orders.

    This function takes three DataFrames representing depots, vehicle types, and pickup and delivery orders, 
    along with a parameters dictionary, an API key and parameters for saving the scenario. It performs milkrun optimization using the Log-hub service.

    Parameters:
    depots (pd.DataFrame): DataFrame containing depot information.
        Columns:
        - name (str): Name of the depot.
        - country (str): Country code.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.

    vehicle_types (pd.DataFrame): DataFrame containing vehicle type information.
        Columns:
        - type (str): Vehicle Type.
        - availableVehicles (number): The number of available vehicles per vehicle type.
        - startDepot (str): Start depot name of the vehicle type.
        - endDepot (str): End depot name of the vehicle type.
        - averageSpeed (number): Average speed.
        - maxRouteStops (number): The maximum number of stops per vehicle.
        - maxRouteLength (number): The maximum length per route. 
        - maxRouteDuration (number): The maximum route duration.
        - maxCapacityWeight (number): The maximum weight that can be loaded by a vehicle of the corresponding vehicle type. 
        - maxCapacityVolume (number): The maximum volume that can be loaded by a vehicle of the corresponding vehicle type. 
        - maxCapacityPallets (number):  The maximum number of pallets that can be loaded by a vehicle of the corresponding vehicle type.
        - fixedCosts (number): The fixed costs per vehicle in case of usage. 
        - costsPerStop (number): The costs per vehicle stop.
        - costsPerDistanceUnit (number): The costs per distance unit. 

     pickup_and_delivery (pd.DataFrame): DataFrame containing pickup and delivery information.
        Columns:
        - name (str): The name of the order. 
        - country (str): Country code.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.
        - weight (number): The weight of the order. 
        - volume (number): The volume of the order.
        - pallets (number): The number of pallets of the order.
        - pickupDelivery (str): Pickup/Delivery.
        - depot (str):  The depot name the order has to be delivered to.
        - vehicleType (str): All valid vehicle types for the order separated by semicolon.
        - serviceTime (number): Stop duration per order in minutes.
        - startTimeWindow (str): Start of the delivery/pickup time window per order.
        - endTimeWindow (str): End of the delivery/pickup time window per order.
        - externalCosts (number): External costs for order. 

    parameters (Dict): Dictionary containing parameters durationUnit and distanceUnit.

    api_key (str): Log-hub API key for accessing the milkrun optimization service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Five pandas DataFrames containing route overview, route details, external orders, input map routes with addresses information and input map routes with coordinates information. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    # Define expected columns and data types for each DataFrame
    depot_mandatory_columns = {
        'country': 'str', 'name': 'str'
    }
    depot_optional_columns = {
        'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'
    }

    vehicle_types_mandatory_columns = {
        'type': 'str', 'availableVehicles': 'float',  'startDepot': 'str', 'endDepot': 'str', 'averageSpeed': 'float', 'maxRouteStops': 'float', 'maxRouteLength': 'float', 'maxRouteDuration': 'float', 'maxCapacityWeight': 'float', 'maxCapacityVolume': 'float', 'maxCapacityPallets': 'float', 'fixedCosts': 'float', 'costsPerStop': 'float', 'costsPerDistanceUnit': 'float'
    }   
    pickup_and_delivery_mandatory_columns = {
        'name': 'str', 'country': 'str', 'weight': 'float', 'volume': 'float', 'pallets': 'float', 'depot': 'str', 'serviceTime': 'float', 'startTimeWindow': 'str', 'endTimeWindow': 'str', 'externalCosts': 'float'
    }
    pickup_and_delivery_optional_columns = {
        'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str', 'vehicleType': 'str', 'pickupDelivery': 'str'
    }

    # Perform validation and conversion for each DataFrame
    depots = validate_and_convert_data_types(depots, depot_mandatory_columns, 'mandatory', 'depots')
    if not depots is None:
        depots = validate_and_convert_data_types(depots, depot_optional_columns, 'optional', 'depots')
    vehicle_types = validate_and_convert_data_types(vehicle_types, vehicle_types_mandatory_columns, 'mandatory', 'vehicle types')
    pickup_and_delivery = validate_and_convert_data_types(pickup_and_delivery, pickup_and_delivery_mandatory_columns, 'mandatory', 'pickup and delivery')
    if not pickup_and_delivery is None:
        pickup_and_delivery = validate_and_convert_data_types(pickup_and_delivery, pickup_and_delivery_optional_columns, 'optional', 'pickup and delivery')

    # Exit if any DataFrame validation failed
    if any(df is None for df in [depots, vehicle_types, pickup_and_delivery]):
        return None

    url = create_url("milkrunoptimization")
    
    headers = create_headers(api_key)

    payload = {
        "depots": depots.to_dict(orient='records'),
        "vehicleTypes": vehicle_types.to_dict(orient='records'),
        "customers": pickup_and_delivery.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "milkrun optimization")
    if response_data is None:
        return None
    else:
        route_overview_df = pd.DataFrame(response_data['routeOverview'])
        route_details_df = pd.DataFrame(response_data['routeDetails'])
        external_orders_df = pd.DataFrame(response_data['droppedCustomers'])
        input_map_routes_df = pd.DataFrame(response_data['inputMapRoutes'])
        input_map_routes_geocodes_df = pd.DataFrame(response_data['inputMapRoutesGeocodes'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return route_overview_df, route_details_df, external_orders_df, input_map_routes_df, input_map_routes_geocodes_df

def forward_milkrun_optimization_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MilkrunSampleDataAddresses.xlsx')
    depots_df = pd.read_excel(data_path, sheet_name='depots', usecols='A:G', dtype={'postalCode': str})
    vehicle_types_df = pd.read_excel(data_path, sheet_name='vehicleTypes', usecols='A:O')
    pickup_and_delivery_df= pd.read_excel(data_path, sheet_name='pickupAndDelivery', usecols='A:Q', dtype={'postalCode': str})

    parameters = {
        "distanceUnit": "km",
        "durationUnit": "min"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'depots': depots_df, 'vehicleTypes': vehicle_types_df, 'pickupAndDelivery': pickup_and_delivery_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_milkrun_optimization(depots: pd.DataFrame, vehicle_types: pd.DataFrame, pickup_and_delivery: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Perform milkrun optimization based on depots, vehicle types, and pickup and delivery orders.

    This function takes three DataFrames representing depots, vehicle types, and pickup and delivery orders, 
    along with a parameters dictionary, an API key and parameters for saving the scenario. It performs milkrun optimization using the Log-hub service.

    Parameters:
    depots (pd.DataFrame): DataFrame containing depot information.
        Columns:
        - name (str): Name of the depot.
        - latitude (number): Latitude of the depot.
        - longitude (number): Longitude of the depot.

    vehicle_types (pd.DataFrame): DataFrame containing vehicle type information.
        Columns:
        - type (str): Vehicle Type.
        - availableVehicles (number): The number of available vehicles per vehicle type.
        - startDepot (str): Start depot name of the vehicle type.
        - endDepot (str): End depot name of the vehicle type.
        - averageSpeed (number): Average speed.
        - maxRouteStops (number): The maximum number of stops per vehicle.
        - maxRouteLength (number): The maximum length per route. 
        - maxRouteDuration (number): The maximum route duration.
        - maxCapacityWeight (number): The maximum weight that can be loaded by a vehicle of the corresponding vehicle type. 
        - maxCapacityVolume (number): The maximum volume that can be loaded by a vehicle of the corresponding vehicle type. 
        - maxCapacityPallets (number):  The maximum number of pallets that can be loaded by a vehicle of the corresponding vehicle type.
        - fixedCosts (number): The fixed costs per vehicle in case of usage. 
        - costsPerStop (number): The costs per vehicle stop.
        - costsPerDistanceUnit (number): The costs per distance unit. 

     pickup_and_delivery (pd.DataFrame): DataFrame containing pickup and delivery information.
        Columns:
        - name (str): The name of the order. 
        - latitude (number): Latitude of the customer.
        - longitude (number): Longitude of the customer.
        - weight (number): The weight of the order. 
        - volume (number): The volume of the order.
        - pallets (number): The number of pallets of the order.
        - pickupDelivery (str): Pickup/Delivery.
        - depot (str):  The depot name the order has to be delivered to.
        - vehicleType (str): All valid vehicle types for the order separated by semicolon.
        - serviceTime (number): Stop duration per order in minutes.
        - startTimeWindow (str): Start of the delivery/pickup time window per order.
        - endTimeWindow (str): End of the delivery/pickup time window per order.
        - externalCosts (number): External costs for order. 

    parameters (Dict): Dictionary containing parameters durationUnit and distanceUnit.

    api_key (str): Log-hub API key for accessing the reverse milkrun optimization service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Four pandas DataFrames containing route overview, route details, external orders and input map routes with coordinates information. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    # Define expected columns and data types for each DataFrame
    depot_mandatory_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }

    vehicle_types_mandatory_columns = {
        'type': 'str', 'availableVehicles': 'float',  'startDepot': 'str', 'endDepot': 'str', 'averageSpeed': 'float', 'maxRouteStops': 'float', 'maxRouteLength': 'float', 'maxRouteDuration': 'float', 'maxCapacityWeight': 'float', 'maxCapacityVolume': 'float', 'maxCapacityPallets': 'float', 'fixedCosts': 'float', 'costsPerStop': 'float', 'costsPerDistanceUnit': 'float'
    }   
    pickup_and_delivery_mandatory_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float', 'weight': 'float', 'volume': 'float', 'pallets': 'float', 'depot': 'str', 'serviceTime': 'float', 'startTimeWindow': 'str', 'endTimeWindow': 'str', 'externalCosts': 'float'
    }
    pickup_and_delivery_optional_columns = {
        'vehicleType': 'str', 'pickupDelivery': 'str'
    }

    # Perform validation and conversion for each DataFrame
    depots = validate_and_convert_data_types(depots, depot_mandatory_columns, 'mandatory', 'depots')
    vehicle_types = validate_and_convert_data_types(vehicle_types, vehicle_types_mandatory_columns, 'mandatory', 'vehicle types')
    pickup_and_delivery = validate_and_convert_data_types(pickup_and_delivery, pickup_and_delivery_mandatory_columns, 'mandatory', 'pickup and delivery')
    if not pickup_and_delivery is None:
        pickup_and_delivery = validate_and_convert_data_types(pickup_and_delivery, pickup_and_delivery_optional_columns, 'optional', 'pickup and delivery')

    # Exit if any DataFrame validation failed
    if any(df is None for df in [depots, vehicle_types, pickup_and_delivery]):
        return None

    url = create_url("reversemilkrunoptimization")
    
    headers = create_headers(api_key)

    payload = {
        "depots": depots.to_dict(orient='records'),
        "vehicleTypes": vehicle_types.to_dict(orient='records'),
        "customers": pickup_and_delivery.to_dict(orient='records'),
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "reverse milkrun optimization")
    if response_data is None:
        return None
    else:
        route_overview_df = pd.DataFrame(response_data['routeOverview'])
        route_details_df = pd.DataFrame(response_data['routeDetails'])
        external_orders_df = pd.DataFrame(response_data['droppedCustomers'])
        input_map_routes_geocodes_df = pd.DataFrame(response_data['inputMapRoutesGeocodes'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return route_overview_df, route_details_df, external_orders_df, input_map_routes_geocodes_df

def reverse_milkrun_optimization_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'MilkrunSampleDataReverse.xlsx')
    depots_df = pd.read_excel(data_path, sheet_name='depots', usecols='A:D')
    vehicle_types_df = pd.read_excel(data_path, sheet_name='vehicleTypes', usecols='A:O')
    pickup_and_delivery_df= pd.read_excel(data_path, sheet_name='pickupAndDelivery', usecols='A:N')

    parameters = {
        "distanceUnit": "km",
        "durationUnit": "min"
    }
    save_scenario = {
        'saveScenario': False,
        'overwriteScenario': False,
        'workspaceId': 'Your workspace id',
        'scenarioName': 'Your scenario name'
    }
    return {'depots': depots_df, 'vehicleTypes': vehicle_types_df, 'pickupAndDelivery': pickup_and_delivery_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
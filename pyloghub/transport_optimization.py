import os
import logging
import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check, create_button
from input_data_validation import convert_timestamps, validate_and_convert_data_types, convert_to_float, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url, get_workspace_entities

def forward_transport_optimization(locations: pd.DataFrame, vehicle_types: pd.DataFrame, shipments: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Perform transport optimization based on locations, vehicle types, and shipments.

    This function takes three DataFrames representing locations, vehicle types, and shipments, 
    along with a parameters dictionary, an API key and parameters for saving the scenario. It performs transport optimization using the Log-hub service.

    Parameters:
    locations (pd.DataFrame): DataFrame containing locations information.
        Columns:
        - name (str): Name of the location.
        - country (str): Country code.
        - state (str): State code.
        - postalCode (str): Postal code.
        - city (str): City name.
        - street (str): Street name with house number.

    vehicle_types (pd.DataFrame): DataFrame containing vehicle type information.
        Columns:
        - type (str): Vehicle Type.
        - availableVehicles (number): The number of available vehicles per vehicle type.
        - startLocation (str): Start location name of the vehicle type.
        - endLocation (str): End location name of the vehicle type.
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

     shipments (pd.DataFrame): DataFrame containing shipments information.
        Columns:
        - name (str): The name of the shipment. 
        - senderId (str): Sender id of the shipment.
        - senderStopDuration (float): Service time needed on the pickup location of the shipment.
        - earliestPickupTime (str): Start of the pickup time window per shipment.
        - latestPickupTime (str): End of the pickup time window per shipment.
        - recipientId (str): Recipient id of the shipment.
        - recipientStopDuration (float): Service time needed on the delivery location of the shipment.
        - earliestDeliveryTime (str): Start of the delivery time window per shipment.
        - latestDeliveryTime (str): End of the delivery time window per shipment.
        - weight (number): The weight of the shipment. 
        - volume (number): The volume of the shipment.
        - pallets (number): The number of pallets of the shipment.
        - externalCosts (number): External costs for shipment.
        - vehicleType (str): All valid vehicle types for the order separated by semicolon.   

    parameters (Dict): Dictionary containing parameters durationUnit and distanceUnit.

    api_key (str): Log-hub API key for accessing the transport optimization service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Five pandas DataFrames containing transport overview, transport details, dropped shipments, input map routes with addresses information and input map routes with coordinates information. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    # Define expected columns and data types for each DataFrame
    locations_mandatory_columns = {
        'country': 'str', 'name': 'str'
    }
    locations_optional_columns = {
        'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'
    }

    vehicle_types_mandatory_columns = {
        'type': 'str', 'availableVehicles': 'float',  'startLocation': 'str', 'endLocation': 'str', 'averageSpeed': 'float', 'maxRouteStops': 'float', 'maxRouteLength': 'float', 'maxRouteDuration': 'float', 'maxCapacityWeight': 'float', 'maxCapacityVolume': 'float', 'maxCapacityPallets': 'float', 'fixedCosts': 'float', 'costsPerStop': 'float', 'costsPerDistanceUnit': 'float'
    }   
    shipments_mandatory_columns = {
        'name': 'str', 'senderId': 'str', 'senderStopDuration': 'float', 'earliestPickupTime': 'str', 'latestPickupTime': 'str', 'recipientId': 'str', 'recipientStopDuration': 'float', 'earliestDeliveryTime': 'str',  'latestDeliveryTime': 'str', 'weight': 'float', 'externalCosts': 'float'
    }
    shipemnts_optional_columns = {
        'vehicleType': 'str'
    }
    shipments_optional_floats = ['volume', 'pallets']

    # Perform validation and conversion for each DataFrame
    locations = validate_and_convert_data_types(locations, locations_mandatory_columns, 'mandatory', 'locations')
    if not locations is None:
        locations = validate_and_convert_data_types(locations, locations_optional_columns, 'optional', 'locations')
    vehicle_types = validate_and_convert_data_types(vehicle_types, vehicle_types_mandatory_columns, 'mandatory', 'vehicle types')
    shipments = validate_and_convert_data_types(shipments, shipments_mandatory_columns, 'mandatory', 'shipments')
    if not shipments is None:
        shipments = validate_and_convert_data_types(shipments, shipemnts_optional_columns, 'optional', 'shipments')
        if not shipments is None:
            shipments = convert_to_float(shipments, shipments_optional_floats, 'optional')
            shipments = convert_timestamps(shipments)
            shipments = convert_df_to_dict_excluding_nan(shipments, shipments_optional_floats)

    # Exit if any DataFrame validation failed
    if any(df is None for df in [locations, vehicle_types, shipments]):
        return None

    url = create_url("transportoptimization")
    
    headers = create_headers(api_key)

    payload = {
        "locations": locations.to_dict(orient='records'),
        "vehicleTypes": vehicle_types.to_dict(orient='records'),
        "shipments": shipments,
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "transport optimization")
    if response_data is None:
        return None
    else:
        transport_overview_df = pd.DataFrame(response_data['transportOverview'])
        transport_details_df = pd.DataFrame(response_data['transportDetails'])
        dropped_shipments_df = pd.DataFrame(response_data['droppedShipments'])
        input_map_routes_df = pd.DataFrame(response_data['inputMapRoutes'])
        input_map_routes_geocodes_df = pd.DataFrame(response_data['inputMapRoutesGeocodes'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return transport_overview_df, transport_details_df, dropped_shipments_df, input_map_routes_df, input_map_routes_geocodes_df

def forward_transport_optimization_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'transportAddresses.xlsx')
    locations_df = pd.read_excel(data_path, sheet_name='locations', usecols='A:G').fillna("")
    vehicle_types_df = pd.read_excel(data_path, sheet_name='vehicleTypes', usecols='A:O').fillna("")
    shipments_df = pd.read_excel(data_path, sheet_name='shipments', usecols='A:O').fillna("")

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
    return {'locations': locations_df, 'vehicleTypes': vehicle_types_df, 'shipments': shipments_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}

def reverse_transport_optimization(locations: pd.DataFrame, vehicle_types: pd.DataFrame, shipments: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}, show_buttons = False) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Perform transport optimization based on locations, vehicle types, and shipments.

    This function takes three DataFrames representing locations, vehicle types, and shipments, 
    along with a parameters dictionary, an API key and parameters for saving the scenario. It performs transport optimization using the Log-hub service.

    Parameters:
    locations (pd.DataFrame): DataFrame containing locations information.
        Columns:
        - name (str): Name of the location.
        - latitude (number): Latitude of the location.
        - longitude (number): Longitude of the location.

    vehicle_types (pd.DataFrame): DataFrame containing vehicle type information.
        Columns:
        - type (str): Vehicle Type.
        - availableVehicles (number): The number of available vehicles per vehicle type.
        - startLocation (str): Start location name of the vehicle type.
        - endLocation (str): End location name of the vehicle type.
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

     shipments (pd.DataFrame): DataFrame containing shipments information.
        Columns:
        - name (str): The name of the order. 
        - senderId (str): Sender id of the shipment.
        - senderStopDuration (float): Service time needed on the pickup location of the shipment.
        - earliestPickupTime (str): Start of the pickup time window per shipment.
        - latestPickupTime (str): End of the pickup time window per shipment.
        - recipientId (str): Recipient id of the shipment.
        - recipientStopDuration (float): Service time needed on the delivery location of the shipment.
        - earliestDeliveryTime (str): Start of the delivery time window per shipment.
        - latestDeliveryTime (str): End of the delivery time window per shipment.
        - weight (number): The weight of the shipment. 
        - volume (number): The volume of the shipment.
        - pallets (number): The number of pallets of the shipment.
        - externalCosts (number): External costs for shipment.
        - vehicleType (str): All valid vehicle types for the order separated by semicolon.   

    parameters (Dict): Dictionary containing parameters durationUnit and distanceUnit.

    api_key (str): Log-hub API key for accessing the reverse transport optimization service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    show_buttons (boolean): If this parameter is set to True and the scenario is saved on the platform, the buttons linking to the output results, map, dashboard and the input table 
                           will be created. If the scenario is not saved, a proper message will be shown.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Four pandas DataFrames containing transport overview, trasnport details, dropped shipments and input map routes with coordinates information. Returns None if the process fails.
    """
    def create_buttons():
        links = get_workspace_entities(save_scenario, api_key)
        create_button(links = [links['map'], links['dashboard'], links['inputDataset'], links['outputDataset']], texts = ["🌍 Open Map", "📊 Open Dashboard", "📋 Show Input Dataset", "📋 Show Output Dataset"])

    # Define expected columns and data types for each DataFrame
    locations_mandatory_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }

    vehicle_types_mandatory_columns = {
        'type': 'str', 'availableVehicles': 'float',  'startLocation': 'str', 'endLocation': 'str', 'averageSpeed': 'float', 'maxRouteStops': 'float', 'maxRouteLength': 'float', 'maxRouteDuration': 'float', 'maxCapacityWeight': 'float', 'maxCapacityVolume': 'float', 'maxCapacityPallets': 'float', 'fixedCosts': 'float', 'costsPerStop': 'float', 'costsPerDistanceUnit': 'float'
    }   
    shipments_mandatory_columns = {
        'name': 'str', 'senderId': 'str', 'senderStopDuration': 'float', 'earliestPickupTime': 'str', 'latestPickupTime': 'str', 'recipientId': 'str', 'recipientStopDuration': 'float', 'earliestDeliveryTime': 'str',  'latestDeliveryTime': 'str', 'weight': 'float', 'externalCosts': 'float'
    }
    shipemnts_optional_columns = {
        'vehicleType': 'str'
    }
    shipments_optional_floats = ['volume', 'pallets']

    # Perform validation and conversion for each DataFrame
    locations = validate_and_convert_data_types(locations, locations_mandatory_columns, 'mandatory', 'locations')
    vehicle_types = validate_and_convert_data_types(vehicle_types, vehicle_types_mandatory_columns, 'mandatory', 'vehicle types')
    shipments = validate_and_convert_data_types(shipments, shipments_mandatory_columns, 'mandatory', 'shipments')
    if not shipments is None:
        shipments = validate_and_convert_data_types(shipments, shipemnts_optional_columns, 'optional', 'shipments')
        if not shipments is None:
            shipments = convert_to_float(shipments, shipments_optional_floats, 'optional')
            shipments = convert_timestamps(shipments)
            shipments = convert_df_to_dict_excluding_nan(shipments, shipments_optional_floats)


    # Exit if any DataFrame validation failed
    if any(df is None for df in [locations, vehicle_types, shipments]):
        return None

    url = create_url("reversetransportoptimization")
    
    headers = create_headers(api_key)

    payload = {
        "locations": locations.to_dict(orient='records'),
        "vehicleTypes": vehicle_types.to_dict(orient='records'),
        "shipments": shipments,
        "parameters": parameters
    }
    payload = save_scenario_check(save_scenario, payload)
    response_data = post_method(url, payload, headers, "reverse transport optimization")
    if response_data is None:
        return None
    else:
        transport_overview_df = pd.DataFrame(response_data['transportOverview'])
        transport_details_df = pd.DataFrame(response_data['transportDetails'])
        dropped_shipments_df = pd.DataFrame(response_data['droppedShipments'])
        input_map_routes_geocodes_df = pd.DataFrame(response_data['inputMapRoutesGeocodes'])
        if (show_buttons and payload['saveScenarioParameters']['saveScenario']):
            create_buttons()
        if (not payload['saveScenarioParameters']['saveScenario'] and show_buttons):
            logging.info("Please, save the scenario in order to create the buttons for opening the results on the platform.")
        return transport_overview_df, transport_details_df, dropped_shipments_df, input_map_routes_geocodes_df

def reverse_transport_optimization_sample_data():
    warnings.simplefilter("ignore", category=UserWarning)
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'TransportSampleDataReverse.xlsx')
    locations_df = pd.read_excel(data_path, sheet_name='locations', usecols='A:D')
    vehicle_types_df = pd.read_excel(data_path, sheet_name='vehicleTypes', usecols='A:O')
    shipments_df= pd.read_excel(data_path, sheet_name='shipments', usecols='A:O')

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
    return {'locations': locations_df, 'vehicleTypes': vehicle_types_df, 'shipments': shipments_df, 'parameters': parameters, 'saveScenarioParameters': save_scenario}
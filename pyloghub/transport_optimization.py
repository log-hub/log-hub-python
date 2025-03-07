import os

import pandas as pd
import warnings
from typing import Optional, Dict, Tuple
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyloghub')))
from save_to_platform import save_scenario_check
from input_data_validation import convert_timestamps, validate_and_convert_data_types, convert_to_float, convert_df_to_dict_excluding_nan
from sending_requests import post_method, create_headers, create_url

def forward_transport_optimization(locations: pd.DataFrame, vehicle_types: pd.DataFrame, shipments: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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
        - maxCapacityLoadingMeter (number):  The maximum number of pallets that can be loaded by a vehicle of the corresponding vehicle type.
        - fixedCosts (number): The fixed costs per vehicle in case of usage. 
        - costsPerStop (number): The costs per vehicle stop.
        - costsPerKm (number): The costs per distance unit. 

     shipments (pd.DataFrame): DataFrame containing shipments information.
        Columns:
        - name (str): The name of the shipment. 
        - sender (str): Sender id of the shipment.
        - senderServiceTime (float): Service time needed on the pickup location of the shipment.
        - earliestPickupTime (str): Start of the pickup time window per shipment.
        - latestPickupTime (str): End of the pickup time window per shipment.
        - recipient (str): Recipient id of the shipment.
        - recipientServiceTime (float): Service time needed on the delivery location of the shipment.
        - earliestDeliveryTime (str): Start of the delivery time window per shipment.
        - latestDeliveryTime (str): End of the delivery time window per shipment.
        - weight (number): The weight of the shipment. 
        - volume (number): The volume of the shipment.
        - loadingMeter (number): The number of pallets of the shipment.
        - opportunityCosts (number): External costs for shipment.
        - vehicleType (str): All valid vehicle types for the order separated by semicolon.   

    parameters (Dict): Dictionary containing parameters durationUnit and distanceUnit.

    api_key (str): Log-hub API key for accessing the milkrun optimization service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Five pandas DataFrames containing transport overview, transport details, dropped shipments, input map routes with addresses information and input map routes with coordinates information. Returns None if the process fails.
    """

    # Define expected columns and data types for each DataFrame
    locations_mandatory_columns = {
        'country': 'str', 'name': 'str'
    }
    locations_optional_columns = {
        'state': 'str', 'postalCode': 'str', 'city': 'str', 'street': 'str'
    }

    vehicle_types_mandatory_columns = {
        'type': 'str', 'availableVehicles': 'float',  'startLocation': 'str', 'endLocation': 'str', 'averageSpeed': 'float', 'maxRouteStops': 'float', 'maxRouteLength': 'float', 'maxRouteDuration': 'float', 'maxCapacityWeight': 'float', 'maxCapacityVolume': 'float', 'maxCapacityLoadingMeter': 'float', 'fixedCosts': 'float', 'costsPerStop': 'float', 'costsPerKm': 'float'
    }   
    shipments_mandatory_columns = {
        'name': 'str', 'sender': 'str', 'senderServiceTime': 'float', 'earliestPickupTime': 'str', 'latestPickupTime': 'str', 'recipient': 'str', 'recipientServiceTime': 'float', 'earliestDeliveryTime': 'str',  'latestDeliveryTime': 'str', 'weight': 'float', 'opportunityCosts': 'float'
    }
    shipemnts_optional_columns = {
        'vehicleType': 'str'
    }
    shipments_optional_floats = ['volume', 'loadingMeter']

    # Perform validation and conversion for each DataFrame
    locations = validate_and_convert_data_types(locations, locations_mandatory_columns, 'mandatory')
    if not locations is None:
        locations = validate_and_convert_data_types(locations, locations_optional_columns, 'optional')
    vehicle_types = validate_and_convert_data_types(vehicle_types, vehicle_types_mandatory_columns, 'mandatory')
    shipments = validate_and_convert_data_types(shipments, shipments_mandatory_columns, 'mandatory')
    if not shipments is None:
        shipments = validate_and_convert_data_types(shipments, shipemnts_optional_columns, 'optional')
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

def reverse_transport_optimization(locations: pd.DataFrame, vehicle_types: pd.DataFrame, shipments: pd.DataFrame, parameters: Dict, api_key: str, save_scenario = {}) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
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
        - maxCapacityLoadingMeter (number):  The maximum number of pallets that can be loaded by a vehicle of the corresponding vehicle type.
        - fixedCosts (number): The fixed costs per vehicle in case of usage. 
        - costsPerStop (number): The costs per vehicle stop.
        - costsPerKm (number): The costs per distance unit. 

     shipments (pd.DataFrame): DataFrame containing shipments information.
        Columns:
        - name (str): The name of the order. 
        - sender (str): Sender id of the shipment.
        - senderServiceTime (float): Service time needed on the pickup location of the shipment.
        - earliestPickupTime (str): Start of the pickup time window per shipment.
        - latestPickupTime (str): End of the pickup time window per shipment.
        - recipient (str): Recipient id of the shipment.
        - recipientServiceTime (float): Service time needed on the delivery location of the shipment.
        - earliestDeliveryTime (str): Start of the delivery time window per shipment.
        - latestDeliveryTime (str): End of the delivery time window per shipment.
        - weight (number): The weight of the shipment. 
        - volume (number): The volume of the shipment.
        - loadingMeter (number): The number of pallets of the shipment.
        - opportunityCosts (number): External costs for shipment.
        - vehicleType (str): All valid vehicle types for the order separated by semicolon.   

    parameters (Dict): Dictionary containing parameters durationUnit and distanceUnit.

    api_key (str): Log-hub API key for accessing the milkrun optimization service.

    save_scenario (dict): A dictionary containg information about saving scenario, empty by default. Allowed key vales are
                        'saveScenario' (boolean), 'overwriteScenario' (boolean), 'workspaceId' (str) and
                        'scenarioName' (str).

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Four pandas DataFrames containing transport overview, trasnport details, dropped shipments and input map routes with coordinates information. Returns None if the process fails.
    """

    # Define expected columns and data types for each DataFrame
    locations_mandatory_columns = {
        'name': 'str', 'latitude': 'float', 'longitude': 'float'
    }

    vehicle_types_mandatory_columns = {
        'type': 'str', 'availableVehicles': 'float',  'startLocation': 'str', 'endLocation': 'str', 'averageSpeed': 'float', 'maxRouteStops': 'float', 'maxRouteLength': 'float', 'maxRouteDuration': 'float', 'maxCapacityWeight': 'float', 'maxCapacityVolume': 'float', 'maxCapacityLoadingMeter': 'float', 'fixedCosts': 'float', 'costsPerStop': 'float', 'costsPerKm': 'float'
    }   
    shipments_mandatory_columns = {
        'name': 'str', 'sender': 'str', 'senderServiceTime': 'float', 'earliestPickupTime': 'str', 'latestPickupTime': 'str', 'recipient': 'str', 'recipientServiceTime': 'float', 'earliestDeliveryTime': 'str',  'latestDeliveryTime': 'str', 'weight': 'float', 'opportunityCosts': 'float'
    }
    shipemnts_optional_columns = {
        'vehicleType': 'str'
    }
    shipments_optional_floats = ['volume', 'loadingMeter']

    # Perform validation and conversion for each DataFrame
    locations = validate_and_convert_data_types(locations, locations_mandatory_columns, 'mandatory')
    vehicle_types = validate_and_convert_data_types(vehicle_types, vehicle_types_mandatory_columns, 'mandatory')
    shipments = validate_and_convert_data_types(shipments, shipments_mandatory_columns, 'mandatory')
    if not shipments is None:
        shipments = validate_and_convert_data_types(shipments, shipemnts_optional_columns, 'optional')
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
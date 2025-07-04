<p align="center">
  <img src="assets/log-hub-github-header.png" alt="Header Image" width="980"/>
</p>


# Log-hub Python API library

[![PyPI version](https://badge.fury.io/py/pyloghub.svg)](https://pypi.org/project/pyloghub/)

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Setting Up Python Environment](#setting-up-python-environment)
  - [Installing `pyloghub` Package](#installing-pyloghub-package)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Functionalities](#available-functionalities)
- [Contact Us](#contact-us)
- [License](#license)

## Introduction

The `pyloghub` package provides convinient access to various Log-hub API services for Supply Chain Visualization, Network Design Optimization, and Transport Optimization as well as access to the Log-hub platform data.

### Prerequisites

- Python 3.10 or later recommended
- Pip (Python package manager)
- Log-hub API key
- Supply Chain APPS PRO subscription

## Installation

### Setting Up Python Environment

#### Recommended Python Version

Python 3.10 or later is recommended for optimal performance and compatibility.

#### Optional: Setting Up a Virtual Environment

A virtual environment allows you to manage Python packages for different projects separately.

1. **Create a Virtual Environment**:
   - **Windows**: 
     ```bash
     python -m venv loghub_env
     ```
   - **macOS/Linux**: 
     ```bash
     python3 -m venv loghub_env
     ```

2. **Activate the Virtual Environment**:
   - **Windows**: 
     ```bash
     .\loghub_env\Scripts\activate
     ```
   - **macOS/Linux**: 
     ```bash
     source loghub_env/bin/activate
     ```

   Deactivate with `deactivate` when done.

### Installing `pyloghub` Package

Within the environment, install the package using:

```bash
pip install pyloghub
```

## Configuration

### Obtaining an API Key

1. Sign up or log in at [Log-hub Account Integration](https://production.supply-chain-apps.log-hub.com/sca/account/integration).
2. Obtain your API key.

### Setting Up Your Environment

Securely store your API key for use in your Python scripts or as an environment variable.

```python
api_key = "YOUR API KEY"
```
## Usage

### Sample Code: Reverse Distance Calculation

This example demonstrates using the Reverse Distance Calculation feature:

1. **Import Functions**:
   ```python
   from pyloghub.distance_calculation import reverse_distance_calculation, reverse_distance_calculation_sample_data
   ```

2. **Load Sample Data**:
   ```python
   sample_data = reverse_distance_calculation_sample_data()
   geocode_data_df = sample_data['geocode_data']
   parameters = sample_data['parameters']
   ```

3. **Perform Calculation**:
   ```python
   reverse_distance_result_df = reverse_distance_calculation(geocode_data_df, parameters, 'YOUR_API_KEY')
   ```

   Replace `'YOUR_API_KEY'` with your actual Log-hub API key.

4. **View Results**:
   ```python
   print(reverse_distance_result_df)
   ```

## Available Functionalities

### Overview

`pyloghub` offers a suite of functionalities to enhance your supply chain management processes. Below is a quick guide to the available features and sample usage for each.

<p align="left">
  <img src="examples\assets\geocoding.png" alt="Geocoding"  width="980"/>
</p>

#### Forward Geocoding
Convert addresses to geographic coordinates.

```python
from pyloghub.geocoding import forward_geocoding, forward_geocoding_sample_data

sample_data = forward_geocoding_sample_data()
addresses_df = sample_data['addresses']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

geocoded_df = forward_geocoding(addresses_df, api_key, save_scenario, show_buttons=True)
geocoded_df.head()
```

#### Reverse Geocoding
Convert geographic coordinates to addresses.

```python
from pyloghub.geocoding import reverse_geocoding, reverse_geocoding_sample_data

sample_data = reverse_geocoding_sample_data()
geocodes_df = sample_data['geocodes']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

reverse_geocoding_result_df = reverse_geocoding(geocodes_df, api_key, save_scenario, show_buttons=True)
reverse_geocoding_result_df.head()
```

<p align="left">
  <img src="examples\assets\distance_calculation.png" alt="Distance Calculation"  width="980"/>
</p>

#### Forward Distance Calculation
Calculate distances based on address data.

```python
from pyloghub.distance_calculation import forward_distance_calculation, forward_distance_calculation_sample_data

sample_data = forward_distance_calculation_sample_data()
address_data_df = sample_data['address_data']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME" 
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

forward_distance_calculation_result_df = forward_distance_calculation(address_data_df, parameters, api_key, save_scenario, show_buttons=True)
forward_distance_calculation_result_df.head()
```


#### Reverse Distance Calculation
Calculate distances based on geocode data.

```python
from pyloghub.distance_calculation import reverse_distance_calculation, reverse_distance_calculation_sample_data

sample_data = reverse_distance_calculation_sample_data()
geocode_data_df = sample_data['geocode_data']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME" 
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

reverse_distance_calculation_df = reverse_distance_calculation(geocode_data_df, parameters, api_key, save_scenario, show_buttons=True)
reverse_distance_calculation_df.head()
```

#### Forward Distance Calculation With Extra Details
Calculate distances based on addresses and getting additional details about the road between start and end point.
```python
from pyloghub.distance_calculation_with_extra_details import forward_distance_calculation_with_extra_details, forward_distance_calculation_with_extra_details_sample_data
from IPython.display import display

sample_data = forward_distance_calculation_with_extra_details_sample_data()
address_data_df = sample_data['address_data']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME" 
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

forward_distance_calculation_result_df, additional_details_df = forward_distance_calculation_with_extra_details(address_data_df, parameters, api_key, save_scenario, show_buttons=True)
display(forward_distance_calculation_result_df.head())
display(additional_details_df.head())
```

#### Reverse Distance Calculation With Extra Details
Calculate distances based on coordinates and getting additional details about the road between start and end point.
```python
from pyloghub.distance_calculation_with_extra_details import reverse_distance_calculation_with_extra_details, reverse_distance_calculation_with_extra_details_sample_data
from IPython.display import display

sample_data = reverse_distance_calculation_with_extra_details_sample_data()
address_data_df = sample_data['geocode_data']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME" 
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

reverse_distance_calculation_result_df, additional_details_df = reverse_distance_calculation_with_extra_details(address_data_df, parameters, api_key, save_scenario, show_buttons=True)
display(reverse_distance_calculation_result_df.head())
display(additional_details_df.head())
```


<p align="left">
  <img src="examples\assets\isochrone.png" alt="Isochrone"  width="980"/>
</p>

#### Forward Isochrone
Determine the areas that can be rached within a certain amount of time or distance from the starting location with the given address.

```python
from pyloghub.isochrone import forward_isochrone, forward_isochrone_sample_data

sample_data = forward_isochrone_sample_data()
addresses_df = sample_data['addresses']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME" 
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

reachable_areas_df = forward_isochrone(addresses_df, parameters, api_key, save_scenario, show_buttons=True)
reachable_areas_df.head()
```

#### Reverse Isochrone
Determine the areas that can be rached within a certain amount of time or distance from the starting location with the given coordinates.

```python
from pyloghub.isochrone import reverse_isochrone, reverse_isochrone_sample_data

sample_data = reverse_isochrone_sample_data()
coordinates_df = sample_data['coordinates']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME" 
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

reachable_areas_df = reverse_isochrone(coordinates_df, parameters, api_key, save_scenario, show_buttons=True)
reachable_areas_df.head()
```

<p align="left">
  <img src="examples\assets\isochrone_plus.png" alt="Isochrone Plus"  width="980"/>
</p>

#### Forward Isochrone Plus
Determine the areas that can be rached within a certain amount of time or distance from the starting location with the given address, using the additional parameters for calculating the isochrones.

```python
from pyloghub.isochrone_plus import forward_isochrone_plus, forward_isochrone_plus_sample_data
from IPython.display import display

sample_data = forward_isochrone_plus_sample_data()
addresses_df = sample_data['addresses']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME" 
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

geocoded_data_df, reachable_areas_df = forward_isochrone_plus(addresses_df, parameters, api_key, save_scenario, show_buttons=True)
display(geocoded_data_df.head())
display(reachable_areas_df.head())
```

#### Reverse Isochrone Plus
Determine the areas that can be rached within a certain amount of time or distance from the starting location with the given coordinates, using the additional parameters for calculating the isochrones.

```python
from pyloghub.isochrone_plus import reverse_isochrone_plus, reverse_isochrone_plus_sample_data
from IPython.display import display

sample_data = reverse_isochrone_plus_sample_data()
coordinates_df = sample_data['coordinates']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['scenarioName'] = "YOUR SCENARIO NAME" 
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"

geocoded_data_df, reachable_areas_df = reverse_isochrone_plus(coordinates_df, parameters, api_key, save_scenario, show_buttons=True)
display(geocoded_data_df.head())
display(reachable_areas_df.head())
```

<p align="left">
  <img src="examples\assets\supply_chain_maps.png" alt="Supply Chain Map"  width="980"/>
</p>

#### Creating a Supply Chain Map
In order to create a Supply Chain Map, a Workspace Id is required. Please, go to the platform and click on the "three dots" next to the workspace in which you want to save the map. Click on "Copy Workspace Id" and paste the corresponding workspace id instead of "YOUR WORKSPACE ID". If there are no workspaces, please create one using the GUI.

#### Forward Supply Chain Map Locations
Creating a map of locations based on their addresses.

```python
from pyloghub.supply_chain_map_locations import forward_supply_chain_map_locations_sample_data, forward_supply_chain_map_locations

sample_data = forward_supply_chain_map_locations_sample_data()
address_data_df = sample_data['addresses']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

locations_df = forward_supply_chain_map_locations(address_data_df, api_key, save_scenario, show_buttons=True)
locations_df.head()
```

#### Reverse Supply Chain Map Locations
Creating a map of locations based on their geocodes.

```python
from pyloghub.supply_chain_map_locations import reverse_supply_chain_map_locations_sample_data, reverse_supply_chain_map_locations

sample_data = reverse_supply_chain_map_locations_sample_data()
coordinates_df = sample_data['coordinates']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

locations_df = reverse_supply_chain_map_locations(coordinates_df, api_key, save_scenario, show_buttons=True)
locations_df.head()
```

#### Forward Supply Chain Map Relations
Creating a map of relations based on the addresses.

```python
from pyloghub.supply_chain_map_relations import forward_supply_chain_map_relations_sample_data, forward_supply_chain_map_relations

sample_data = forward_supply_chain_map_relations_sample_data()
address_data_df = sample_data['addresses']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

relations_df = forward_supply_chain_map_relations(address_data_df, parameters, api_key, save_scenario, show_buttons=True)
relations_df.head()
```

#### Reverse Supply Chain Map Relations
Creating a map of relations based on the coordinates.

```python
from pyloghub.supply_chain_map_relations import reverse_supply_chain_map_relations_sample_data, reverse_supply_chain_map_relations

sample_data = reverse_supply_chain_map_relations_sample_data()
coordinates_df = sample_data['coordinates']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

relations_df = reverse_supply_chain_map_relations(coordinates_df, parameters, api_key, save_scenario, show_buttons=True)
relations_df.head()
```

#### Forward Supply Chain Map Areas
Creating a map based on the given areas information.

```python
from pyloghub.supply_chain_map_areas import forward_supply_chain_map_areas_sample_data, forward_supply_chain_map_areas

sample_data = forward_supply_chain_map_areas_sample_data()
areas_df = sample_data['areas']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

areas_output_df = forward_supply_chain_map_areas(areas_df, parameters, api_key, save_scenario, show_buttons=True)
areas_output_df.head()
```

#### Reverse Supply Chain Map Polyline
Visualizing polylines on a map based on the given coordinates.

```python
from pyloghub.supply_chain_map_polyline import reverse_supply_chain_map_polyline_sample_data, reverse_supply_chain_map_polyline

sample_data = reverse_supply_chain_map_polyline_sample_data()
polyline_df = sample_data['polyline']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

polyline_output_df = reverse_supply_chain_map_polyline(polyline_df, api_key, save_scenario, show_buttons=True)
polyline_output_df.head()
```

#### Forward Supply Chain Map Routes
Creating a route map based on the addresses.

```python
from pyloghub.supply_chain_map_routes import forward_supply_chain_map_routes_sample_data, forward_supply_chain_map_routes

sample_data = forward_supply_chain_map_routes_sample_data()
addresses_df = sample_data['addresses']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

routes_df = forward_supply_chain_map_routes(addresses_df, parameters, api_key, save_scenario, show_buttons = True)
routes_df.head()
```

#### Reverse Supply Chain Map Routes
Creating a route map based on the coordinates.

```python
from pyloghub.supply_chain_map_routes import reverse_supply_chain_map_routes_sample_data, reverse_supply_chain_map_routes

sample_data = reverse_supply_chain_map_routes_sample_data()
coordinates_df = sample_data['coordinates']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

routes_df = reverse_supply_chain_map_routes(coordinates_df, parameters, api_key, save_scenario, show_buttons=True)
routes_df.head()
```

#### Forward Supply Chain Map Sea Routes
Creates a map of sea routes based on the given UN/LOCODEs.

```python
from pyloghub.supply_chain_map_sea_routes import forward_supply_chain_map_sea_routes_sample_data, forward_supply_chain_map_sea_routes

sample_data = forward_supply_chain_map_sea_routes_sample_data()
sea_routes_df = sample_data['addresses']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

sea_routes_output_df = forward_supply_chain_map_sea_routes(sea_routes_df, parameters, api_key, save_scenario, show_buttons = True)
sea_routes_output_df.head()
```

#### Reverse Supply Chain Map Sea Routes
Creating a sea routes map based on the given coordinates. 

```python
from pyloghub.supply_chain_map_sea_routes import reverse_supply_chain_map_sea_routes_sample_data, reverse_supply_chain_map_sea_routes

sample_data = reverse_supply_chain_map_sea_routes_sample_data()
sea_routes_df = sample_data['coordinates']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

sea_routes_output_df = reverse_supply_chain_map_sea_routes(sea_routes_df, parameters, api_key, save_scenario, show_buttons=True)
sea_routes_output_df.head()
```

<p align="left">
  <img src="examples\assets\center_of_gravity.png" alt="Center of Gravity"  width="980"/>
</p>

#### Forward Center of Gravity
Determine optimal facility locations based on addresses.

```python
from IPython.display import display
from pyloghub.center_of_gravity import forward_center_of_gravity, forward_center_of_gravity_sample_data

sample_data = forward_center_of_gravity_sample_data()
addresses_df = sample_data['addresses']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

assigned_addresses_df, centers_df = forward_center_of_gravity(addresses_df, parameters, api_key, save_scenario, show_buttons=True)

display(assigned_addresses_df.head())
display(centers_df.head())
```

#### Reverse Center of Gravity
Determine optimal facility locations based on coordinates.

```python
from IPython.display import display
from pyloghub.center_of_gravity import reverse_center_of_gravity, reverse_center_of_gravity_sample_data

sample_data = reverse_center_of_gravity_sample_data()
coordinates_df = sample_data['coordinates']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

assigned_geocodes_df, centers_df = reverse_center_of_gravity(coordinates_df, parameters, api_key, save_scenario, show_buttons=True)
display(assigned_geocodes_df.head())
display(centers_df.head())
```

<p align="left">
  <img src="examples\assets\fixed_center_of_gravity.png" alt="Fixed Center of Gravity"  width="980"/>
</p>

#### Forward Fixed Center of Gravity
Calculating the optimal locations for new warehouses based on the address location of customers, their respective weights and existing warehouses.

```python
from IPython.display import display
from pyloghub.fixed_center_of_gravity import forward_fixed_center_of_gravity_sample_data, forward_fixed_center_of_gravity

sample_data = forward_fixed_center_of_gravity_sample_data()
customers_df = sample_data['customers']
fixed_centers_df = sample_data['fixedCenters']
parameters =sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

assigned_geocodes_df, centers_df = forward_fixed_center_of_gravity(customers_df, fixed_centers_df, parameters, api_key, save_scenario, show_buttons=True)
display(assigned_geocodes_df.head())
display(centers_df.head())
```

#### Reverse Fixed Center of Gravity
Calculating the optimal location for new warehouses based on the geocode of customers, their respective weights and existing warehouses.

```python
from IPython.display import display
from pyloghub.fixed_center_of_gravity import reverse_fixed_center_of_gravity_sample_data, reverse_fixed_center_of_gravity

sample_data = reverse_fixed_center_of_gravity_sample_data()
customers_df = sample_data['customers']
fixed_centers_df = sample_data['fixedCenters']
parameters =sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

assigned_geocodes_df, centers_df = reverse_fixed_center_of_gravity(customers_df, fixed_centers_df, parameters, api_key, save_scenario, show_buttons=True)
display(assigned_geocodes_df.head())
display(centers_df.head())
```

<p align="left">
  <img src="examples\assets\center_of_gravity_plus.png" alt="Center of Gravity Plus"  width="980"/>
</p>

#### Forward Center of Gravity Plus
Calculating the optimal location for new warehouses given the address location of customers and their respective weights, volumes and revenues.

```python
from IPython.display import display
from pyloghub.center_of_gravity_plus import forward_center_of_gravity_plus_sample_data, forward_center_of_gravity_plus

sample_data = forward_center_of_gravity_plus_sample_data()
addresses_df = sample_data['addresses']
parameters =sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

assigned_addresses_df, centers_df = forward_center_of_gravity_plus(addresses_df, parameters, api_key, save_scenario, show_buttons = True)
display(assigned_addresses_df.head())
display(centers_df.head())
```

#### Reverse Center of Gravity Plus
Calculating the optimal location for new warehouses based on the coordinates of customers and their respective weights, volumes and revenues.

```python
from IPython.display import display
from pyloghub.center_of_gravity_plus import reverse_center_of_gravity_plus_sample_data, reverse_center_of_gravity_plus

sample_data = reverse_center_of_gravity_plus_sample_data()
coordinates_df = sample_data['coordinates']
parameters =sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

assigned_geocodes_df, centers_df = reverse_center_of_gravity_plus(coordinates_df, parameters, api_key, save_scenario, show_buttons=True)
display(assigned_geocodes_df.head())
display(centers_df.head())
```

<p align="left">
  <img src="examples\assets\advanced_center_of_gravity.png" alt="Advanced Center of Gravity"  width="980"/>
</p>

#### Forward Advanced Center of Gravity
Calculating the optimal location for new warehouses given the address location of customers, their respective weights and product groups they require, as well as sources of the product groups.
```python
from IPython.display import display
from pyloghub.advanced_center_of_gravity import forward_advanced_center_of_gravity_sample_data, forward_advanced_center_of_gravity

sample_data = forward_advanced_center_of_gravity_sample_data()
customers_df = sample_data['customers']
sources_df = sample_data['sources']
fixed_centers_df = sample_data['fixedCenters']
product_groups_df = sample_data['productGroups']
parameters =sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

assigned_centers_df, inbound_df, outbound_df = forward_advanced_center_of_gravity(customers_df, sources_df, fixed_centers_df, product_groups_df, parameters, api_key, save_scenario, show_buttons=True)
display(assigned_centers_df.head())
display(inbound_df.head())
display(outbound_df.head())
```

#### Reverse Advanced Center of Gravity
Calculating the optimal location for new warehouses given the coordinates of customers, their respective weights and product groups they require, as well as sources of the product groups.

```python
from IPython.display import display
from pyloghub.advanced_center_of_gravity import reverse_advanced_center_of_gravity_sample_data, reverse_advanced_center_of_gravity

sample_data = reverse_advanced_center_of_gravity_sample_data()
customers_df = sample_data['customers']
sources_df = sample_data['sources']
fixed_centers_df = sample_data['fixedCenters']
product_groups_df = sample_data['productGroups']
parameters =sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

assigned_centers_df, inbound_df, outbound_df = reverse_advanced_center_of_gravity(customers_df, sources_df, fixed_centers_df, product_groups_df, parameters, api_key, save_scenario, show_buttons=True)
display(assigned_centers_df.head())
display(inbound_df.head())
display(outbound_df.head())
```

<p align="left">
  <img src="examples\assets\nearest_warehouses.png" alt="Nearest Warehouses"  width="980"/>
</p>

#### Forward Nearest Warehouses
Calculating a given number of the nearest warehouses from a customer address.

```python
from IPython.display import display
from pyloghub.nearest_warehouses import forward_nearest_warehouses_sample_data, forward_nearest_warehouses

sample_data = forward_nearest_warehouses_sample_data()
warehouses_df = sample_data['warehouses']
customers_df = sample_data['customers']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

nearest_warehouses_df, unassigned_df = forward_nearest_warehouses(warehouses_df, customers_df, parameters, api_key, save_scenario, show_buttons=True)
display(nearest_warehouses_df.head())
display(unassigned_df.head())
```

#### Reverse Nearest Warehouses
Calculating a given number of the nearest warehouses from a customer coordinates.

```python
from IPython.display import display
from pyloghub.nearest_warehouses import reverse_nearest_warehouses_sample_data, reverse_nearest_warehouses

sample_data = reverse_nearest_warehouses_sample_data()
warehouses_df = sample_data['warehouses']
customers_df = sample_data['customers']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

nearest_warehouses_df, unassigned_df = reverse_nearest_warehouses(warehouses_df, customers_df, parameters, api_key, save_scenario, show_buttons=True)
display(nearest_warehouses_df.head())
display(unassigned_df.head())
```

<p align="left">
  <img src="examples\assets\network_design_plus.png" alt="Network Design Plus"  width="980"/>
</p>

#### Forward Network Design Plus
Finds the optimal number and locations of warehouses based on transport, handling and fixed warehouse costs.

```python
from IPython.display import display
from pyloghub.network_design_plus import forward_network_design_plus_sample_data, forward_network_design_plus

sample_data = forward_network_design_plus_sample_data()
factories_df = sample_data['factories']
warehouses_df = sample_data['warehouses']
customers_df = sample_data['customers']
product_segments_df = sample_data['productSegments']
transport_costs_df = sample_data['transportCosts']
transport_costs_rules_df = sample_data['transportCostsRules']
stepwise_function_weight_df = sample_data['stepwiseCostFunctionWeight']
stepwise_function_volume_df = sample_data['stepwiseCostFunctionVolume']
distance_limits_df = sample_data['distanceLimits']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

open_warehouses, factory_assignement, customer_assignement, solution_kpis = forward_network_design_plus(factories_df, warehouses_df, customers_df, product_segments_df, transport_costs_df, transport_costs_rules_df, stepwise_function_weight_df, stepwise_function_volume_df, distance_limits_df, parameters, api_key, save_scenario, show_buttons=True)
display(open_warehouses.head())
display(factory_assignement.head())
display(customer_assignement.head())
display(solution_kpis.head())
```

#### Reverse Network Design Plus
Finding the optimal number and locations of warehouses based on transport, handling and fixed warehouse costs.

```python
from IPython.display import display
from pyloghub.network_design_plus import reverse_network_design_plus_sample_data, reverse_network_design_plus

sample_data = reverse_network_design_plus_sample_data()
factories_df = sample_data['factories']
warehouses_df = sample_data['warehouses']
customers_df = sample_data['customers']
product_segments_df = sample_data['productSegments']
transport_costs_df = sample_data['transportCosts']
transport_costs_rules_df = sample_data['transportCostsRules']
stepwise_function_weight_df = sample_data['stepwiseCostFunctionWeight']
stepwise_function_volume_df = sample_data['stepwiseCostFunctionVolume']
distance_limits_df = sample_data['distanceLimits']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

open_warehouses, factory_assignement, customer_assignement, solution_kpis = reverse_network_design_plus(factories_df, warehouses_df, customers_df, product_segments_df, transport_costs_df, transport_costs_rules_df, stepwise_function_weight_df, stepwise_function_volume_df, distance_limits_df, parameters, api_key, save_scenario, show_buttons=True)
display(open_warehouses.head())
display(factory_assignement.head())
display(customer_assignement.head())
display(solution_kpis.head())
```

<p align="left">
  <img src="examples\assets\location_planning.png" alt="Location Planning"  width="980"/>
</p>

#### Forward Location Planning
Optimizing flows from the warehouses to the customers.

```python
from IPython.display import display
from pyloghub.location_planning import forward_location_planning_sample_data, forward_location_planning

sample_data = forward_location_planning_sample_data()
warehouses_df = sample_data['warehouses']
customers_df = sample_data['customers']
cost_adjustments_df = sample_data['costsAdjustments']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

open_warehouses, customer_assignement, solution_kpis = forward_location_planning(customers_df, warehouses_df, cost_adjustments_df, parameters, api_key, save_scenario, show_buttons=True)
display(open_warehouses.head())
display(customer_assignement.head())
display(solution_kpis.head())
```

#### Reverse Location Planning
Optimizing flows from the warehouses to the customers.

```python
from IPython.display import display
from pyloghub.location_planning import reverse_location_planning_sample_data, reverse_location_planning

sample_data = reverse_location_planning_sample_data()
warehouses_df = sample_data['warehouses']
customers_df = sample_data['customers']
cost_adjustments_df = sample_data['costsAdjustments']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

open_warehouses, customer_assignement, solution_kpis = reverse_location_planning(customers_df, warehouses_df, cost_adjustments_df, parameters, api_key, save_scenario, show_buttons=True)
display(open_warehouses.head())
display(customer_assignement.head())
display(solution_kpis.head())
```

<p align="left">
  <img src="examples\assets\milkrun_optimization.png" alt="Milkrun Optimization"  width="980"/>
</p>

#### Forward Milkrun Optimization
Calculate cost-optimal routes for inbound and outbound orders described with their addresses.

```python
from pyloghub.milkrun_optimization import forward_milkrun_optimization_sample_data, forward_milkrun_optimization
from IPython.display import display

sample_data = forward_milkrun_optimization_sample_data()
depots_df = sample_data['depots']
vehicle_types_df = sample_data['vehicleTypes']
pickup_and_delivery_df = sample_data['pickupAndDelivery']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

route_overview_df, route_details_df, external_orders_df, input_map_routes_df, input_map_routes_geocodes_df = forward_milkrun_optimization(depots_df, vehicle_types_df, pickup_and_delivery_df, parameters, api_key, save_scenario, show_buttons=True)

display(route_overview_df.head())
display(route_details_df.head())
display(external_orders_df.head())
display(input_map_routes_df.head())
display(input_map_routes_geocodes_df.head())
```

#### Reverse Milkrun Optimization
Calculate cost-optimal routes for inbound and outbound orders described with their coordinates.

```python
from pyloghub.milkrun_optimization import reverse_milkrun_optimization_sample_data, reverse_milkrun_optimization
from IPython.display import display

sample_data = reverse_milkrun_optimization_sample_data()
depots_df = sample_data['depots']
vehicle_types_df = sample_data['vehicleTypes']
pickup_and_delivery_df = sample_data['pickupAndDelivery']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

route_overview_df, route_details_df, external_orders_df, input_map_routes_geocodes_df = reverse_milkrun_optimization(depots_df, vehicle_types_df, pickup_and_delivery_df, parameters, api_key, save_scenario, show_buttons=True)

display(route_overview_df.head())
display(route_details_df.head())
display(external_orders_df.head())
display(input_map_routes_geocodes_df.head())
```

<p align="left">
  <img src="examples\assets\milkrun_optimization_plus.png" alt="Milkrun Optimization Plus"  width="980"/>
</p>

#### Forward Milkrun Optimization Plus
Calculating optimal routes for multiple days shipments by taking into consideration constraints such as customer time windows, detailed vehicle, and capacity profiles.

```python
from IPython.display import display
from pyloghub.milkrun_optimization_plus import forward_milkrun_optimization_plus_sample_data, forward_milkrun_optimization_plus

sample_data = forward_milkrun_optimization_plus_sample_data()
depots_df = sample_data['depots']
vehicles_df = sample_data['vehicles']
jobs_df = sample_data['jobs']
time_window_profiles_df = sample_data['timeWindowProfiles']
breaks_df = sample_data['breaks']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

route_overview_df, route_details_df, external_orders_df = forward_milkrun_optimization_plus(depots_df, vehicles_df, jobs_df, time_window_profiles_df, breaks_df, parameters, api_key, save_scenario, show_buttons=True)
display(route_overview_df.head())
display(route_details_df.head())
display(external_orders_df.head())
```

#### Reverse Milkrun Optimization Plus
Calculating optimal routes for multiple days shipments by taking into consideration constraints such as customer time windows, detailed vehicle, and capacity profiles.

```python
from IPython.display import display
from pyloghub.milkrun_optimization_plus import reverse_milkrun_optimization_plus_sample_data, reverse_milkrun_optimization_plus

sample_data = reverse_milkrun_optimization_plus_sample_data()
depots_df = sample_data['depots']
vehicles_df = sample_data['vehicles']
jobs_df = sample_data['jobs']
time_window_profiles_df = sample_data['timeWindowProfiles']
breaks_df = sample_data['breaks']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

route_overview_df, route_details_df, external_orders_df = reverse_milkrun_optimization_plus(depots_df, vehicles_df, jobs_df, time_window_profiles_df, breaks_df, parameters, api_key, save_scenario, show_buttons=True)
display(route_overview_df.head())
display(route_details_df.head())
display(external_orders_df.head())
```

<p align="left">
  <img src="examples\assets\transport_optimization.png" alt="Transport Optimization"  width="980"/>
</p>

#### Forward Transport Optimization
Assign shipments with corresponding addresses to available vehicles in an optimal way.

```python
from IPython.display import display
from pyloghub.transport_optimization import forward_transport_optimization, forward_transport_optimization_sample_data

sample_data = forward_transport_optimization_sample_data()
locations_df = sample_data['locations']
vehicle_types_df = sample_data['vehicleTypes']
shipments_df = sample_data['shipments']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

route_overview_df, route_details_df, external_orders_df, input_map_routes_df, input_map_routes_geocodes_df = forward_transport_optimization(locations_df, vehicle_types_df, shipments_df, parameters, api_key, save_scenario, show_buttons=True)
display(route_overview_df.head())
display(route_details_df.head())
display(external_orders_df.head())
display(input_map_routes_df.head())
display(input_map_routes_geocodes_df.head())
```

#### Reverse Transport Optimization
Assign shipments with corresponding coordinates to available vehicles in an optimal way.

```python
from IPython.display import display
from pyloghub.transport_optimization import reverse_transport_optimization, reverse_transport_optimization_sample_data

sample_data = reverse_transport_optimization_sample_data()
locations_df = sample_data['locations']
vehicle_types_df = sample_data['vehicleTypes']
shipments_df = sample_data['shipments']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

route_overview_df, route_details_df, external_orders_df, input_map_routes_geocodes_df = reverse_transport_optimization(locations_df, vehicle_types_df, shipments_df, parameters, api_key, save_scenario, show_buttons=True)
display(route_overview_df.head())
display(route_details_df.head())
display(external_orders_df.head())
display(input_map_routes_geocodes_df.head())
```

<p align="left">
  <img src="examples\assets\transport_optimization_plus.png" alt="Transport Optimization Plus"  width="980"/>
</p>

#### Forward Transport Optimization Plus
Calculating optimal routes for multiple days shipments by taking into consideration constraints such as customer time windows, detailed vehicle, and capacity profiles.

```python
from IPython.display import display
from pyloghub.transport_optimization_plus import forward_transport_optimization_plus, forward_transport_optimization_plus_sample_data

sample_data = forward_transport_optimization_plus_sample_data()
vehicles_df = sample_data['vehicles']
shipments_df = sample_data['shipments']
timeWindowProfiles_df = sample_data['timeWindowProfiles']
breaks_df = sample_data['breaks']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

route_overview_df, route_details_df, external_orders_df = forward_transport_optimization_plus(vehicles_df, shipments_df, timeWindowProfiles_df, breaks_df, parameters, api_key, save_scenario, show_buttons=True)
display(route_overview_df.head())
display(route_details_df.head())
display(external_orders_df.head())
```

#### Reverse Transport Optimization Plus
Calculating optimal routes for multiple days shipments by taking into consideration constraints such as customer time windows, detailed vehicle, and capacity profiles.

```python
from IPython.display import display
from pyloghub.transport_optimization_plus import reverse_transport_optimization_plus, reverse_transport_optimization_plus_sample_data

sample_data = reverse_transport_optimization_plus_sample_data()
vehicles_df = sample_data['vehicles']
shipments_df = sample_data['shipments']
timeWindowProfiles_df = sample_data['timeWindowProfiles']
breaks_df = sample_data['breaks']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

route_overview_df, route_details_df, external_orders_df = reverse_transport_optimization_plus(vehicles_df, shipments_df, timeWindowProfiles_df, breaks_df, parameters, api_key, save_scenario, show_buttons=True)
display(route_overview_df.head())
display(route_details_df.head())
display(external_orders_df.head())
```

<p align="left">
  <img src="examples\assets\shipment_analyzer.png" alt="Shipment Analyzer"  width="980"/>
</p>

#### Forward Shipment Analyzer
Analyzing and optimizing shipment costs and operations.

```python
from IPython.display import display
from pyloghub.shipment_analyzer import forward_shipment_analyzer, forward_shipment_analyzer_sample_data

sample_data = forward_shipment_analyzer_sample_data()
shipments_df = sample_data['shipments']
transport_costs_adjustments_df = sample_data['transportCostAdjustments']
consolidation_df = sample_data['consolidation']
surcharges_df = sample_data['surcharges']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

shipments_analysis_df, transports_analysis_df = forward_shipment_analyzer(shipments_df, transport_costs_adjustments_df, consolidation_df, surcharges_df, parameters, api_key, save_scenario, show_buttons=True)

display(shipments_analysis_df.head())
display(transports_analysis_df.head())
```

#### Reverse Shipment Analyzer
Analyzing and optimizing shipment costs and operations.

```python
from IPython.display import display
from pyloghub.shipment_analyzer import reverse_shipment_analyzer, reverse_shipment_analyzer_sample_data

sample_data = reverse_shipment_analyzer_sample_data()
shipments_df = sample_data['shipments']
transport_costs_adjustments_df = sample_data['transportCostAdjustments']
consolidation_df = sample_data['consolidation']
surcharges_df = sample_data['surcharges']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

shipments_analysis_df, transports_analysis_df = reverse_shipment_analyzer(shipments_df, transport_costs_adjustments_df, consolidation_df, surcharges_df, parameters, api_key, save_scenario, show_buttons=True)

display(shipments_analysis_df.head())
display(transports_analysis_df.head())
```

<p align="left">
  <img src="examples\assets\freight_matrix_plus.png" alt="Freight Matrix Plus"  width="980"/>
</p>

#### Forward Freight Matrix Plus
Evaluate shipments with costs based on your own freight cost matrices. The following matrix types are supported:

* Absolute weight distance matrix
* Relative weight distance matrix
* Absolute weight zone matrix
* Relative weight zone matrix
* Zone zone matrix
* Absolute weight zone distance matrix
* Relative weight zone distance matrix

```python
from pyloghub.freight_matrix_plus import forward_freight_matrix_plus, forward_freight_matrix_plus_sample_data

sample_data = forward_freight_matrix_plus_sample_data()
shipments_df = sample_data['shipments']
matrix_id = "YOUR FREIGHT MATRIX ID"

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

evaluated_shipments_df = forward_freight_matrix_plus(shipments_df, matrix_id, api_key, save_scenario, show_buttons=True)
evaluated_shipments_df.head()
```

#### Reverse Freight Matrix
Evaluating shipments with costs based on your own freight cost matrices. Supported matrix types are the same as in the forward version.

```from pyloghub.freight_matrix_plus import reverse_freight_matrix_plus, reverse_freight_matrix_plus_sample_data

sample_data = reverse_freight_matrix_plus_sample_data()
shipments_df = sample_data['shipments']
matrix_id = "YOUR FREIGHT MATRIX ID"

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

evaluated_shipments_df = reverse_freight_matrix_plus(shipments_df, matrix_id, api_key, save_scenario, show_buttons=True)
evaluated_shipments_df.head()
```

You can create a freight matrix on the Log-hub Platform. Therefore, please create a workspace and click within the workspace on "Create Freight Matrix". There you can provide the matrix a name, select the matrix type and define all other parameters. 
To get the matrix id, please click on the "gear" icon. There you can copy & paste the matrix id that is needed in your API request.

<p align="left">
  <img src="examples\assets\CO2_emissions.png" alt="CO2 Emissions"  width="980"/>
</p>

#### Forward CO2 Emissions Road
Calculating a CO2 footprint based on your shipments transported by road.

```python
from IPython.display import display
from pyloghub.freight_shipment_emissions_road import forward_freight_shipment_emissions_road_sample_data, forward_freight_shipment_emissions_road

sample_data = forward_freight_shipment_emissions_road_sample_data()
addresses_df = sample_data['addresses']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

freight_emissions_df, not_evaluated_df = forward_freight_shipment_emissions_road(addresses_df, parameters, api_key, save_scenario, show_buttons=True)
display(freight_emissions_df.head())
display(not_evaluated_df.head())
```

#### Reverse CO2 Emissions Road
Calculating a CO2 footprint based on your shipments transported by road.

```python
from IPython.display import display
from pyloghub.freight_shipment_emissions_road import reverse_freight_shipment_emissions_road_sample_data, reverse_freight_shipment_emissions_road

sample_data = reverse_freight_shipment_emissions_road_sample_data()
coordinates_df = sample_data['coordinates']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

freight_emissions_df, not_evaluated_df = reverse_freight_shipment_emissions_road(coordinates_df, parameters, api_key, save_scenario, show_buttons=True)
display(freight_emissions_df.head())
display(not_evaluated_df.head())
```

#### CO2 Emissions Air
Calculating a CO2 footprint based on your shipments transported by air.

```python
from pyloghub.freight_shipment_emissions_air import forward_freight_shipment_emissions_air_sample_data, forward_freight_shipment_emissions_air

sample_data = forward_freight_shipment_emissions_air_sample_data()
iata_codes_df = sample_data['iataCodes']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

freight_emissions_df = forward_freight_shipment_emissions_air(iata_codes_df, parameters, api_key, save_scenario, show_buttons=True)
freight_emissions_df.head()
```

#### CO2 Emissions Sea
Calculating a CO2 footprint based on your shipments transported by sea.

```python
from pyloghub.freight_shipment_emissions_sea import forward_freight_shipment_emissions_sea_sample_data, forward_freight_shipment_emissions_sea

sample_data = forward_freight_shipment_emissions_sea_sample_data()
un_locodes_df = sample_data['unLocodes']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

freight_emissions_df = forward_freight_shipment_emissions_sea(un_locodes_df, parameters, api_key, save_scenario, show_buttons=True)
freight_emissions_df.head()
```

<p align="left">
  <img src="examples\assets\demand_forecasting.png" alt="Demand Forecasting"  width="980"/>
</p>

#### Demand Forecasting
Predicting future demand for your products based on the past demand data.

```python
from pyloghub.demand_forecasting import demand_forecasting_sample_data, demand_forecasting

sample_data = demand_forecasting_sample_data()
past_demand_data_df = sample_data['pastDemandData']
future_impact_factors_df = sample_data['futureImpactFactors']
sku_parameters_df = sample_data['skuParameters']

prediction_df = demand_forecasting(past_demand_data_df, future_impact_factors_df, sku_parameters_df, api_key)
prediction_df.head()
```

<p align="left">
  <img src="examples\assets\log_hub_tables.png" alt="Working with Log-hub Tables"  width="980"/>
</p>


### Working with Log-hub Tables

To read or update a table, you need a table link from a table in the Log-hub platform. Therefore, please navigate in a workspace with an existing dataset and go to the table you would like to read or update. Click on the "three dots" and click on "Table Link". Then copy the corresponding table link. If no table exists create a dataset and a new table via the GUI.

#### Reading Data from a Table
The read_table function simplifies the process of fetching and formatting data from a specific table on the Log-hub platform into a pandas DataFrame. This function ensures that the data types in the DataFrame match those in the Log-hub table, leveraging metadata from the table for precise formatting.

```python
from pyloghub.dataset import read_table
import pandas as pd

# Replace with actual table link, email, and API key
table_link = "https://production.supply-chain-apps.log-hub.com/api/v1/datasets/.../tables/.../rows"
email = "your_email@example.com"
api_key = "your_api_key"

# Read data from table
dataframe = read_table(table_link, email, api_key)

# Check the DataFrame
if dataframe is not None:
    print(dataframe.head())
else:
    print("Failed to read data from the table.")
```

#### Updating Data in a Table
The update_table function is designed for uploading data from a local pandas DataFrame to a specific table on the Log-hub platform. It requires the table link, the DataFrame, metadata describing the table structure (optional). If no metadata are provided, the datatypes are automatically extracted from the pandas dataframe.

```python
from pyloghub.dataset import update_table
import pandas as pd

# Replace with actual credentials and link
table_link = "https://production.supply-chain-apps.log-hub.com/api/v1/datasets/.../tables/.../rows"
email = "your_email@example.com"
api_key = "your_api_key"

# Example DataFrame
dataframe = pd.DataFrame({
    'ColumnA': ['Value1', 'Value2'],
    'ColumnB': [123, 456]
})

# Metadata for the table
metadata = {
    'table_name': 'YourTableName',  # Optional, defaults to 'Table 01' if not provided
    'columns': [
        {
            'name': 'ColumnA',
            'propertyName': 'ColumnA',
            'dataType': 'string',
            'format': 'General'
        },
        {
            'name': 'ColumnB',
            'propertyName': 'ColumnB',
            'dataType': 'number',
            'format': 'General'
        }
        # More columns as needed
    ]
}

# Update table
response = update_table(table_link, dataframe, metadata, email, api_key)

if response is None:
    print("Table updated successfully.")
else:
    print("Failed to update the table.")
```


## Contact Us

For any inquiries, assistance, or additional information, feel free to reach out to us at our office or via email.

**Address:**  
Schwandweg 5,  
8834 Schindellegi,  
Switzerland  

**Email:**  
[support@log-hub.com](mailto:support@log-hub.com)

Alternatively, for more information and resources, visit [Log-hub API Documentation](https://production.supply-chain-apps.log-hub.com/sca/api-docs).


## License

Distributed under the [MIT License](https://opensource.org/licenses/MIT).

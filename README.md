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

### Geocoding
#### Forward Geocoding
Convert addresses to geographic coordinates.

```python
from pyloghub.geocoding import forward_geocoding, forward_geocoding_sample_data

sample_data = forward_geocoding_sample_data()
addresses_df = sample_data['addresses']
forward_geocoding_result_df = forward_geocoding(addresses_df, api_key)
```

#### Reverse Geocoding
Convert geographic coordinates to addresses.

```python
from pyloghub.geocoding import reverse_geocoding, reverse_geocoding_sample_data

sample_data = reverse_geocoding_sample_data()
geocodes_df = sample_data['geocodes']
reverse_geocoding_result_df = reverse_geocoding(geocodes_df, api_key)
```

### Distance Calculation
#### Forward Distance Calculation
Calculate distances based on address data.

```python
from pyloghub.distance_calculation import forward_distance_calculation, forward_distance_calculation_sample_data

sample_data = forward_distance_calculation_sample_data()
address_data_df = sample_data['address_data']
parameters = sample_data['parameters']
forward_distance_calculation_result_df = forward_distance_calculation(address_data_df, parameters, api_key)
```

#### Reverse Distance Calculation
Calculate distances based on geocode data.

```python
from pyloghub.distance_calculation import reverse_distance_calculation, reverse_distance_calculation_sample_data

sample_data = reverse_distance_calculation_sample_data()
geocode_data_df = sample_data['geocode_data']
parameters = sample_data['parameters']
reverse_center_of_gravity_result_df = reverse_distance_calculation(geocode_data_df, parameters, api_key)
```

### Center of Gravity
#### Forward Center of Gravity
Determine optimal facility locations based on addresses.

```python
from pyloghub.center_of_gravity import forward_center_of_gravity, forward_center_of_gravity_sample_data

sample_data = forward_center_of_gravity_sample_data()
addresses_df = sample_data['addresses']
parameters = sample_data['parameters']
assigned_addresses_df, centers_df = forward_center_of_gravity(addresses_df, parameters, api_key)
```

#### Reverse Center of Gravity
Determine optimal facility locations based on coordinates.

```python
from pyloghub.center_of_gravity import reverse_center_of_gravity, reverse_center_of_gravity_sample_data

sample_data = reverse_center_of_gravity_sample_data()
coordinates_df = sample_data['coordinates']
parameters = sample_data['parameters']
assigned_geocodes_df, centers_df = reverse_center_of_gravity(coordinates_df, parameters, api_key)
```

### Transport Optimization
#### Milkrun Optimization Plus
Optimize delivery routes with multiple stops.

```python
from pyloghub.milkrun_optimization_plus import forward_milkrun_optimization_plus, forward_milkrun_optimization_plus_sample_data

sample_data = forward_milkrun_optimization_plus_sample_data()
depots_df = sample_data['depots']
vehicles_df = sample_data['vehicles']
jobs_df = sample_data['jobs']
timeWindowProfiles_df = sample_data['timeWindowProfiles']
breaks_df = sample_data['breaks']
parameters = sample_data['parameters']

route_overview_df, route_details_df, external_orders_df  = forward_milkrun_optimization_plus(depots_df, vehicles_df, jobs_df, timeWindowProfiles_df, breaks_df, parameters, api_key)
```

#### Transport Optimization Plus
Optimize transport routes for shipments.

```python
from pyloghub.transport_optimization_plus import forward_transport_optimization_plus, forward_transport_optimization_plus_sample_data

sample_data = forward_transport_optimization_plus_sample_data()
vehicles_df = sample_data['vehicles']
shipments_df = sample_data['shipments']
timeWindowProfiles_df = sample_data['timeWindowProfiles']
breaks_df = sample_data['breaks']
parameters = sample_data['parameters']

route_overview_df, route_details_df, external_orders_df = forward_transport_optimization_plus(vehicles_df, shipments_df, timeWindowProfiles_df, breaks_df, parameters, api_key)
```

#### Shipment Analyzer
Analyze and optimize shipment costs and operations.

```python
from pyloghub.shipment_analyzer import forward_shipment_analyzer, forward_shipment_analyzer_sample_data

sample_data = forward_shipment_analyzer_sample_data()
shipments_df = sample_data['shipments']
transport_costs_adjustments_df = sample_data['transportCostAdjustments']
consolidation_df = sample_data['consolidation']
surcharges_df = sample_data['surcharges']
parameters = sample_data['parameters']

shipments_analysis_df, transports_analysis_df = forward_shipment_analyzer(shipments_df, transport_costs_adjustments_df, consolidation_df, surcharges_df, parameters, api_key)
```

For the Milkrun Optimization, Transport Optimization as well as the Shipment Analyzer service there is also the reverse version available.

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

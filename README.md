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
  <img src="examples\assets\geocoding.png" alt="Header Image"  width="980"/>
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
<style>
.button-style {
    font-family: 'Open Sans', sans-serif;
    font-weight: 600;
    background-color: #F7F8FA;
    color: #111;
    border: 1px solid #E5E7EB;
    padding: 10px 20px;
    font-size: 14px;
    letter-spacing: 0.5px;
    border-radius: 6px;
    transition: background-color 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 10px;
}
.button-style:hover {
    background-color: #E5E7EB;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>
<style>
.table-container {
    width: 100%;
    overflow-x: auto;
    margin-bottom: 20px;
    border: none;
}
table {
    width: 100%;
    border-collapse: collapse;
    font-family: Arial, sans-serif;
    border: none;
}
th, td {
    text-align: right;
    border: none;
}
th {
    font-weight: bold;
    text-align: right;
    border: none;
}
tr {
  style="text-align: right;"
}
th {
  style="text-align: right;"
  border: none;
}
td {
  style = "border: none;"
}
</style>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>country</th>
      <th>state</th>
      <th>city</th>
      <th>street</th>
      <th>searchString</th>
      <th>parsedCountry</th>
      <th>parsedState</th>
      <th>parsedPostalCode</th>
      <th>parsedCity</th>
      <th>parsedStreet</th>
      <th>parsedLatitude</th>
      <th>parsedLongitude</th>
      <th>validationQuality</th>
    </tr>
  </thead>
  <tbody>
    <tr style="text-align: right;">
      <td>RU</td>
      <td></td>
      <td></td>
      <td>Moscow</td>
      <td></td>
      <td></td>
      <td>RU</td>
      <td>Moscow</td>
      <td></td>
      <td>Moscow</td>
      <td></td>
      <td>55.750541</td>
      <td>37.617478</td>
      <td>90</td>
    </tr>
    <tr>
      <td>TR</td>
      <td></td>
      <td></td>
      <td>Istanbul</td>
      <td></td>
      <td></td>
      <td>TR</td>
      <td></td>
      <td>34122</td>
      <td>Istanbul</td>
      <td></td>
      <td>41.006381</td>
      <td>28.975872</td>
      <td>91</td>
    </tr>
    <tr>
      <td>GB</td>
      <td></td>
      <td></td>
      <td>London</td>
      <td></td>
      <td></td>
      <td>GB</td>
      <td>England</td>
      <td></td>
      <td>London</td>
      <td></td>
      <td>51.507446</td>
      <td>-0.127765</td>
      <td>89</td>
    </tr>
    <tr>
      <td>RU</td>
      <td></td>
      <td></td>
      <td>Sankt Petersburg</td>
      <td></td>
      <td></td>
      <td>RU</td>
      <td>Saint Petersburg</td>
      <td></td>
      <td>Saint Petersburg</td>
      <td></td>
      <td>59.938732</td>
      <td>30.316229</td>
      <td>89</td>
    </tr>
    <tr>
      <td>DE</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td></td>
      <td>DE</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>52.510885</td>
      <td>13.398937</td>
      <td>86</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>latitude</th>
      <th>longitude</th>
      <th>parsedCountry</th>
      <th>parsedState</th>
      <th>parsedPostalCode</th>
      <th>parsedCity</th>
      <th>parsedStreet</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>55.479205</td>
      <td>37.327330</td>
      <td>RU</td>
      <td>Москва</td>
      <td>142793</td>
      <td></td>
      <td>проспект Славского</td>
    </tr>
    <tr>
      <td>41.076602</td>
      <td>29.052495</td>
      <td>TR</td>
      <td>İstanbul</td>
      <td>34342</td>
      <td>Beşiktaş</td>
      <td>Cevdetpaşa Caddesi</td>
    </tr>
    <tr>
      <td>51.507322</td>
      <td>-0.127647</td>
      <td>GB</td>
      <td>England</td>
      <td></td>
      <td>London</td>
      <td></td>
    </tr>
    <tr>
      <td>59.960674</td>
      <td>30.158655</td>
      <td>RU</td>
      <td>Санкт-Петербург</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>52.519854</td>
      <td>13.438596</td>
      <td>DE</td>
      <td></td>
      <td>10249</td>
      <td>Berlin</td>
      <td>Friedenstraße</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\distance_calculation.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>senderCountry</th>
      <th>senderState</th>
      <th>senderPostalCode</th>
      <th>senderCity</th>
      <th>senderStreet</th>
      <th>parsedSenderLatitude</th>
      <th>parsedSenderLongitude</th>
      <th>senderStatus</th>
      <th>recipientCountry</th>
      <th>recipientState</th>
      <th>recipientCity</th>
      <th>recipientStreet</th>
      <th>parsedRecipientLatitude</th>
      <th>parsedRecipientLongitude</th>
      <th>recipientStatus</th>
      <th>dist</th>
      <th>time</th>
      <th>beeline</th>
      <th>distanceUnit</th>
      <th>durationUnit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Fresno</td>
      <td></td>
      <td>36.739442</td>
      <td>-119.784830</td>
      <td>ok</td>
      <td>299.30</td>
      <td>193.59</td>
      <td>260.23</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Sacramento</td>
      <td></td>
      <td>38.581061</td>
      <td>-121.493895</td>
      <td>ok</td>
      <td>139.79</td>
      <td>94.98</td>
      <td>120.38</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Long Beach</td>
      <td></td>
      <td>33.769016</td>
      <td>-118.191604</td>
      <td>ok</td>
      <td>650.88</td>
      <td>404.49</td>
      <td>586.63</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Oakland</td>
      <td></td>
      <td>37.804456</td>
      <td>-122.271356</td>
      <td>ok</td>
      <td>18.46</td>
      <td>16.97</td>
      <td>13.30</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Bakersfield</td>
      <td></td>
      <td>35.373871</td>
      <td>-119.019463</td>
      <td>ok</td>
      <td>455.35</td>
      <td>285.39</td>
      <td>404.55</td>
      <td>km</td>
      <td>min</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>senderLocation</th>
      <th>senderLatitude</th>
      <th>senderLongitude</th>
      <th>recipientLocation</th>
      <th>recipientLatitude</th>
      <th>recipientLongitude</th>
      <th>dist</th>
      <th>time</th>
      <th>beeline</th>
      <th>distanceUnit</th>
      <th>durationUnit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Fresno</td>
      <td>36.729529</td>
      <td>-119.708861</td>
      <td>308.53</td>
      <td>201.03</td>
      <td>266.76</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Sacramento</td>
      <td>38.581572</td>
      <td>-121.494400</td>
      <td>139.87</td>
      <td>95.12</td>
      <td>120.39</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Long Beach</td>
      <td>33.785389</td>
      <td>-118.158049</td>
      <td>651.35</td>
      <td>405.27</td>
      <td>587.20</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Oakland</td>
      <td>37.804456</td>
      <td>-122.271356</td>
      <td>18.46</td>
      <td>16.96</td>
      <td>13.29</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Bakersfield</td>
      <td>35.373871</td>
      <td>-119.019464</td>
      <td>455.34</td>
      <td>285.39</td>
      <td>404.55</td>
      <td>km</td>
      <td>min</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>senderCountry</th>
      <th>senderState</th>
      <th>senderPostalCode</th>
      <th>senderCity</th>
      <th>senderStreet</th>
      <th>parsedSenderLatitude</th>
      <th>parsedSenderLongitude</th>
      <th>senderStatus</th>
      <th>recipientCountry</th>
      <th>recipientState</th>
      <th>recipientCity</th>
      <th>recipientStreet</th>
      <th>parsedRecipientLatitude</th>
      <th>parsedRecipientLongitude</th>
      <th>recipientStatus</th>
      <th>dist</th>
      <th>time</th>
      <th>route_id</th>
      <th>beeline</th>
      <th>distanceUnit</th>
      <th>durationUnit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Fresno</td>
      <td></td>
      <td>36.739442</td>
      <td>-119.784830</td>
      <td>ok</td>
      <td>299.30</td>
      <td>193.59</td>
      <td>1</td>
      <td>260.23</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Sacramento</td>
      <td></td>
      <td>38.581061</td>
      <td>-121.493895</td>
      <td>ok</td>
      <td>139.79</td>
      <td>94.98</td>
      <td>2</td>
      <td>120.38</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Long Beach</td>
      <td></td>
      <td>33.769016</td>
      <td>-118.191604</td>
      <td>ok</td>
      <td>650.88</td>
      <td>404.49</td>
      <td>3</td>
      <td>586.63</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Oakland</td>
      <td></td>
      <td>37.804456</td>
      <td>-122.271356</td>
      <td>ok</td>
      <td>18.46</td>
      <td>16.97</td>
      <td>4</td>
      <td>13.30</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>ok</td>
      <td>US</td>
      <td>CA</td>
      <td>Bakersfield</td>
      <td></td>
      <td>35.373871</td>
      <td>-119.019463</td>
      <td>ok</td>
      <td>455.35</td>
      <td>285.39</td>
      <td>5</td>
      <td>404.55</td>
      <td>km</td>
      <td>min</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>route_id</th>
      <th>country_name</th>
      <th>country_distance</th>
      <th>no_category</th>
      <th>highway</th>
      <th>tollways</th>
      <th>steps</th>
      <th>ferry</th>
      <th>ford</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>United States</td>
      <td>299.30</td>
      <td>4.39</td>
      <td>294.91</td>
      <td>4.35</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>2</td>
      <td>United States</td>
      <td>139.79</td>
      <td>6.73</td>
      <td>133.06</td>
      <td>4.07</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>United States</td>
      <td>650.88</td>
      <td>3.49</td>
      <td>647.39</td>
      <td>0.00</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>4</td>
      <td>United States</td>
      <td>18.46</td>
      <td>5.81</td>
      <td>12.65</td>
      <td>0.00</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>5</td>
      <td>United States</td>
      <td>455.35</td>
      <td>21.20</td>
      <td>434.14</td>
      <td>0.00</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>senderLocation</th>
      <th>senderLatitude</th>
      <th>senderLongitude</th>
      <th>recipientLocation</th>
      <th>recipientLatitude</th>
      <th>recipientLongitude</th>
      <th>dist</th>
      <th>time</th>
      <th>route_id</th>
      <th>beeline</th>
      <th>distanceUnit</th>
      <th>durationUnit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Fresno</td>
      <td>36.729529</td>
      <td>-119.708861</td>
      <td>308.53</td>
      <td>201.03</td>
      <td>1</td>
      <td>266.76</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Sacramento</td>
      <td>38.581572</td>
      <td>-121.494400</td>
      <td>139.87</td>
      <td>95.12</td>
      <td>2</td>
      <td>120.39</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Long Beach</td>
      <td>33.785389</td>
      <td>-118.158049</td>
      <td>651.35</td>
      <td>405.27</td>
      <td>3</td>
      <td>587.20</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Oakland</td>
      <td>37.804456</td>
      <td>-122.271356</td>
      <td>18.46</td>
      <td>16.96</td>
      <td>4</td>
      <td>13.29</td>
      <td>km</td>
      <td>min</td>
    </tr>
    <tr>
      <td>San Francisco</td>
      <td>37.779281</td>
      <td>-122.419236</td>
      <td>Bakersfield</td>
      <td>35.373871</td>
      <td>-119.019464</td>
      <td>455.34</td>
      <td>285.39</td>
      <td>5</td>
      <td>404.55</td>
      <td>km</td>
      <td>min</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>route_id</th>
      <th>country_name</th>
      <th>country_distance</th>
      <th>no_category</th>
      <th>highway</th>
      <th>tollways</th>
      <th>steps</th>
      <th>ferry</th>
      <th>ford</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>United States</td>
      <td>308.53</td>
      <td>6.09</td>
      <td>302.44</td>
      <td>4.35</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>2</td>
      <td>United States</td>
      <td>139.87</td>
      <td>6.81</td>
      <td>133.06</td>
      <td>4.07</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>United States</td>
      <td>651.35</td>
      <td>6.41</td>
      <td>644.94</td>
      <td>0.00</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>4</td>
      <td>United States</td>
      <td>18.46</td>
      <td>5.81</td>
      <td>12.65</td>
      <td>0.00</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>5</td>
      <td>United States</td>
      <td>455.34</td>
      <td>21.20</td>
      <td>434.14</td>
      <td>0.00</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\isochrone.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>country</th>
      <th>state</th>
      <th>postalCode</th>
      <th>city</th>
      <th>parsedCountry</th>
      <th>parsedState</th>
      <th>parsedPostalCode</th>
      <th>parsedCity</th>
      <th>parsedStreet</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>population</th>
      <th>timezone</th>
      <th>layer</th>
      <th>areakm2mi2</th>
      <th>populationBykm2mi2</th>
      <th>status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td>DE</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>52.51097</td>
      <td>13.398923</td>
      <td>359673</td>
      <td></td>
      <td>Layer 1</td>
      <td>63</td>
      <td>5709</td>
      <td>ok</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td>DE</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>52.51097</td>
      <td>13.398923</td>
      <td>1326228</td>
      <td></td>
      <td>Layer 2</td>
      <td>242</td>
      <td>5480</td>
      <td>ok</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td>DE</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>52.51097</td>
      <td>13.398923</td>
      <td>1459724</td>
      <td></td>
      <td>Layer 3</td>
      <td>452</td>
      <td>3229</td>
      <td>ok</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td>DE</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>52.51097</td>
      <td>13.398923</td>
      <td>758205</td>
      <td></td>
      <td>Layer 4</td>
      <td>975</td>
      <td>778</td>
      <td>ok</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td>DE</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>52.51097</td>
      <td>13.398923</td>
      <td>472305</td>
      <td></td>
      <td>Layer 5</td>
      <td>1415</td>
      <td>334</td>
      <td>ok</td>
    </tr>
  </tbody>
</table>
</div>

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

reachable_areas_df = reverse_isochrone(addresses_df, parameters, api_key, save_scenario, show_buttons=True)
reachable_areas_df.head()
```

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>latitude</th>
      <th>longitude</th>
      <th>name</th>
      <th>layer</th>
      <th>areakm2mi2</th>
      <th>population</th>
      <th>populationBykm2mi2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Berlin</td>
      <td>Layer 1</td>
      <td>72</td>
      <td>422397</td>
      <td>5867</td>
    </tr>
    <tr>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Berlin</td>
      <td>Layer 2</td>
      <td>249</td>
      <td>1325832</td>
      <td>5325</td>
    </tr>
    <tr>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Berlin</td>
      <td>Layer 3</td>
      <td>477</td>
      <td>1442949</td>
      <td>3025</td>
    </tr>
    <tr>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Berlin</td>
      <td>Layer 4</td>
      <td>989</td>
      <td>755202</td>
      <td>764</td>
    </tr>
    <tr>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Berlin</td>
      <td>Layer 5</td>
      <td>1584</td>
      <td>473102</td>
      <td>299</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\isochrone_plus.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>country</th>
      <th>state</th>
      <th>postalCode</th>
      <th>city</th>
      <th>street</th>
      <th>parsedCountry</th>
      <th>parsedState</th>
      <th>parsedPostalCode</th>
      <th>parsedCity</th>
      <th>parsedStreet</th>
      <th>population</th>
      <th>timezone</th>
      <th>status</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>DE</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td></td>
      <td></td>
      <td>ok</td>
      <td>52.510885</td>
      <td>13.398937</td>
    </tr>
    <tr>
      <td>Hamburg</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Hamburg</td>
      <td></td>
      <td>DE</td>
      <td></td>
      <td></td>
      <td>Hamburg</td>
      <td></td>
      <td></td>
      <td></td>
      <td>ok</td>
      <td>53.550341</td>
      <td>10.000654</td>
    </tr>
    <tr>
      <td>Frankfurt</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Frankfurt</td>
      <td></td>
      <td>DE</td>
      <td>Hesse</td>
      <td></td>
      <td>Frankfurt</td>
      <td></td>
      <td></td>
      <td></td>
      <td>ok</td>
      <td>50.110644</td>
      <td>8.682092</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>country</th>
      <th>state</th>
      <th>postalCode</th>
      <th>city</th>
      <th>street</th>
      <th>areaName</th>
      <th>areaCountry</th>
      <th>areaType</th>
      <th>areaLevel</th>
      <th>areaCenterLatitude</th>
      <th>areaCenterLongitude</th>
      <th>beelineDistanceToCenter</th>
      <th>estimatedTimeToCenter</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>areakm2mi2</th>
      <th>population</th>
      <th>populationBykm2mi2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>Moryń</td>
      <td>Poland</td>
      <td>Gmina (urban-rural)</td>
      <td>3</td>
      <td>52.855748</td>
      <td>14.404224</td>
      <td>77.861627</td>
      <td>93.433953</td>
      <td>52.510885</td>
      <td>13.398937</td>
      <td>125</td>
      <td>4308</td>
      <td>34</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>Mieszkowice</td>
      <td>Poland</td>
      <td>Gmina (urban-rural)</td>
      <td>3</td>
      <td>52.781190</td>
      <td>14.455068</td>
      <td>77.332035</td>
      <td>92.798442</td>
      <td>52.510885</td>
      <td>13.398937</td>
      <td>238</td>
      <td>6862</td>
      <td>29</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>Boleszkowice</td>
      <td>Poland</td>
      <td>Gmina (rural)</td>
      <td>3</td>
      <td>52.692201</td>
      <td>14.557352</td>
      <td>80.788366</td>
      <td>96.946039</td>
      <td>52.510885</td>
      <td>13.398937</td>
      <td>130</td>
      <td>2399</td>
      <td>18</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>Golzow</td>
      <td>Germany</td>
      <td>Amt</td>
      <td>3</td>
      <td>52.577099</td>
      <td>14.521444</td>
      <td>76.263266</td>
      <td>91.515919</td>
      <td>52.510885</td>
      <td>13.398937</td>
      <td>153</td>
      <td>5777</td>
      <td>38</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>Deutschland</td>
      <td></td>
      <td></td>
      <td>Berlin</td>
      <td></td>
      <td>Seelow</td>
      <td>Germany</td>
      <td>Amtsfreie Gemeinde</td>
      <td>3</td>
      <td>52.552815</td>
      <td>14.400625</td>
      <td>67.916026</td>
      <td>81.499232</td>
      <td>52.510885</td>
      <td>13.398937</td>
      <td>43</td>
      <td>5646</td>
      <td>131</td>
    </tr>
  </tbody>
</table>
</div>

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
save_scenario['scenarioName'] = "IP rev button" 
save_scenario['workspaceId'] = "2fdb6508020000336eda5932b32c114f9db46ccb"

geocoded_data_df, reachable_areas_df = reverse_isochrone_plus(coordinates_df, parameters, api_key, save_scenario, show_buttons=True)
display(geocoded_data_df.head())
display(reachable_areas_df.head())
```

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Berlin</td>
      <td>52.517037</td>
      <td>13.388860</td>
    </tr>
    <tr>
      <td>Hamburg</td>
      <td>53.543764</td>
      <td>10.009913</td>
    </tr>
    <tr>
      <td>Frankfurt</td>
      <td>50.110644</td>
      <td>8.682092</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>areaName</th>
      <th>areaCountry</th>
      <th>areaType</th>
      <th>areaLevel</th>
      <th>areaCenterLatitude</th>
      <th>areaCenterLongitude</th>
      <th>beelineDistanceToCenter</th>
      <th>areakm2mi2</th>
      <th>population</th>
      <th>populationBykm2mi2</th>
      <th>timeToCenterMin</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Berlin</td>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Moryń</td>
      <td>Poland</td>
      <td>Gmina (urban-rural)</td>
      <td>3</td>
      <td>52.855748</td>
      <td>14.404224</td>
      <td>78.117228</td>
      <td>125</td>
      <td>4308</td>
      <td>34</td>
      <td>93.740674</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Mieszkowice</td>
      <td>Poland</td>
      <td>Gmina (urban-rural)</td>
      <td>3</td>
      <td>52.781190</td>
      <td>14.455068</td>
      <td>77.693033</td>
      <td>238</td>
      <td>6862</td>
      <td>29</td>
      <td>93.231640</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Boleszkowice</td>
      <td>Poland</td>
      <td>Gmina (rural)</td>
      <td>3</td>
      <td>52.692201</td>
      <td>14.557352</td>
      <td>81.275537</td>
      <td>130</td>
      <td>2399</td>
      <td>18</td>
      <td>97.530644</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Golzow</td>
      <td>Germany</td>
      <td>Amt</td>
      <td>3</td>
      <td>52.577099</td>
      <td>14.521444</td>
      <td>76.873737</td>
      <td>153</td>
      <td>5777</td>
      <td>38</td>
      <td>92.248485</td>
    </tr>
    <tr>
      <td>Berlin</td>
      <td>52.517037</td>
      <td>13.38886</td>
      <td>Seelow</td>
      <td>Germany</td>
      <td>Amtsfreie Gemeinde</td>
      <td>3</td>
      <td>52.552815</td>
      <td>14.400625</td>
      <td>68.548156</td>
      <td>43</td>
      <td>5646</td>
      <td>131</td>
      <td>82.257787</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\supply_chain_maps.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>country</th>
      <th>state</th>
      <th>postalCode</th>
      <th>city</th>
      <th>street</th>
      <th>layer</th>
      <th>quantity</th>
      <th>nameDescription1</th>
      <th>nameDescription2</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CG-12970</td>
      <td>US</td>
      <td>Kentucky</td>
      <td>42420</td>
      <td>Henderson</td>
      <td></td>
      <td>South</td>
      <td>2145.11</td>
      <td>South</td>
      <td>Supermarket</td>
      <td>37.767210</td>
      <td>-87.557374</td>
    </tr>
    <tr>
      <td>JE-16615</td>
      <td>US</td>
      <td>Wisconsin</td>
      <td>53132</td>
      <td>Franklin</td>
      <td></td>
      <td>Central</td>
      <td>9439.45</td>
      <td>Central</td>
      <td>Discount Store</td>
      <td>42.888627</td>
      <td>-88.038418</td>
    </tr>
    <tr>
      <td>DV-13495</td>
      <td>US</td>
      <td>California</td>
      <td>90036</td>
      <td>Los Angeles</td>
      <td></td>
      <td>West</td>
      <td>5907.48</td>
      <td>West</td>
      <td>Discount Store</td>
      <td>34.053691</td>
      <td>-118.242766</td>
    </tr>
    <tr>
      <td>BF-11425</td>
      <td>US</td>
      <td>North Carolina</td>
      <td>28205</td>
      <td>Charlotte</td>
      <td></td>
      <td>South</td>
      <td>4529.33</td>
      <td>South</td>
      <td>Discount Store</td>
      <td>35.227209</td>
      <td>-80.843083</td>
    </tr>
    <tr>
      <td>SO-20785</td>
      <td>US</td>
      <td>Florida</td>
      <td>33311</td>
      <td>Fort Lauderdale</td>
      <td></td>
      <td>South</td>
      <td>15881.34</td>
      <td>South</td>
      <td>Supermarket</td>
      <td>26.122308</td>
      <td>-80.143379</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>layer</th>
      <th>quantity</th>
      <th>nameDescription1</th>
      <th>nameDescription2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CG-12970</td>
      <td>37.827384</td>
      <td>-87.559035</td>
      <td>South</td>
      <td>2145.11</td>
      <td>South</td>
      <td>Supermarket</td>
    </tr>
    <tr>
      <td>JE-16615</td>
      <td>42.905176</td>
      <td>-88.016468</td>
      <td>Central</td>
      <td>9439.45</td>
      <td>Central</td>
      <td>Discount Store</td>
    </tr>
    <tr>
      <td>DV-13495</td>
      <td>34.066482</td>
      <td>-118.352039</td>
      <td>West</td>
      <td>5907.48</td>
      <td>West</td>
      <td>Discount Store</td>
    </tr>
    <tr>
      <td>BF-11425</td>
      <td>35.241809</td>
      <td>-80.801737</td>
      <td>South</td>
      <td>4529.33</td>
      <td>South</td>
      <td>Discount Store</td>
    </tr>
    <tr>
      <td>SO-20785</td>
      <td>26.153974</td>
      <td>-80.169490</td>
      <td>South</td>
      <td>15881.34</td>
      <td>South</td>
      <td>Supermarket</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>senderCountry</th>
      <th>senderState</th>
      <th>senderPostalCode</th>
      <th>senderCity</th>
      <th>senderStreet</th>
      <th>parsedSenderLatitude</th>
      <th>parsedSenderLongitude</th>
      <th>recipientCountry</th>
      <th>recipientState</th>
      <th>recipientPostalCode</th>
      <th>recipientCity</th>
      <th>recipientStreet</th>
      <th>parsedRecipientLatitude</th>
      <th>parsedRecipientLongitude</th>
      <th>senderLocationLayer</th>
      <th>layer</th>
      <th>quantity</th>
      <th>nameDescription1</th>
      <th>nameDescription2</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>US</td>
      <td>Kentucky</td>
      <td>40003</td>
      <td></td>
      <td></td>
      <td>38.255597</td>
      <td>-85.061561</td>
      <td>US</td>
      <td>Kentucky</td>
      <td>42420</td>
      <td>Henderson</td>
      <td></td>
      <td>37.767210</td>
      <td>-87.557374</td>
      <td>Warehouse</td>
      <td>South</td>
      <td>2145.11</td>
      <td>South</td>
      <td>Supermarket</td>
      <td>CG-12970</td>
    </tr>
    <tr>
      <td>US</td>
      <td>Illinois</td>
      <td>60516</td>
      <td>Downers Grove</td>
      <td></td>
      <td>41.793682</td>
      <td>-88.010228</td>
      <td>US</td>
      <td>Wisconsin</td>
      <td>53132</td>
      <td>Franklin</td>
      <td></td>
      <td>42.888627</td>
      <td>-88.038418</td>
      <td>Warehouse</td>
      <td>Central</td>
      <td>9439.45</td>
      <td>Central</td>
      <td>Discount Store</td>
      <td>JE-16615</td>
    </tr>
    <tr>
      <td>US</td>
      <td>California</td>
      <td>92801</td>
      <td>Anaheim</td>
      <td></td>
      <td>33.834752</td>
      <td>-117.911732</td>
      <td>US</td>
      <td>California</td>
      <td>90036</td>
      <td>Los Angeles</td>
      <td></td>
      <td>34.053691</td>
      <td>-118.242766</td>
      <td>Warehouse</td>
      <td>West</td>
      <td>5907.48</td>
      <td>West</td>
      <td>Discount Store</td>
      <td>DV-13495</td>
    </tr>
    <tr>
      <td>US</td>
      <td>Virginia</td>
      <td></td>
      <td></td>
      <td></td>
      <td>37.123224</td>
      <td>-78.492772</td>
      <td>US</td>
      <td>North Carolina</td>
      <td>28205</td>
      <td>Charlotte</td>
      <td></td>
      <td>35.241809</td>
      <td>-80.801737</td>
      <td>Warehouse</td>
      <td>South</td>
      <td>4529.33</td>
      <td>South</td>
      <td>Discount Store</td>
      <td>BF-11425</td>
    </tr>
    <tr>
      <td>US</td>
      <td>Florida</td>
      <td></td>
      <td></td>
      <td></td>
      <td>27.756767</td>
      <td>-81.463983</td>
      <td>US</td>
      <td>Florida</td>
      <td>33311</td>
      <td>Fort Lauderdale</td>
      <td></td>
      <td>26.153974</td>
      <td>-80.169490</td>
      <td>Warehouse</td>
      <td>South</td>
      <td>15881.34</td>
      <td>South</td>
      <td>Supermarket</td>
      <td>SO-20785</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>senderName</th>
      <th>senderLatitude</th>
      <th>senderLongitude</th>
      <th>senderLocationLayer</th>
      <th>recipientName</th>
      <th>recipientLatitude</th>
      <th>recipientLongitude</th>
      <th>recipientLocationLayer</th>
      <th>relationLayer</th>
      <th>quantity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Center 8</td>
      <td>38.223905</td>
      <td>-85.045030</td>
      <td>Warehouse</td>
      <td>CG-12970</td>
      <td>37.827384</td>
      <td>-87.559035</td>
      <td>South</td>
      <td>Distribution</td>
      <td>2145</td>
    </tr>
    <tr>
      <td>Center 13</td>
      <td>41.753940</td>
      <td>-88.005545</td>
      <td>Warehouse</td>
      <td>JE-16615</td>
      <td>42.905176</td>
      <td>-88.016468</td>
      <td>Central</td>
      <td>Distribution</td>
      <td>9439</td>
    </tr>
    <tr>
      <td>Center 5</td>
      <td>33.854662</td>
      <td>-117.973103</td>
      <td>Warehouse</td>
      <td>DV-13495</td>
      <td>34.066482</td>
      <td>-118.352039</td>
      <td>West</td>
      <td>Distribution</td>
      <td>5907</td>
    </tr>
    <tr>
      <td>Center 6</td>
      <td>36.831887</td>
      <td>-78.335525</td>
      <td>Warehouse</td>
      <td>BF-11425</td>
      <td>35.241809</td>
      <td>-80.801737</td>
      <td>South</td>
      <td>Distribution</td>
      <td>4529</td>
    </tr>
    <tr>
      <td>Center 1</td>
      <td>28.075587</td>
      <td>-81.173554</td>
      <td>Warehouse</td>
      <td>SO-20785</td>
      <td>26.153974</td>
      <td>-80.169490</td>
      <td>South</td>
      <td>Distribution</td>
      <td>15881</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>searchId</th>
      <th>country</th>
      <th>region</th>
      <th>name</th>
      <th>layer</th>
      <th>quantity</th>
      <th>continent</th>
      <th>countryRegionOne</th>
      <th>countryRegionTwo</th>
      <th>countryName</th>
      <th>centerLat</th>
      <th>centerLong</th>
      <th>population</th>
      <th>area_km2</th>
      <th>length_km</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>D3 Cerklje na Gorenjskem</td>
      <td>SI</td>
      <td>Cerklje na Gorenjskem</td>
      <td>Cerklje na Gorenjskem</td>
      <td>D3 Commune|Municipality</td>
      <td>8572.36</td>
      <td>Europe</td>
      <td>Southern Europe</td>
      <td></td>
      <td>Slovenia</td>
      <td>46.252904</td>
      <td>14.493528</td>
      <td>8572.36</td>
      <td>77.27</td>
      <td>38.92</td>
    </tr>
    <tr>
      <td>D3 Gorenja Vas-Poljane</td>
      <td>SI</td>
      <td>Gorenja Vas-Poljane</td>
      <td>Gorenja Vas-Poljane</td>
      <td>D3 Commune|Municipality</td>
      <td>7507.47</td>
      <td>Europe</td>
      <td>Southern Europe</td>
      <td></td>
      <td>Slovenia</td>
      <td>46.116649</td>
      <td>14.130162</td>
      <td>7507.47</td>
      <td>152.04</td>
      <td>59.83</td>
    </tr>
    <tr>
      <td>D3 Jezersko</td>
      <td>SI</td>
      <td>Jezersko</td>
      <td>Jezersko</td>
      <td>D3 Commune|Municipality</td>
      <td>609.72</td>
      <td>Europe</td>
      <td>Southern Europe</td>
      <td></td>
      <td>Slovenia</td>
      <td>46.387400</td>
      <td>14.480943</td>
      <td>609.72</td>
      <td>70.58</td>
      <td>41.94</td>
    </tr>
    <tr>
      <td>D3 Železniki</td>
      <td>SI</td>
      <td>Železniki</td>
      <td>Železniki</td>
      <td>D3 Commune|Municipality</td>
      <td>6239.23</td>
      <td>Europe</td>
      <td>Southern Europe</td>
      <td></td>
      <td>Slovenia</td>
      <td>46.219671</td>
      <td>14.105773</td>
      <td>6239.23</td>
      <td>163.84</td>
      <td>69.36</td>
    </tr>
    <tr>
      <td>D3 Bovec</td>
      <td>SI</td>
      <td>Bovec</td>
      <td>Bovec</td>
      <td>D3 Commune|Municipality</td>
      <td>3466.04</td>
      <td>Europe</td>
      <td>Southern Europe</td>
      <td></td>
      <td>Slovenia</td>
      <td>46.361327</td>
      <td>13.622877</td>
      <td>3466.04</td>
      <td>382.47</td>
      <td>100.65</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>polyline</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>layer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Polyline 1</td>
      <td>50.068764</td>
      <td>7.777298</td>
      <td>Layer 1</td>
    </tr>
    <tr>
      <td>Polyline 1</td>
      <td>50.070352</td>
      <td>7.777697</td>
      <td>Layer 1</td>
    </tr>
    <tr>
      <td>Polyline 1</td>
      <td>50.071177</td>
      <td>7.777859</td>
      <td>Layer 1</td>
    </tr>
    <tr>
      <td>Polyline 1</td>
      <td>50.072018</td>
      <td>7.777996</td>
      <td>Layer 1</td>
    </tr>
    <tr>
      <td>Polyline 1</td>
      <td>50.072891</td>
      <td>7.778157</td>
      <td>Layer 1</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>routeId</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>pickupQuantity</th>
      <th>deliveryQuantity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Route 1</td>
      <td>Depot_Tilburg</td>
      <td>51.556240</td>
      <td>5.088601</td>
      <td>16</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Route 1</td>
      <td>NL_5043_Tilburg</td>
      <td>51.556240</td>
      <td>5.088601</td>
      <td>4</td>
      <td>2</td>
    </tr>
    <tr>
      <td>Route 1</td>
      <td>NL_5035_Tilburg</td>
      <td>51.556240</td>
      <td>5.088601</td>
      <td>4</td>
      <td>2</td>
    </tr>
    <tr>
      <td>Route 1</td>
      <td>NL_5105_Dongen</td>
      <td>51.642893</td>
      <td>4.957877</td>
      <td>0</td>
      <td>4</td>
    </tr>
    <tr>
      <td>Route 1</td>
      <td>NL_5106_Dongen</td>
      <td>51.642893</td>
      <td>4.957877</td>
      <td>0</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>routeId</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>pickupQuantity</th>
      <th>deliveryQuantity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Route 1</td>
      <td>Depot_Tilburg</td>
      <td>51.556240</td>
      <td>5.088601</td>
      <td>16</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Route 1</td>
      <td>NL_5043_Tilburg</td>
      <td>51.556240</td>
      <td>5.088601</td>
      <td>4</td>
      <td>2</td>
    </tr>
    <tr>
      <td>Route 1</td>
      <td>NL_5035_Tilburg</td>
      <td>51.556240</td>
      <td>5.088601</td>
      <td>4</td>
      <td>2</td>
    </tr>
    <tr>
      <td>Route 1</td>
      <td>NL_5105_Dongen</td>
      <td>51.642893</td>
      <td>4.957877</td>
      <td>0</td>
      <td>4</td>
    </tr>
    <tr>
      <td>Route 1</td>
      <td>NL_5106_Dongen</td>
      <td>51.642893</td>
      <td>4.957877</td>
      <td>0</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>fromName</th>
      <th>fromUnLocode</th>
      <th>toName</th>
      <th>toUnLocode</th>
      <th>quantity</th>
      <th>distance</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>fromIso2Country</th>
      <th>toIso2Country</th>
      <th>distanceUnit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Shanghai</td>
      <td>CNSHG</td>
      <td>Rotterdam</td>
      <td>NLRTM</td>
      <td>1000</td>
      <td>10526.35</td>
      <td>30.626539</td>
      <td>122.064958</td>
      <td>51.916667</td>
      <td>4.500000</td>
      <td>CN</td>
      <td>NL</td>
      <td>nm</td>
    </tr>
    <tr>
      <td>Singapore</td>
      <td>SGSIN</td>
      <td>Shenzhen</td>
      <td>CNSZX</td>
      <td>1000</td>
      <td>1460.42</td>
      <td>1.264000</td>
      <td>103.840000</td>
      <td>22.500000</td>
      <td>113.883333</td>
      <td>SG</td>
      <td>CN</td>
      <td>nm</td>
    </tr>
    <tr>
      <td>Zhoushan</td>
      <td>CNZOS</td>
      <td>Hamburg</td>
      <td>DEHAM</td>
      <td>1000</td>
      <td>14590.69</td>
      <td>29.560000</td>
      <td>121.500000</td>
      <td>53.516667</td>
      <td>9.933333</td>
      <td>CN</td>
      <td>DE</td>
      <td>nm</td>
    </tr>
    <tr>
      <td>Rotterdam</td>
      <td>NLRTM</td>
      <td>Guangzhou</td>
      <td>CNGZG</td>
      <td>1000</td>
      <td>13204.37</td>
      <td>51.916667</td>
      <td>4.500000</td>
      <td>23.085500</td>
      <td>113.425000</td>
      <td>NL</td>
      <td>CN</td>
      <td>nm</td>
    </tr>
    <tr>
      <td>Dubai</td>
      <td>AEDXB</td>
      <td>Busan</td>
      <td>KRPUS</td>
      <td>1000</td>
      <td>6077.56</td>
      <td>25.250000</td>
      <td>55.266667</td>
      <td>35.133333</td>
      <td>129.050000</td>
      <td>AE</td>
      <td>KR</td>
      <td>nm</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>fromName</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>toName</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>quantity</th>
      <th>distance</th>
      <th>fromIso2Country</th>
      <th>toIso2Country</th>
      <th>fromUnLocode</th>
      <th>toUnLocode</th>
      <th>distanceUnit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Shanghai</td>
      <td>30.626539</td>
      <td>122.064958</td>
      <td>Rotterdam</td>
      <td>51.916667</td>
      <td>4.500000</td>
      <td>1000</td>
      <td>10526.35</td>
      <td>CN</td>
      <td>NL</td>
      <td>CNSHG</td>
      <td>NLRTM</td>
      <td>nm</td>
    </tr>
    <tr>
      <td>Singapore</td>
      <td>1.264000</td>
      <td>103.840000</td>
      <td>Shenzhen</td>
      <td>22.500000</td>
      <td>113.883333</td>
      <td>1000</td>
      <td>1460.42</td>
      <td>SG</td>
      <td>CN</td>
      <td>SGSIN</td>
      <td>CNSZX</td>
      <td>nm</td>
    </tr>
    <tr>
      <td>Zhoushan</td>
      <td>29.560000</td>
      <td>121.500000</td>
      <td>Hamburg</td>
      <td>53.516667</td>
      <td>9.933333</td>
      <td>1000</td>
      <td>14590.69</td>
      <td>CN</td>
      <td>DE</td>
      <td>CNZOS</td>
      <td>DEHAM</td>
      <td>nm</td>
    </tr>
    <tr>
      <td>Rotterdam</td>
      <td>51.916667</td>
      <td>4.500000</td>
      <td>Guangzhou</td>
      <td>23.085500</td>
      <td>113.425000</td>
      <td>1000</td>
      <td>13204.37</td>
      <td>NL</td>
      <td>CN</td>
      <td>NLRTM</td>
      <td>CNGZG</td>
      <td>nm</td>
    </tr>
    <tr>
      <td>Dubai</td>
      <td>25.250000</td>
      <td>55.266667</td>
      <td>Busan</td>
      <td>35.133333</td>
      <td>129.050000</td>
      <td>1000</td>
      <td>6077.56</td>
      <td>AE</td>
      <td>KR</td>
      <td>AEDXB</td>
      <td>KRPUS</td>
      <td>nm</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\center_of_gravity.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>weight</th>
      <th>centerLatitude</th>
      <th>centerLongitude</th>
      <th>centerName</th>
      <th>distance</th>
      <th>country</th>
      <th>state</th>
      <th>postalCode</th>
      <th>city</th>
      <th>street</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Customer_0044</td>
      <td>367</td>
      <td>30.605067</td>
      <td>75.412006</td>
      <td>Center 2</td>
      <td>136.51</td>
      <td>IN</td>
      <td></td>
      <td>143500</td>
      <td>Batala</td>
      <td></td>
      <td>31.819302</td>
      <td>75.199997</td>
    </tr>
    <tr>
      <td>Customer_1378</td>
      <td>67</td>
      <td>25.489989</td>
      <td>87.847055</td>
      <td>Center 3</td>
      <td>176.92</td>
      <td>IN</td>
      <td></td>
      <td>736135</td>
      <td>Dinhata</td>
      <td></td>
      <td>26.123838</td>
      <td>89.468102</td>
    </tr>
    <tr>
      <td>Customer_0263</td>
      <td>20</td>
      <td>23.826857</td>
      <td>71.872190</td>
      <td>Center 4</td>
      <td>285.87</td>
      <td>IN</td>
      <td></td>
      <td>345025</td>
      <td>Phalsund</td>
      <td></td>
      <td>26.397339</td>
      <td>71.922417</td>
    </tr>
    <tr>
      <td>Customer_0767</td>
      <td>238</td>
      <td>11.329570</td>
      <td>77.731634</td>
      <td>Center 5</td>
      <td>119.38</td>
      <td>IN</td>
      <td></td>
      <td>635111</td>
      <td>Karimangalam</td>
      <td></td>
      <td>12.307006</td>
      <td>78.185379</td>
    </tr>
    <tr>
      <td>Customer_1027</td>
      <td>664</td>
      <td>17.060637</td>
      <td>79.283285</td>
      <td>Center 1</td>
      <td>299.97</td>
      <td>IN</td>
      <td></td>
      <td>524001</td>
      <td>Nellore</td>
      <td></td>
      <td>14.449371</td>
      <td>79.987373</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>centerLatitude</th>
      <th>centerLongitude</th>
      <th>centerName</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>17.060637</td>
      <td>79.283285</td>
      <td>Center 1</td>
      <td>7576</td>
    </tr>
    <tr>
      <td>30.605067</td>
      <td>75.412006</td>
      <td>Center 2</td>
      <td>9782</td>
    </tr>
    <tr>
      <td>25.489989</td>
      <td>87.847055</td>
      <td>Center 3</td>
      <td>4136</td>
    </tr>
    <tr>
      <td>23.826857</td>
      <td>71.872190</td>
      <td>Center 4</td>
      <td>3808</td>
    </tr>
    <tr>
      <td>11.329570</td>
      <td>77.731634</td>
      <td>Center 5</td>
      <td>9395</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>weight</th>
      <th>centerLatitude</th>
      <th>centerLongitude</th>
      <th>centerName</th>
      <th>distance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Customer_0044</td>
      <td>31.818508</td>
      <td>75.204906</td>
      <td>367</td>
      <td>30.527110</td>
      <td>75.472489</td>
      <td>Center 3</td>
      <td>145.84</td>
    </tr>
    <tr>
      <td>Customer_1378</td>
      <td>26.126189</td>
      <td>89.467499</td>
      <td>67</td>
      <td>25.627212</td>
      <td>88.132321</td>
      <td>Center 2</td>
      <td>144.64</td>
    </tr>
    <tr>
      <td>Customer_0263</td>
      <td>26.402907</td>
      <td>71.916797</td>
      <td>20</td>
      <td>23.825234</td>
      <td>71.899610</td>
      <td>Center 4</td>
      <td>286.63</td>
    </tr>
    <tr>
      <td>Customer_0767</td>
      <td>12.299513</td>
      <td>78.206302</td>
      <td>238</td>
      <td>11.337219</td>
      <td>77.733798</td>
      <td>Center 1</td>
      <td>118.72</td>
    </tr>
    <tr>
      <td>Customer_1027</td>
      <td>14.446319</td>
      <td>79.982021</td>
      <td>664</td>
      <td>17.052517</td>
      <td>79.267603</td>
      <td>Center 5</td>
      <td>299.71</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>centerLatitude</th>
      <th>centerLongitude</th>
      <th>centerName</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>11.337219</td>
      <td>77.733798</td>
      <td>Center 1</td>
      <td>9395</td>
    </tr>
    <tr>
      <td>25.627212</td>
      <td>88.132321</td>
      <td>Center 2</td>
      <td>4004</td>
    </tr>
    <tr>
      <td>30.527110</td>
      <td>75.472489</td>
      <td>Center 3</td>
      <td>9914</td>
    </tr>
    <tr>
      <td>23.825234</td>
      <td>71.899610</td>
      <td>Center 4</td>
      <td>3808</td>
    </tr>
    <tr>
      <td>17.052517</td>
      <td>79.267603</td>
      <td>Center 5</td>
      <td>7576</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\fixed_center_of_gravity.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>weight</th>
      <th>centerLatitude</th>
      <th>centerLongitude</th>
      <th>centerName</th>
      <th>distance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Customer_ES_1</td>
      <td>37.23431</td>
      <td>-3.823843</td>
      <td>722.124</td>
      <td>37.018365</td>
      <td>-4.559665</td>
      <td>Fixed_Center_ES_2</td>
      <td>69.513928</td>
    </tr>
    <tr>
      <td>Customer_ES_2</td>
      <td>43.266472</td>
      <td>-3.892813</td>
      <td>2864.672</td>
      <td>42.818199</td>
      <td>-1.644009</td>
      <td>Fixed_Center_ES_3</td>
      <td>189.421872</td>
    </tr>
    <tr>
      <td>Customer_ES_3</td>
      <td>42.242729</td>
      <td>0.197584</td>
      <td>1032.668</td>
      <td>41.577721</td>
      <td>1.159376</td>
      <td>Center 4</td>
      <td>108.637035</td>
    </tr>
    <tr>
      <td>Customer_ES_4</td>
      <td>41.614761</td>
      <td>0.626784</td>
      <td>998.138</td>
      <td>41.577721</td>
      <td>1.159376</td>
      <td>Center 4</td>
      <td>44.479366</td>
    </tr>
    <tr>
      <td>Customer_ES_5</td>
      <td>42.284222</td>
      <td>-8.6086</td>
      <td>949.193</td>
      <td>41.612202</td>
      <td>-5.433072</td>
      <td>Center 5</td>
      <td>273.024526</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>centerLatitude</th>
      <th>centerLongitude</th>
      <th>centerName</th>
      <th>fixed</th>
      <th>savingPotential</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>40.914187</td>
      <td>-1.298175</td>
      <td>Fixed_Center_ES_1</td>
      <td>yes</td>
      <td>-5.90</td>
      <td>96136.698</td>
    </tr>
    <tr>
      <td>37.018365</td>
      <td>-4.559665</td>
      <td>Fixed_Center_ES_2</td>
      <td>yes</td>
      <td>-1.42</td>
      <td>128526.541</td>
    </tr>
    <tr>
      <td>42.818199</td>
      <td>-1.644009</td>
      <td>Fixed_Center_ES_3</td>
      <td>yes</td>
      <td>-9.71</td>
      <td>116359.143</td>
    </tr>
    <tr>
      <td>41.577721</td>
      <td>1.159376</td>
      <td>Center 4</td>
      <td>no</td>
      <td>0.00</td>
      <td>59842.621</td>
    </tr>
    <tr>
      <td>41.612202</td>
      <td>-5.433072</td>
      <td>Center 5</td>
      <td>no</td>
      <td>0.00</td>
      <td>232405.247</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>weight</th>
      <th>centerLatitude</th>
      <th>centerLongitude</th>
      <th>centerName</th>
      <th>distance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Customer_ES_1</td>
      <td>38.464288</td>
      <td>-0.498835</td>
      <td>674.01</td>
      <td>37.302008</td>
      <td>-1.885545</td>
      <td>Fixed_Center_ES_1</td>
      <td>177.516944</td>
    </tr>
    <tr>
      <td>Customer_ES_2</td>
      <td>40.197869</td>
      <td>-0.23732</td>
      <td>648.31</td>
      <td>41.03904</td>
      <td>-0.866398</td>
      <td>Fixed_Center_ES_2</td>
      <td>107.553133</td>
    </tr>
    <tr>
      <td>Customer_ES_3</td>
      <td>38.625397</td>
      <td>-0.576848</td>
      <td>539.95</td>
      <td>37.302008</td>
      <td>-1.885545</td>
      <td>Fixed_Center_ES_1</td>
      <td>186.587991</td>
    </tr>
    <tr>
      <td>Customer_ES_4</td>
      <td>40.099452</td>
      <td>-0.45167</td>
      <td>667.55</td>
      <td>41.03904</td>
      <td>-0.866398</td>
      <td>Fixed_Center_ES_2</td>
      <td>110.193388</td>
    </tr>
    <tr>
      <td>Customer_ES_5</td>
      <td>39.8943</td>
      <td>-0.579091</td>
      <td>965.01</td>
      <td>41.03904</td>
      <td>-0.866398</td>
      <td>Fixed_Center_ES_2</td>
      <td>129.588651</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr style="text-align: right;">
      <th>centerLatitude</th>
      <th>centerLongitude</th>
      <th>centerName</th>
      <th>fixed</th>
      <th>savingPotential</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>37.302008</td>
      <td>-1.885545</td>
      <td>Fixed_Center_ES_1</td>
      <td>yes</td>
      <td>2.93</td>
      <td>57270.86</td>
    </tr>
    <tr>
      <td>41.03904</td>
      <td>-0.866398</td>
      <td>Fixed_Center_ES_2</td>
      <td>yes</td>
      <td>-2.62</td>
      <td>129603.9</td>
    </tr>
    <tr>
      <td>41.99953</td>
      <td>-5.74665</td>
      <td>Fixed_Center_ES_3</td>
      <td>yes</td>
      <td>1.94</td>
      <td>122758.96</td>
    </tr>
    <tr>
      <td>37.945379</td>
      <td>-5.568481</td>
      <td>Center 4</td>
      <td>no</td>
      <td>0.0</td>
      <td>94999.9</td>
    </tr>
    <tr>
      <td>39.99712</td>
      <td>-3.631111</td>
      <td>Center 5</td>
      <td>no</td>
      <td>0.0</td>
      <td>86881.78</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\center_of_gravity_plus.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
        <thead>
            <tr>
                <th>name</th>
                <th>weight</th>
                <th>volume</th>
                <th>revenue</th>
                <th>centerLatitude</th>
                <th>centerLongitude</th>
                <th>centerName</th>
                <th>distance</th>
                <th>country</th>
                <th>state</th>
                <th>postalCode</th>
                <th>city</th>
                <th>street</th>
                <th>latitude</th>
                <th>longitude</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Paris</td>
                <td>1120311</td>
                <td>3201</td>
                <td>2400750</td>
                <td>48.85889</td>
                <td>2.320041</td>
                <td>Center 2</td>
                <td>0.00</td>
                <td>FR</td>
                <td></td>
                <td></td>
                <td>Paris</td>
                <td></td>
                <td>48.858891</td>
                <td>2.320041</td>
            </tr>
            <tr>
                <td>Marseille</td>
                <td>426258</td>
                <td>1218</td>
                <td>913500</td>
                <td>43.81293</td>
                <td>4.939257</td>
                <td>Center 1</td>
                <td>67.13</td>
                <td>FR</td>
                <td></td>
                <td></td>
                <td>Marseille</td>
                <td></td>
                <td>43.296173</td>
                <td>5.369953</td>
            </tr>
            <tr>
                <td>Lyon</td>
                <td>248172</td>
                <td>709</td>
                <td>531750</td>
                <td>43.81293</td>
                <td>4.939257</td>
                <td>Center 1</td>
                <td>216.43</td>
                <td>FR</td>
                <td></td>
                <td></td>
                <td>Lyon</td>
                <td></td>
                <td>45.757812</td>
                <td>4.832011</td>
            </tr>
            <tr>
                <td>Toulouse</td>
                <td>226659</td>
                <td>648</td>
                <td>486000</td>
                <td>43.81293</td>
                <td>4.939257</td>
                <td>Center 1</td>
                <td>281.86</td>
                <td>FR</td>
                <td></td>
                <td></td>
                <td>Toulouse</td>
                <td></td>
                <td>43.604462</td>
                <td>1.444247</td>
            </tr>
            <tr>
                <td>Nice</td>
                <td>171810</td>
                <td>491</td>
                <td>368250</td>
                <td>43.81293</td>
                <td>4.939257</td>
                <td>Center 1</td>
                <td>187.47</td>
                <td>FR</td>
                <td></td>
                <td></td>
                <td>Nice</td>
                <td></td>
                <td>43.700935</td>
                <td>7.268391</td>
            </tr>
        </tbody>
    </table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>centerLatitude</th>
            <th>centerLongitude</th>
            <th>centerName</th>
            <th>weight</th>
            <th>volume</th>
            <th>revenue</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>43.81293</td>
            <td>4.939257</td>
            <td>Center 1</td>
            <td>1953564</td>
            <td>5583</td>
            <td>4187250</td>
        </tr>
        <tr>
            <td>48.85889</td>
            <td>2.320041</td>
            <td>Center 2</td>
            <td>3141966</td>
            <td>8976</td>
            <td>6732000</td>
        </tr>
        <tr>
            <td>47.13300</td>
            <td>-1.024814</td>
            <td>Center 3</td>
            <td>910299</td>
            <td>2602</td>
            <td>1951500</td>
        </tr>
    </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>latitude</th>
            <th>longitude</th>
            <th>weight</th>
            <th>volume</th>
            <th>revenue</th>
            <th>centerLatitude</th>
            <th>centerLongitude</th>
            <th>centerName</th>
            <th>distance</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Paris</td>
            <td>48.856614</td>
            <td>2.352222</td>
            <td>1120311</td>
            <td>3201</td>
            <td>2400750</td>
            <td>48.856614</td>
            <td>2.352222</td>
            <td>Center 2</td>
            <td>0.00</td>
        </tr>
        <tr>
            <td>Marseille</td>
            <td>43.296482</td>
            <td>5.369780</td>
            <td>426258</td>
            <td>1218</td>
            <td>913500</td>
            <td>43.813581</td>
            <td>4.939038</td>
            <td>Center 1</td>
            <td>67.16</td>
        </tr>
        <tr>
            <td>Lyon</td>
            <td>45.764043</td>
            <td>4.835659</td>
            <td>248172</td>
            <td>709</td>
            <td>531750</td>
            <td>43.813581</td>
            <td>4.939038</td>
            <td>Center 1</td>
            <td>217.03</td>
        </tr>
        <tr>
            <td>Toulouse</td>
            <td>43.604652</td>
            <td>1.444209</td>
            <td>226659</td>
            <td>648</td>
            <td>486000</td>
            <td>43.813581</td>
            <td>4.939038</td>
            <td>Center 1</td>
            <td>281.85</td>
        </tr>
        <tr>
            <td>Nice</td>
            <td>43.710173</td>
            <td>7.261953</td>
            <td>171810</td>
            <td>491</td>
            <td>368250</td>
            <td>43.813581</td>
            <td>4.939038</td>
            <td>Center 1</td>
            <td>186.89</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>centerLatitude</th>
            <th>centerLongitude</th>
            <th>centerName</th>
            <th>weight</th>
            <th>volume</th>
            <th>revenue</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>43.813581</td>
            <td>4.939038</td>
            <td>Center 1</td>
            <td>1953564</td>
            <td>5583</td>
            <td>4187250</td>
        </tr>
        <tr>
            <td>48.856614</td>
            <td>2.352222</td>
            <td>Center 2</td>
            <td>3141966</td>
            <td>8976</td>
            <td>6732000</td>
        </tr>
        <tr>
            <td>47.134929</td>
            <td>-1.028559</td>
            <td>Center 3</td>
            <td>910299</td>
            <td>2602</td>
            <td>1951500</td>
        </tr>
    </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\advanced_center_of_gravity.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr>
            <th>centerLatitude</th>
            <th>centerLongitude</th>
            <th>centerName</th>
            <th>productGroup</th>
            <th>weight</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>40.914187</td>
            <td>-1.298175</td>
            <td>Fixed_Center_ES_1</td>
            <td>Home Appliances</td>
            <td>53054.63</td>
        </tr>
        <tr>
            <td>40.914187</td>
            <td>-1.298175</td>
            <td>Fixed_Center_ES_1</td>
            <td>Industrial Goods</td>
            <td>43082.09</td>
        </tr>
        <tr>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>Home Appliances</td>
            <td>65965.33</td>
        </tr>
        <tr>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>Industrial Goods</td>
            <td>62561.22</td>
        </tr>
        <tr>
            <td>42.818199</td>
            <td>-1.644009</td>
            <td>Fixed_Center_ES_3</td>
            <td>Home Appliances</td>
            <td>59364.43</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>sourceName</th>
            <th>sourceLatitude</th>
            <th>sourceLongitude</th>
            <th>centerLatitude</th>
            <th>centerLongitude</th>
            <th>centerName</th>
            <th>distance</th>
            <th>layer</th>
            <th>relationLayer</th>
            <th>productGroup</th>
            <th>weight</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Cadiz</td>
            <td>36.529744</td>
            <td>-6.292898</td>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>163.65</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Industrial Goods</td>
            <td>62561.22</td>
        </tr>
        <tr>
            <td>Valencia</td>
            <td>39.469707</td>
            <td>-0.376335</td>
            <td>40.914187</td>
            <td>-1.298175</td>
            <td>Fixed_Center_ES_1</td>
            <td>178.69</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Home Appliances</td>
            <td>53054.63</td>
        </tr>
        <tr>
            <td>Valencia</td>
            <td>39.469707</td>
            <td>-0.376335</td>
            <td>40.914187</td>
            <td>-1.298175</td>
            <td>Fixed_Center_ES_1</td>
            <td>178.69</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Industrial Goods</td>
            <td>43082.09</td>
        </tr>
        <tr>
            <td>Valencia</td>
            <td>39.469707</td>
            <td>-0.376335</td>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>455.72</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Home Appliances</td>
            <td>65965.33</td>
        </tr>
        <tr>
            <td>Valencia</td>
            <td>39.469707</td>
            <td>-0.376335</td>
            <td>42.818199</td>
            <td>-1.644009</td>
            <td>Fixed_Center_ES_3</td>
            <td>387.16</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Home Appliances</td>
            <td>59364.43</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>customerName</th>
            <th>customerLatitude</th>
            <th>customerLongitude</th>
            <th>weight</th>
            <th>productGroup</th>
            <th>centerLatitude</th>
            <th>centerLongitude</th>
            <th>centerName</th>
            <th>distance</th>
            <th>layer</th>
            <th>relationLayer</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Customer_ES_1</td>
            <td>37.234309</td>
            <td>-3.823843</td>
            <td>722.12</td>
            <td>Industrial Goods</td>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>69.51</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
        <tr>
            <td>Customer_ES_2</td>
            <td>43.266473</td>
            <td>-3.892813</td>
            <td>2864.67</td>
            <td>Industrial Goods</td>
            <td>42.818199</td>
            <td>-1.644009</td>
            <td>Fixed_Center_ES_3</td>
            <td>189.42</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
        <tr>
            <td>Customer_ES_3</td>
            <td>42.242730</td>
            <td>0.197584</td>
            <td>1032.67</td>
            <td>Industrial Goods</td>
            <td>41.378327</td>
            <td>1.247607</td>
            <td>Center 5</td>
            <td>129.66</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
        <tr>
            <td>Customer_ES_4</td>
            <td>41.614761</td>
            <td>0.626784</td>
            <td>998.14</td>
            <td>Industrial Goods</td>
            <td>41.378327</td>
            <td>1.247607</td>
            <td>Center 5</td>
            <td>58.00</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
        <tr>
            <td>Customer_ES_5</td>
            <td>42.284221</td>
            <td>-8.608599</td>
            <td>949.19</td>
            <td>Industrial Goods</td>
            <td>41.531362</td>
            <td>-5.664006</td>
            <td>Center 4</td>
            <td>257.64</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
    </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr>
            <th>centerLatitude</th>
            <th>centerLongitude</th>
            <th>centerName</th>
            <th>productGroup</th>
            <th>weight</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>40.914187</td>
            <td>-1.298175</td>
            <td>Fixed_Center_ES_1</td>
            <td>Home Appliances</td>
            <td>58346.89</td>
        </tr>
        <tr>
            <td>40.914187</td>
            <td>-1.298175</td>
            <td>Fixed_Center_ES_1</td>
            <td>Industrial Goods</td>
            <td>52491.48</td>
        </tr>
        <tr>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>Home Appliances</td>
            <td>63512.75</td>
        </tr>
        <tr>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>Industrial Goods</td>
            <td>65843.61</td>
        </tr>
        <tr>
            <td>42.818199</td>
            <td>-1.644009</td>
            <td>Fixed_Center_ES_3</td>
            <td>Home Appliances</td>
            <td>52366.79</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>sourceName</th>
            <th>sourceLatitude</th>
            <th>sourceLongitude</th>
            <th>centerLatitude</th>
            <th>centerLongitude</th>
            <th>centerName</th>
            <th>distance</th>
            <th>layer</th>
            <th>relationLayer</th>
            <th>productGroup</th>
            <th>weight</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Cadiz</td>
            <td>36.529744</td>
            <td>-6.292898</td>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>163.65</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Industrial Goods</td>
            <td>65843.61</td>
        </tr>
        <tr>
            <td>Valencia</td>
            <td>39.469707</td>
            <td>-0.376335</td>
            <td>40.914187</td>
            <td>-1.298175</td>
            <td>Fixed_Center_ES_1</td>
            <td>178.69</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Home Appliances</td>
            <td>58346.89</td>
        </tr>
        <tr>
            <td>Valencia</td>
            <td>39.469707</td>
            <td>-0.376335</td>
            <td>40.914187</td>
            <td>-1.298175</td>
            <td>Fixed_Center_ES_1</td>
            <td>178.69</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Industrial Goods</td>
            <td>52491.48</td>
        </tr>
        <tr>
            <td>Valencia</td>
            <td>39.469707</td>
            <td>-0.376335</td>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>455.72</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Home Appliances</td>
            <td>63512.75</td>
        </tr>
        <tr>
            <td>Valencia</td>
            <td>39.469707</td>
            <td>-0.376335</td>
            <td>42.818199</td>
            <td>-1.644009</td>
            <td>Fixed_Center_ES_3</td>
            <td>387.16</td>
            <td>Source</td>
            <td>Inbound</td>
            <td>Home Appliances</td>
            <td>52366.79</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>customerName</th>
            <th>customerLatitude</th>
            <th>customerLongitude</th>
            <th>weight</th>
            <th>productGroup</th>
            <th>centerLatitude</th>
            <th>centerLongitude</th>
            <th>centerName</th>
            <th>distance</th>
            <th>layer</th>
            <th>relationLayer</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Customer_ES_1</td>
            <td>37.234309</td>
            <td>-3.823843</td>
            <td>722.12</td>
            <td>Industrial Goods</td>
            <td>37.018365</td>
            <td>-4.559665</td>
            <td>Fixed_Center_ES_2</td>
            <td>69.51</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
        <tr>
            <td>Customer_ES_2</td>
            <td>43.266473</td>
            <td>-3.892813</td>
            <td>2864.67</td>
            <td>Industrial Goods</td>
            <td>42.818199</td>
            <td>-1.644009</td>
            <td>Fixed_Center_ES_3</td>
            <td>189.42</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
        <tr>
            <td>Customer_ES_3</td>
            <td>42.242730</td>
            <td>0.197584</td>
            <td>1032.67</td>
            <td>Industrial Goods</td>
            <td>41.378327</td>
            <td>1.247607</td>
            <td>Center 5</td>
            <td>129.66</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
        <tr>
            <td>Customer_ES_4</td>
            <td>41.614761</td>
            <td>0.626784</td>
            <td>998.14</td>
            <td>Industrial Goods</td>
            <td>41.378327</td>
            <td>1.247607</td>
            <td>Center 5</td>
            <td>58.00</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
        <tr>
            <td>Customer_ES_5</td>
            <td>42.284221</td>
            <td>-8.608599</td>
            <td>949.19</td>
            <td>Industrial Goods</td>
            <td>41.531362</td>
            <td>-5.664006</td>
            <td>Center 4</td>
            <td>257.64</td>
            <td>Customer</td>
            <td>Outbound</td>
        </tr>
    </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\nearest_warehouses.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr>
            <th>warehouseName</th>
            <th>warehouseCountry</th>
            <th>warehouseState</th>
            <th>warehousePostalCode</th>
            <th>warehouseCity</th>
            <th>warehouseStreet</th>
            <th>warehouseParsedLatitude</th>
            <th>warehouseParsedLongitude</th>
            <th>warehouseStatus</th>
            <th>customerName</th>
            <th>customerCountry</th>
            <th>customerState</th>
            <th>customerPostalCode</th>
            <th>customerCity</th>
            <th>customerStreet</th>
            <th>customerLatitude</th>
            <th>customerLongitude</th>
            <th>distance</th>
            <th>layer</th>
            <th>relationLayer</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Jersey City</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>Jersey City</td>
            <td></td>
            <td>40.721568</td>
            <td>-74.047455</td>
            <td>ok</td>
            <td>New York</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>New York</td>
            <td></td>
            <td>40.712728</td>
            <td>-74.006015</td>
            <td>3.63</td>
            <td>6.63</td>
            <td>8.81</td>
        </tr>
        <tr>
            <td>Newark</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>Newark</td>
            <td></td>
            <td>40.735657</td>
            <td>-74.172367</td>
            <td>ok</td>
            <td>New York</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>New York</td>
            <td></td>
            <td>40.712728</td>
            <td>-74.006015</td>
            <td>14.25</td>
            <td>17.53</td>
            <td>16.12</td>
        </tr>
        <tr>
            <td>Buffalo</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>Buffalo</td>
            <td></td>
            <td>42.886717</td>
            <td>-78.878392</td>
            <td>ok</td>
            <td>New York</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>New York</td>
            <td></td>
            <td>40.712728</td>
            <td>-74.006015</td>
            <td>470.59</td>
            <td>599.43</td>
            <td>412.43</td>
        </tr>
        <tr>
            <td>Aurora</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>Aurora</td>
            <td></td>
            <td>41.757170</td>
            <td>-88.314754</td>
            <td>ok</td>
            <td>Chicago</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>Chicago</td>
            <td></td>
            <td>41.875562</td>
            <td>-87.624421</td>
            <td>58.70</td>
            <td>64.84</td>
            <td>50.10</td>
        </tr>
        <tr>
            <td>Madison</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>Madison</td>
            <td></td>
            <td>43.074761</td>
            <td>-89.383761</td>
            <td>ok</td>
            <td>Chicago</td>
            <td>US</td>
            <td></td>
            <td></td>
            <td>Chicago</td>
            <td></td>
            <td>41.875562</td>
            <td>-87.624421</td>
            <td>196.46</td>
            <td>237.40</td>
            <td>151.50</td>
        </tr>
    </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr>
            <th>warehouseName</th>
            <th>warehouseLatitude</th>
            <th>warehouseLongitude</th>
            <th>customerName</th>
            <th>customerLatitude</th>
            <th>customerLongitude</th>
            <th>beeline</th>
            <th>dist</th>
            <th>duration</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Stockton</td>
            <td>40.407883</td>
            <td>-74.978224</td>
            <td>New York</td>
            <td>43.156168</td>
            <td>-75.844995</td>
            <td>313.93</td>
            <td>398.37</td>
            <td>277.23</td>
        </tr>
        <tr>
            <td>Newark</td>
            <td>40.735657</td>
            <td>-74.172367</td>
            <td>New York</td>
            <td>43.156168</td>
            <td>-75.844995</td>
            <td>302.60</td>
            <td>413.33</td>
            <td>277.89</td>
        </tr>
        <tr>
            <td>Jersey City</td>
            <td>40.728158</td>
            <td>-74.077642</td>
            <td>New York</td>
            <td>43.156168</td>
            <td>-75.844995</td>
            <td>307.00</td>
            <td>421.95</td>
            <td>284.73</td>
        </tr>
        <tr>
            <td>Fort Wayne</td>
            <td>41.079990</td>
            <td>-85.138601</td>
            <td>Chicago</td>
            <td>41.875555</td>
            <td>-87.624421</td>
            <td>225.18</td>
            <td>258.14</td>
            <td>184.70</td>
        </tr>
        <tr>
            <td>Saint Paul</td>
            <td>39.428105</td>
            <td>-85.628309</td>
            <td>Chicago</td>
            <td>41.875555</td>
            <td>-87.624421</td>
            <td>320.01</td>
            <td>352.41</td>
            <td>227.72</td>
        </tr>
    </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\network_design_plus.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr style="text-align: right;">
            <th>name</th>
            <th>country</th>
            <th>state</th>
            <th>postalCode</th>
            <th>city</th>
            <th>street</th>
            <th>parsedLatitude</th>
            <th>parsedLongitude</th>
            <th>assignedWeight</th>
            <th>assignedVolume</th>
            <th>assignedNumberOfShipments</th>
            <th>warehouseFixedCosts</th>
            <th>warehouseVariableCosts</th>
            <th>stepwiseFixedCosts</th>
            <th>stepwiseVariableCosts</th>
            <th>minWeight</th>
            <th>maxWeight</th>
            <th>minVolume</th>
            <th>maxVolume</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Whs_Darmstadt</td>
            <td>DE</td>
            <td></td>
            <td></td>
            <td>Darmstadt</td>
            <td></td>
            <td>49.872775</td>
            <td>8.651177</td>
            <td>4545455.34</td>
            <td>15859.61</td>
            <td>1563</td>
            <td>280000</td>
            <td>246304</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>8326000</td>
            <td>0</td>
            <td>29500</td>
        </tr>
        <tr>
            <td>Whs_Fulda</td>
            <td>DE</td>
            <td></td>
            <td></td>
            <td>Fulda</td>
            <td></td>
            <td>50.554233</td>
            <td>9.677045</td>
            <td>4293018.98</td>
            <td>16002.84</td>
            <td>1412</td>
            <td>730000</td>
            <td>233854</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>27599000</td>
            <td>0</td>
            <td>97600</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>factoryName</th>
            <th>factoryCountry</th>
            <th>factoryState</th>
            <th>factoryPostalCode</th>
            <th>factoryCity</th>
            <th>factoryStreet</th>
            <th>factoryParsedLatitude</th>
            <th>factoryParsedLongitude</th>
            <th>warehouseName</th>
            <th>warehouseCountry</th>
            <th>warehouseState</th>
            <th>warehousePostalCode</th>
            <th>warehouseCity</th>
            <th>warehouseStreet</th>
            <th>warehouseParsedLatitude</th>
            <th>warehouseParsedLongitude</th>
            <th>assignedWeight</th>
            <th>assignedVolume</th>
            <th>assignedNumberOfShipments</th>
            <th>warehouseFixedCosts</th>
            <th>warehouseVariableCosts</th>
            <th>stepwiseFixedCosts</th>
            <th>stepwiseVariableCosts</th>
            <th>minWeight</th>
            <th>maxWeight</th>
            <th>minVolume</th>
            <th>maxVolume</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Barcelona</td>
            <td>ES</td>
            <td></td>
            <td></td>
            <td>Barcelona</td>
            <td></td>
            <td>41.382894</td>
            <td>2.177432</td>
            <td>Whs_Darmstadt</td>
            <td>DE</td>
            <td></td>
            <td></td>
            <td>Darmstadt</td>
            <td></td>
            <td>49.872775</td>
            <td>8.651177</td>
            <td>713124.33</td>
            <td>2451.55</td>
            <td>214</td>
            <td>545.10</td>
            <td>18000.00</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>8326000</td>
            <td>0</td>
            <td>29500</td>
        </tr>
        <tr>
            <td>Barcelona</td>
            <td>ES</td>
            <td></td>
            <td></td>
            <td>Barcelona</td>
            <td></td>
            <td>41.382894</td>
            <td>2.177432</td>
            <td>Whs_Fulda</td>
            <td>DE</td>
            <td></td>
            <td></td>
            <td>Fulda</td>
            <td></td>
            <td>50.554233</td>
            <td>9.677045</td>
            <td>2672879.01</td>
            <td>9795.59</td>
            <td>710</td>
            <td>433.68</td>
            <td>77200.00</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>27599000</td>
            <td>0</td>
            <td>97600</td>
        </tr>
        <tr>
            <td>ImportGate_HamburgHarbour</td>
            <td>DE</td>
            <td></td>
            <td>20097</td>
            <td>Hamburg</td>
            <td></td>
            <td>53.546774</td>
            <td>10.023524</td>
            <td>Whs_Darmstadt</td>
            <td>DE</td>
            <td></td>
            <td></td>
            <td>Darmstadt</td>
            <td></td>
            <td>49.872775</td>
            <td>8.651177</td>
            <td>713124.33</td>
            <td>2451.55</td>
            <td>214</td>
            <td>545.10</td>
            <td>18000.00</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>8326000</td>
            <td>0</td>
            <td>29500</td>
        </tr>
        <tr>
            <td>ImportGate_HamburgHarbour</td>
            <td>DE</td>
            <td></td>
            <td>20097</td>
            <td>Hamburg</td>
            <td></td>
            <td>53.546774</td>
            <td>10.023524</td>
            <td>Whs_Fulda</td>
            <td>DE</td>
            <td></td>
            <td></td>
            <td>Fulda</td>
            <td></td>
            <td>50.554233</td>
            <td>9.677045</td>
            <td>2672879.01</td>
            <td>9795.59</td>
            <td>710</td>
            <td>433.68</td>
            <td>77200.00</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>27599000</td>
            <td>0</td>
            <td>97600</td>
        </tr>
        <tr>
            <td>Lyon</td>
            <td>FR</td>
            <td></td>
            <td></td>
            <td>Lyon</td>
            <td></td>
            <td>45.757814</td>
            <td>4.832011</td>
            <td>Whs_Darmstadt</td>
            <td>DE</td>
            <td></td>
            <td></td>
            <td>Darmstadt</td>
            <td></td>
            <td>49.872775</td>
            <td>8.651177</td>
            <td>631423.81</td>
            <td>2049.55</td>
            <td>137</td>
            <td>700.69</td>
            <td>24798.04</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>8326000</td>
            <td>0</td>
            <td>29500</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>country</th>
            <th>state</th>
            <th>postalCode</th>
            <th>city</th>
            <th>street</th>
            <th>parsedLatitude</th>
            <th>parsedLongitude</th>
            <th>weight</th>
            <th>volume</th>
            <th>numberOfShipments</th>
            <th>warehouseName</th>
            <th>distance</th>
            <th>factoryName</th>
            <th>outboundTransportCosts</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Customer_0001</td>
            <td>DE</td>
            <td></td>
            <td>24647</td>
            <td>Wasbek</td>
            <td></td>
            <td>54.073959</td>
            <td>9.898631</td>
            <td>6055.52</td>
            <td>18.31</td>
            <td>54</td>
            <td>Whs_Fulda</td>
            <td>509.16</td>
            <td>ImportGate_HamburgHarbour</td>
            <td>17077.35</td>
        </tr>
        <tr>
            <td>Customer_0002</td>
            <td>DE</td>
            <td></td>
            <td>22962</td>
            <td>Siek</td>
            <td></td>
            <td>53.634963</td>
            <td>10.297829</td>
            <td>5036.28</td>
            <td>17.52</td>
            <td>45</td>
            <td>Whs_Darmstadt</td>
            <td>563.40</td>
            <td>ImportGate_HamburgHarbour</td>
            <td>14761.93</td>
        </tr>
        <tr>
            <td>Customer_0003</td>
            <td>DE</td>
            <td></td>
            <td>22145</td>
            <td>Stapelfeld</td>
            <td></td>
            <td>53.606944</td>
            <td>10.218915</td>
            <td>1183.32</td>
            <td>7.05</td>
            <td>13</td>
            <td>Whs_Fulda</td>
            <td>443.89</td>
            <td>Ulm</td>
            <td>1413.74</td>
        </tr>
        <tr>
            <td>Customer_0004</td>
            <td>DE</td>
            <td></td>
            <td>21035</td>
            <td>Hamburg</td>
            <td></td>
            <td>53.489606</td>
            <td>10.158170</td>
            <td>370.76</td>
            <td>2.87</td>
            <td>23</td>
            <td>Whs_Fulda</td>
            <td>426.47</td>
            <td>Poznan</td>
            <td>984.50</td>
        </tr>
        <tr>
            <td>Customer_0005</td>
            <td>DE</td>
            <td></td>
            <td>24113</td>
            <td>Kiel</td>
            <td></td>
            <td>54.291249</td>
            <td>10.094350</td>
            <td>3512.31</td>
            <td>14.48</td>
            <td>28</td>
            <td>Whs_Darmstadt</td>
            <td>651.41</td>
            <td>Poznan</td>
            <td>8482.27</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>kpiName</th>
            <th>kpiValue</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Value Target Function</td>
            <td>2110198</td>
        </tr>
        <tr>
            <td>Optimization Status</td>
            <td>optimal solution</td>
        </tr>
        <tr>
            <td>Total Costs</td>
            <td>2110198</td>
        </tr>
        <tr>
            <td>Transport Costs</td>
            <td>620040</td>
        </tr>
        <tr>
            <td>Factory Outbound Transport Costs</td>
            <td>316002</td>
        </tr>
    </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>latitude</th>
            <th>longitude</th>
            <th>minWeight</th>
            <th>maxWeight</th>
            <th>minVolume</th>
            <th>maxVolume</th>
            <th>assignedWeight</th>
            <th>assignedVolume</th>
            <th>assignedNumberOfShipments</th>
            <th>warehouseFixedCosts</th>
            <th>warehouseVariableCosts</th>
            <th>stepwiseFixedCosts</th>
            <th>stepwiseVariableCosts</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Whs_Darmstadt</td>
            <td>49.872825</td>
            <td>8.651193</td>
            <td>0</td>
            <td>8326000</td>
            <td>0</td>
            <td>29500</td>
            <td>4289385.10</td>
            <td>15122.93</td>
            <td>1529</td>
            <td>280000</td>
            <td>232617</td>
            <td>0</td>
            <td>0</td>
        </tr>
        <tr>
            <td>Whs_Fulda</td>
            <td>50.555810</td>
            <td>9.680845</td>
            <td>0</td>
            <td>27599000</td>
            <td>0</td>
            <td>97600</td>
            <td>4549089.22</td>
            <td>16739.52</td>
            <td>1446</td>
            <td>730000</td>
            <td>247542</td>
            <td>0</td>
            <td>0</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>factoryName</th>
            <th>factoryLatitude</th>
            <th>factoryLongitude</th>
            <th>warehouseName</th>
            <th>warehouseLatitude</th>
            <th>warehouseLongitude</th>
            <th>weight</th>
            <th>volume</th>
            <th>numberOfShipments</th>
            <th>distance</th>
            <th>inboundTransportCosts</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Barcelona</td>
            <td>41.385064</td>
            <td>2.173404</td>
            <td>Whs_Darmstadt</td>
            <td>49.872825</td>
            <td>8.651193</td>
            <td>425787.20</td>
            <td>1409.07</td>
            <td>172</td>
            <td>1389.49</td>
            <td>29035.89</td>
        </tr>
        <tr>
            <td>Barcelona</td>
            <td>41.385064</td>
            <td>2.173404</td>
            <td>Whs_Fulda</td>
            <td>50.555810</td>
            <td>9.680845</td>
            <td>118441.60</td>
            <td>431.10</td>
            <td>25</td>
            <td>1523.40</td>
            <td>9454.44</td>
        </tr>
        <tr>
            <td>ImportGate_HamburgHarbour</td>
            <td>53.548038</td>
            <td>10.017699</td>
            <td>Whs_Darmstadt</td>
            <td>49.872825</td>
            <td>8.651193</td>
            <td>486491.73</td>
            <td>1663.15</td>
            <td>169</td>
            <td>545.15</td>
            <td>12500.00</td>
        </tr>
        <tr>
            <td>ImportGate_HamburgHarbour</td>
            <td>53.548038</td>
            <td>10.017699</td>
            <td>Whs_Darmstadt</td>
            <td>49.872825</td>
            <td>8.651193</td>
            <td>226632.60</td>
            <td>788.40</td>
            <td>45</td>
            <td>545.15</td>
            <td>5500.00</td>
        </tr>
        <tr>
            <td>ImportGate_HamburgHarbour</td>
            <td>53.548038</td>
            <td>10.017699</td>
            <td>Whs_Fulda</td>
            <td>50.555810</td>
            <td>9.680845</td>
            <td>2088048.08</td>
            <td>7803.30</td>
            <td>596</td>
            <td>433.57</td>
            <td>64800.00</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>latitude</th>
            <th>longitude</th>
            <th>weight</th>
            <th>volume</th>
            <th>numberOfShipments</th>
            <th>warehouseName</th>
            <th>distance</th>
            <th>factoryName</th>
            <th>outboundTransportCosts</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Customer_0001</td>
            <td>54.072431</td>
            <td>9.895834</td>
            <td>6055.52</td>
            <td>18.31</td>
            <td>54</td>
            <td>Whs_Fulda</td>
            <td>508.69</td>
            <td>ImportGate_HamburgHarbour</td>
            <td>17064.58</td>
        </tr>
        <tr>
            <td>Customer_0002</td>
            <td>53.634444</td>
            <td>10.298056</td>
            <td>5036.28</td>
            <td>17.52</td>
            <td>45</td>
            <td>Whs_Darmstadt</td>
            <td>563.33</td>
            <td>ImportGate_HamburgHarbour</td>
            <td>14760.49</td>
        </tr>
        <tr>
            <td>Customer_0003</td>
            <td>53.605029</td>
            <td>10.217829</td>
            <td>1183.32</td>
            <td>7.05</td>
            <td>13</td>
            <td>Whs_Fulda</td>
            <td>443.35</td>
            <td>Ulm</td>
            <td>1412.30</td>
        </tr>
        <tr>
            <td>Customer_0004</td>
            <td>53.487313</td>
            <td>10.153583</td>
            <td>370.76</td>
            <td>2.87</td>
            <td>23</td>
            <td>Whs_Fulda</td>
            <td>425.84</td>
            <td>Poznan</td>
            <td>983.27</td>
        </tr>
        <tr>
            <td>Customer_0005</td>
            <td>54.281305</td>
            <td>10.080690</td>
            <td>3512.31</td>
            <td>14.48</td>
            <td>28</td>
            <td>Whs_Darmstadt</td>
            <td>649.76</td>
            <td>Poznan</td>
            <td>8466.30</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>kpiName</th>
            <th>kpiValue</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Value Target Function</td>
            <td>2116448</td>
        </tr>
        <tr>
            <td>Optimization Status</td>
            <td>optimal solution</td>
        </tr>
        <tr>
            <td>Total Costs</td>
            <td>2116448</td>
        </tr>
        <tr>
            <td>Transport Costs</td>
            <td>626290</td>
        </tr>
        <tr>
            <td>Factory Outbound Transport Costs</td>
            <td>317033</td>
        </tr>
    </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\location_planning.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>country</th>
            <th>state</th>
            <th>postalCode</th>
            <th>city</th>
            <th>street</th>
            <th>assignedWeight</th>
            <th>assignedVolume</th>
            <th>assignedNumberOfShipments</th>
            <th>warehouseFixedCosts</th>
            <th>warehouseVariableCosts</th>
            <th>minWeight</th>
            <th>maxWeight</th>
            <th>minVolume</th>
            <th>maxVolume</th>
            <th>latitude</th>
            <th>longitude</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Moscow</td>
            <td>RU</td>
            <td></td>
            <td></td>
            <td>Moscow</td>
            <td></td>
            <td>43515343</td>
            <td>144090.01</td>
            <td>3478</td>
            <td>833138</td>
            <td>87319</td>
            <td>0</td>
            <td>44434000</td>
            <td>0</td>
            <td>148113.33</td>
            <td>55.750541</td>
            <td>37.617478</td>
        </tr>
        <tr>
            <td>Istanbul</td>
            <td>TR</td>
            <td></td>
            <td></td>
            <td>Istanbul</td>
            <td></td>
            <td>14000144</td>
            <td>47347.24</td>
            <td>1370</td>
            <td>891450</td>
            <td>28095</td>
            <td>0</td>
            <td>47544000</td>
            <td>0</td>
            <td>158480.00</td>
            <td>41.006381</td>
            <td>28.975872</td>
        </tr>
        <tr>
            <td>London</td>
            <td>GB</td>
            <td></td>
            <td></td>
            <td>London</td>
            <td></td>
            <td>26600711</td>
            <td>85779.10</td>
            <td>2362</td>
            <td>835500</td>
            <td>53373</td>
            <td>0</td>
            <td>44560000</td>
            <td>0</td>
            <td>148533.33</td>
            <td>51.507446</td>
            <td>-0.127765</td>
        </tr>
        <tr>
            <td>Madrid</td>
            <td>ES</td>
            <td></td>
            <td></td>
            <td>Madrid</td>
            <td></td>
            <td>8608197</td>
            <td>28392.71</td>
            <td>883</td>
            <td>852750</td>
            <td>17273</td>
            <td>0</td>
            <td>45480000</td>
            <td>0</td>
            <td>151600.00</td>
            <td>40.416705</td>
            <td>-3.703582</td>
        </tr>
        <tr>
            <td>Wien</td>
            <td>AT</td>
            <td></td>
            <td></td>
            <td>Wien</td>
            <td></td>
            <td>37484704</td>
            <td>124901.73</td>
            <td>3060</td>
            <td>753255</td>
            <td>75219</td>
            <td>0</td>
            <td>40173600</td>
            <td>0</td>
            <td>133912.00</td>
            <td>48.208354</td>
            <td>16.372504</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>country</th>
            <th>state</th>
            <th>postalCode</th>
            <th>city</th>
            <th>street</th>
            <th>weight</th>
            <th>volume</th>
            <th>numberOfShipments</th>
            <th>warehouseName</th>
            <th>customerTransportCosts</th>
            <th>distance</th>
            <th>transportRule</th>
            <th>parsedCountry</th>
            <th>latitude</th>
            <th>longitude</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Moscow</td>
            <td>RU</td>
            <td></td>
            <td></td>
            <td>Moscow</td>
            <td></td>
            <td>13175</td>
            <td>44.21</td>
            <td>1205</td>
            <td>Moscow</td>
            <td>96352</td>
            <td>0.00</td>
            <td></td>
            <td>RU</td>
            <td>55.750541</td>
            <td>37.617478</td>
        </tr>
        <tr>
            <td>Istanbul</td>
            <td>TR</td>
            <td></td>
            <td></td>
            <td>Istanbul</td>
            <td></td>
            <td>9695</td>
            <td>33.20</td>
            <td>930</td>
            <td>Istanbul</td>
            <td>64105</td>
            <td>0.00</td>
            <td></td>
            <td>TR</td>
            <td>41.006381</td>
            <td>28.975872</td>
        </tr>
        <tr>
            <td>London</td>
            <td>GB</td>
            <td></td>
            <td></td>
            <td>London</td>
            <td></td>
            <td>12930</td>
            <td>39.78</td>
            <td>854</td>
            <td>London</td>
            <td>110371</td>
            <td>0.00</td>
            <td>Customer Country ISO2: * Warehouse Country ISO2:</td>
            <td>GB</td>
            <td>51.507446</td>
            <td>-0.127765</td>
        </tr>
        <tr>
            <td>Sankt Petersburg</td>
            <td>RU</td>
            <td></td>
            <td></td>
            <td>Sankt Petersburg</td>
            <td></td>
            <td>14729</td>
            <td>49.43</td>
            <td>519</td>
            <td>Moscow</td>
            <td>871468</td>
            <td>824.95</td>
            <td></td>
            <td>RU</td>
            <td>59.938732</td>
            <td>30.316229</td>
        </tr>
        <tr>
            <td>Berlin</td>
            <td>DE</td>
            <td></td>
            <td></td>
            <td>Berlin</td>
            <td></td>
            <td>12315</td>
            <td>40.11</td>
            <td>351</td>
            <td>Wien</td>
            <td>500705</td>
            <td>679.57</td>
            <td></td>
            <td>DE</td>
            <td>52.510885</td>
            <td>13.398937</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>kpiName</th>
            <th>kpiValue</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Value Target Function</td>
            <td>1761</td>
        </tr>
        <tr>
            <td>Transport Costs</td>
            <td>12450791</td>
        </tr>
        <tr>
            <td>Variable Warehouse Costs</td>
            <td>293429</td>
        </tr>
        <tr>
            <td>Fixed Warehouse Costs</td>
            <td>4929247</td>
        </tr>
        <tr>
            <td>Optimal Number of Warehouses</td>
            <td>6</td>
        </tr>
    </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>latitude</th>
            <th>longitude</th>
            <th>minWeight</th>
            <th>maxWeight</th>
            <th>minVolume</th>
            <th>maxVolume</th>
            <th>assignedWeight</th>
            <th>assignedVolume</th>
            <th>assignedNumberOfShipments</th>
            <th>warehouseFixedCosts</th>
            <th>warehouseVariableCosts</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Moscow</td>
            <td>55.479205</td>
            <td>37.327330</td>
            <td>0</td>
            <td>44434000</td>
            <td>0</td>
            <td>148113.33</td>
            <td>43791303</td>
            <td>144265.12</td>
            <td>3633</td>
            <td>833138</td>
            <td>87871</td>
        </tr>
        <tr>
            <td>Istanbul</td>
            <td>41.076602</td>
            <td>29.052495</td>
            <td>0</td>
            <td>47544000</td>
            <td>0</td>
            <td>158480.00</td>
            <td>19011337</td>
            <td>63611.75</td>
            <td>1822</td>
            <td>891450</td>
            <td>38150</td>
        </tr>
        <tr>
            <td>London</td>
            <td>51.507322</td>
            <td>-0.127647</td>
            <td>0</td>
            <td>44560000</td>
            <td>0</td>
            <td>148533.33</td>
            <td>28031461</td>
            <td>90213.70</td>
            <td>2475</td>
            <td>835500</td>
            <td>56243</td>
        </tr>
        <tr>
            <td>Sankt Petersburg</td>
            <td>59.960674</td>
            <td>30.158655</td>
            <td>0</td>
            <td>45826000</td>
            <td>0</td>
            <td>152753.33</td>
            <td>11498602</td>
            <td>38569.07</td>
            <td>856</td>
            <td>859238</td>
            <td>23074</td>
        </tr>
        <tr>
            <td>Madrid</td>
            <td>39.262086</td>
            <td>-2.596882</td>
            <td>0</td>
            <td>45480000</td>
            <td>0</td>
            <td>151600.00</td>
            <td>8608197</td>
            <td>28392.71</td>
            <td>883</td>
            <td>852750</td>
            <td>17273</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>latitude</th>
            <th>longitude</th>
            <th>weight</th>
            <th>volume</th>
            <th>numberOfShipments</th>
            <th>warehouseName</th>
            <th>customerTransportCosts</th>
            <th>distance</th>
            <th>transportRule</th>
            <th>parsedCountry</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Moscow</td>
            <td>55.479205</td>
            <td>37.327330</td>
            <td>13175</td>
            <td>44.21</td>
            <td>1205</td>
            <td>Moscow</td>
            <td>96352</td>
            <td>0.00</td>
            <td></td>
            <td>RU</td>
        </tr>
        <tr>
            <td>Istanbul</td>
            <td>41.076602</td>
            <td>29.052495</td>
            <td>9695</td>
            <td>33.20</td>
            <td>930</td>
            <td>Istanbul</td>
            <td>64105</td>
            <td>0.00</td>
            <td></td>
            <td>TR</td>
        </tr>
        <tr>
            <td>London</td>
            <td>51.507322</td>
            <td>-0.127647</td>
            <td>12930</td>
            <td>39.78</td>
            <td>854</td>
            <td>London</td>
            <td>67671</td>
            <td>0.00</td>
            <td></td>
            <td>GB</td>
        </tr>
        <tr>
            <td>Sankt Petersburg</td>
            <td>59.960674</td>
            <td>30.158655</td>
            <td>14729</td>
            <td>49.43</td>
            <td>519</td>
            <td>Moscow</td>
            <td>43824</td>
            <td>0.00</td>
            <td></td>
            <td>RU</td>
        </tr>
        <tr>
            <td>Berlin</td>
            <td>52.519854</td>
            <td>13.438596</td>
            <td>12315</td>
            <td>40.11</td>
            <td>351</td>
            <td>Wien</td>
            <td>500705</td>
            <td>677.65</td>
            <td></td>
            <td>DE</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>kpiName</th>
            <th>kpiValue</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Value Target Function</td>
            <td>1745</td>
        </tr>
        <tr>
            <td>Transport Costs</td>
            <td>12197573</td>
        </tr>
        <tr>
            <td>Variable Warehouse Costs</td>
            <td>293429</td>
        </tr>
        <tr>
            <td>Fixed Warehouse Costs</td>
            <td>5025330</td>
        </tr>
        <tr>
            <td>Optimal Number of Warehouses</td>
            <td>6</td>
        </tr>
    </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\milkrun_optimization.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
    <thead>
        <tr>
            <th>id</th>
            <th>startDepotName</th>
            <th>startDepotCountry</th>
            <th>startDepotState</th>
            <th>startDepotPostalCode</th>
            <th>startDepotCity</th>
            <th>startDepotStreet</th>
            <th>startDepotLatitude</th>
            <th>startDepotLongitude</th>
            <th>endDepotName</th>
            <th>utilizationWeight</th>
            <th>volume</th>
            <th>utilizationVolume</th>
            <th>startTime</th>
            <th>startDay</th>
            <th>endTime</th>
            <th>endDay</th>
            <th>numberOfStops</th>
            <th>pallets</th>
            <th>utilizationPallets</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>0</td>
            <td>Depot_Tilburg</td>
            <td>NL</td>
            <td></td>
            <td>5015</td>
            <td>Tilburg</td>
            <td></td>
            <td>51.55624</td>
            <td>5.088601</td>
            <td>Depot_Tilburg</td>
            <td>73.35</td>
            <td>10</td>
            <td>58.82</td>
            <td>06:45:00</td>
            <td>day 0</td>
            <td>12:17:00</td>
            <td>day 0</td>
            <td>10</td>
            <td>13</td>
            <td>76.47</td>
        </tr>
        <tr>
            <td>1</td>
            <td>Depot_Tilburg</td>
            <td>NL</td>
            <td></td>
            <td>5015</td>
            <td>Tilburg</td>
            <td></td>
            <td>51.55624</td>
            <td>5.088601</td>
            <td>Depot_Tilburg</td>
            <td>95.55</td>
            <td>14</td>
            <td>82.35</td>
            <td>06:29:00</td>
            <td>day 0</td>
            <td>14:01:00</td>
            <td>day 0</td>
            <td>10</td>
            <td>16</td>
            <td>94.12</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Depot_Tilburg</td>
            <td>NL</td>
            <td></td>
            <td>5015</td>
            <td>Tilburg</td>
            <td></td>
            <td>51.55624</td>
            <td>5.088601</td>
            <td>Depot_Tilburg</td>
            <td>92.67</td>
            <td>14</td>
            <td>82.35</td>
            <td>06:00:00</td>
            <td>day 0</td>
            <td>09:57:00</td>
            <td>day 0</td>
            <td>10</td>
            <td>15</td>
            <td>88.24</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Depot_Tilburg</td>
            <td>NL</td>
            <td></td>
            <td>5015</td>
            <td>Tilburg</td>
            <td></td>
            <td>51.55624</td>
            <td>5.088601</td>
            <td>Depot_Tilburg</td>
            <td>79.93</td>
            <td>12</td>
            <td>70.59</td>
            <td>06:29:00</td>
            <td>day 0</td>
            <td>09:40:00</td>
            <td>day 0</td>
            <td>11</td>
            <td>14</td>
            <td>82.35</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Depot_Tilburg</td>
            <td>NL</td>
            <td></td>
            <td>5015</td>
            <td>Tilburg</td>
            <td></td>
            <td>51.55624</td>
            <td>5.088601</td>
            <td>Depot_Tilburg</td>
            <td>14.93</td>
            <td>2</td>
            <td>11.76</td>
            <td>02:18:00</td>
            <td>day 0</td>
            <td>09:53:00</td>
            <td>day 0</td>
            <td>1</td>
            <td>3</td>
            <td>17.65</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>id</th>
            <th>routeLeg</th>
            <th>startLocationCountry</th>
            <th>startLocationState</th>
            <th>startLocationPostalCode</th>
            <th>startLocationCity</th>
            <th>startLocationStreet</th>
            <th>startLocationLatitude</th>
            <th>startLocationLongitude</th>
            <th>startTime</th>
            <th>arrivalDay</th>
            <th>weight</th>
            <th>volume</th>
            <th>distance</th>
            <th>drivingDuration</th>
            <th>duration</th>
            <th>departureLocationName</th>
            <th>arrivalLoadingTime</th>
            <th>pallets</th>
            <th>pickupDelivery</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>0</td>
            <td>1</td>
            <td>NL</td>
            <td></td>
            <td>5015</td>
            <td>Tilburg</td>
            <td></td>
            <td>51.556240</td>
            <td>5.088601</td>
            <td>06:45:00</td>
            <td>day 0</td>
            <td>903</td>
            <td>2</td>
            <td>89.40</td>
            <td>107</td>
            <td>121</td>
            <td>Depot_Tilburg</td>
            <td>14</td>
            <td>3</td>
            <td>Pickup</td>
        </tr>
        <tr>
            <td>0</td>
            <td>2</td>
            <td>NL</td>
            <td></td>
            <td>5062</td>
            <td>Heukelom</td>
            <td></td>
            <td>51.614378</td>
            <td>6.033782</td>
            <td>08:46:00</td>
            <td>day 0</td>
            <td>1989</td>
            <td>5</td>
            <td>82.47</td>
            <td>99</td>
            <td>127</td>
            <td>NL_5062_Heukelom</td>
            <td>14</td>
            <td>6</td>
            <td>Delivery</td>
        </tr>
        <tr>
            <td>0</td>
            <td>3</td>
            <td>NL</td>
            <td></td>
            <td>5056</td>
            <td>Berkel-Enschot</td>
            <td></td>
            <td>51.585452</td>
            <td>5.142254</td>
            <td>10:39:00</td>
            <td>day 0</td>
            <td>1086</td>
            <td>3</td>
            <td>5.83</td>
            <td>7</td>
            <td>21</td>
            <td>NL_5056_Berkel-Enschot</td>
            <td>0</td>
            <td>3</td>
            <td></td>
        </tr>
        <tr>
            <td>0</td>
            <td>4</td>
            <td>NL</td>
            <td></td>
            <td>5015</td>
            <td>Tilburg</td>
            <td></td>
            <td>51.556240</td>
            <td>5.088601</td>
            <td>10:46:00</td>
            <td>day 0</td>
            <td>1297</td>
            <td>3</td>
            <td>0.00</td>
            <td>0</td>
            <td>17</td>
            <td>Depot_Tilburg</td>
            <td>17</td>
            <td>4</td>
            <td>Delivery</td>
        </tr>
        <tr>
            <td>0</td>
            <td>5</td>
            <td>NL</td>
            <td></td>
            <td>5021</td>
            <td>Tilburg</td>
            <td></td>
            <td>51.556240</td>
            <td>5.088601</td>
            <td>11:03:00</td>
            <td>day 0</td>
            <td>0</td>
            <td>0</td>
            <td>0.00</td>
            <td>0</td>
            <td>37</td>
            <td>NL_5021_Tilburg</td>
            <td>20</td>
            <td>0</td>
            <td>Pickup</td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>country</th>
            <th>state</th>
            <th>postalCode</th>
            <th>city</th>
            <th>street</th>
            <th>weight</th>
            <th>volume</th>
            <th>depot</th>
            <th>vehicleType</th>
            <th>serviceTime</th>
            <th>startTimeWindow</th>
            <th>endTimeWindow</th>
            <th>pallets</th>
            <th>pickupDelivery</th>
            <th>externalCosts</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>routeId</th>
      <th>name</th>
      <th>country</th>
      <th>state</th>
      <th>postalCode</th>
      <th>city</th>
      <th>street</th>
      <th>weight</th>
      <th>volume</th>
      <th>pallets</th>
      <th>pickupDelivery</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>depot_Depot_Tilburg</td>
      <td>NL</td>
      <td></td>
      <td>5015</td>
      <td>Tilburg</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>Depot_Tilburg</td>
      <td>NL</td>
      <td></td>
      <td>5015</td>
      <td>Tilburg</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>NL_5062_Heukelom</td>
      <td>NL</td>
      <td></td>
      <td>5062</td>
      <td>Heukelom</td>
      <td></td>
      <td>1086</td>
      <td>3.03</td>
      <td>3</td>
      <td>Pickup</td>
    </tr>
    <tr>
      <td>0</td>
      <td>NL_5056_Berkel-Enschot</td>
      <td>NL</td>
      <td></td>
      <td>5056</td>
      <td>Berkel-Enschot</td>
      <td></td>
      <td>903</td>
      <td>2.52</td>
      <td>3</td>
      <td>Delivery</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Depot_Tilburg</td>
      <td>NL</td>
      <td></td>
      <td>5015</td>
      <td>Tilburg</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>routeId</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>weight</th>
      <th>volume</th>
      <th>pallets</th>
      <th>pickupDelivery</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>depot_Depot_Tilburg</td>
      <td>51.556240</td>
      <td>5.088601</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>Depot_Tilburg</td>
      <td>51.556240</td>
      <td>5.088601</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>NL_5062_Heukelom</td>
      <td>51.614378</td>
      <td>6.033782</td>
      <td>1086</td>
      <td>3.03</td>
      <td>3</td>
      <td>Pickup</td>
    </tr>
    <tr>
      <td>0</td>
      <td>NL_5056_Berkel-Enschot</td>
      <td>51.585452</td>
      <td>5.142254</td>
      <td>903</td>
      <td>2.52</td>
      <td>3</td>
      <td>Delivery</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Depot_Tilburg</td>
      <td>51.556240</td>
      <td>5.088601</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>id</th>
      <th>startDepotName</th>
      <th>startDepotLatitude</th>
      <th>startDepotLongitude</th>
      <th>endDepotName</th>
      <th>endDepotLatitude</th>
      <th>endDepotLongitude</th>
      <th>vehicleType</th>
      <th>totalCosts</th>
      <th>distance</th>
      <th>utilizationWeight</th>
      <th>volume</th>
      <th>utilizationVolume</th>
      <th>startTime</th>
      <th>startDay</th>
      <th>endTime</th>
      <th>endDay</th>
      <th>numberOfStops</th>
      <th>pallets</th>
      <th>utilizationPallets</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>Truck_12t</td>
      <td>511.3156</td>
      <td>54.68</td>
      <td>92.63</td>
      <td>13</td>
      <td>76.47</td>
      <td>06:45:00</td>
      <td>day 0</td>
      <td>10:13:00</td>
      <td>day 0</td>
      <td>10</td>
      <td>17</td>
      <td>100.00</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>Truck_12t</td>
      <td>487.5781</td>
      <td>58.43</td>
      <td>98.33</td>
      <td>14</td>
      <td>82.35</td>
      <td>06:15:00</td>
      <td>day 0</td>
      <td>10:11:00</td>
      <td>day 0</td>
      <td>8</td>
      <td>16</td>
      <td>94.12</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>Truck_12t</td>
      <td>472.9489</td>
      <td>49.67</td>
      <td>93.17</td>
      <td>14</td>
      <td>82.35</td>
      <td>06:45:00</td>
      <td>day 0</td>
      <td>10:07:00</td>
      <td>day 0</td>
      <td>8</td>
      <td>16</td>
      <td>94.12</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>Truck_12t</td>
      <td>523.8239</td>
      <td>62.17</td>
      <td>91.80</td>
      <td>13</td>
      <td>76.47</td>
      <td>07:00:00</td>
      <td>day 0</td>
      <td>10:50:00</td>
      <td>day 0</td>
      <td>10</td>
      <td>16</td>
      <td>94.12</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>id</th>
      <th>routeLeg</th>
      <th>startLocationLatitude</th>
      <th>startLocationLongitude</th>
      <th>startTime</th>
      <th>startDay</th>
      <th>arrivalLocationName</th>
      <th>arrivalLocationLatitude</th>
      <th>arrivalLocationLongitude</th>
      <th>arrivalTime</th>
      <th>arrivalDay</th>
      <th>weight</th>
      <th>volume</th>
      <th>distance</th>
      <th>drivingDuration</th>
      <th>duration</th>
      <th>departureLocationName</th>
      <th>arrivalLoadingTime</th>
      <th>pallets</th>
      <th>pickupDelivery</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>1</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>06:45:00</td>
      <td>day 0</td>
      <td>NL_5037_Tilburg</td>
      <td>51.573709</td>
      <td>5.043931</td>
      <td>06:52:00</td>
      <td>day 0</td>
      <td>903</td>
      <td>2</td>
      <td>6.22</td>
      <td>7</td>
      <td>21</td>
      <td>Depot_Tilburg</td>
      <td>14</td>
      <td>3</td>
      <td>Pickup</td>
    </tr>
    <tr>
      <td>0</td>
      <td>2</td>
      <td>51.573709</td>
      <td>5.043931</td>
      <td>07:06:00</td>
      <td>day 0</td>
      <td>NL_5049_Tilburg</td>
      <td>51.592410</td>
      <td>5.073913</td>
      <td>07:13:00</td>
      <td>day 0</td>
      <td>1731</td>
      <td>4</td>
      <td>5.58</td>
      <td>7</td>
      <td>35</td>
      <td>NL_5037_Tilburg</td>
      <td>14</td>
      <td>6</td>
      <td>Pickup</td>
    </tr>
    <tr>
      <td>0</td>
      <td>3</td>
      <td>51.592410</td>
      <td>5.073913</td>
      <td>07:27:00</td>
      <td>day 0</td>
      <td>NL_5056_Berkel-Enschot</td>
      <td>51.585860</td>
      <td>5.141180</td>
      <td>07:35:00</td>
      <td>day 0</td>
      <td>2534</td>
      <td>6</td>
      <td>7.03</td>
      <td>8</td>
      <td>36</td>
      <td>NL_5049_Tilburg</td>
      <td>14</td>
      <td>9</td>
      <td>Delivery</td>
    </tr>
    <tr>
      <td>0</td>
      <td>4</td>
      <td>51.585860</td>
      <td>5.141180</td>
      <td>07:49:00</td>
      <td>day 0</td>
      <td>NL_5062_Heukelom</td>
      <td>51.566331</td>
      <td>5.152745</td>
      <td>07:52:00</td>
      <td>day 0</td>
      <td>1631</td>
      <td>4</td>
      <td>2.90</td>
      <td>3</td>
      <td>36</td>
      <td>NL_5056_Berkel-Enschot</td>
      <td>14</td>
      <td>6</td>
      <td>Pickup</td>
    </tr>
    <tr>
      <td>0</td>
      <td>5</td>
      <td>51.566331</td>
      <td>5.152745</td>
      <td>08:06:00</td>
      <td>day 0</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td>08:12:00</td>
      <td>day 0</td>
      <td>2717</td>
      <td>7</td>
      <td>5.00</td>
      <td>6</td>
      <td>36</td>
      <td>NL_5062_Heukelom</td>
      <td>0</td>
      <td>9</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>weight</th>
      <th>volume</th>
      <th>depot</th>
      <th>vehicleType</th>
      <th>serviceTime</th>
      <th>startTimeWindow</th>
      <th>endTimeWindow</th>
      <th>pallets</th>
      <th>pickupDelivery</th>
      <th>externalCosts</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>routeId</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>weight</th>
      <th>volume</th>
      <th>pallets</th>
      <th>pickupDelivery</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>depot_Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>Depot_Tilburg</td>
      <td>51.569517</td>
      <td>5.115192</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>NL_5037_Tilburg</td>
      <td>51.573709</td>
      <td>5.043931</td>
      <td>828</td>
      <td>2.31</td>
      <td>3</td>
      <td>Pickup</td>
    </tr>
    <tr>
      <td>0</td>
      <td>NL_5049_Tilburg</td>
      <td>51.592410</td>
      <td>5.073913</td>
      <td>803</td>
      <td>2.24</td>
      <td>3</td>
      <td>Pickup</td>
    </tr>
    <tr>
      <td>0</td>
      <td>NL_5056_Berkel-Enschot</td>
      <td>51.585860</td>
      <td>5.141180</td>
      <td>903</td>
      <td>2.52</td>
      <td>3</td>
      <td>Delivery</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\milkrun_optimization_plus.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>vehicleType</th>
      <th>deliveryWeight</th>
      <th>deliveryVolume</th>
      <th>deliveryPallets</th>
      <th>pickupWeight</th>
      <th>pickupVolume</th>
      <th>pickupPallets</th>
      <th>drivingTime</th>
      <th>waitingTime</th>
      <th>startTime</th>
      <th>numberOfStops</th>
      <th>maxHeight</th>
      <th>minHeight</th>
      <th>metersUp</th>
      <th>metersDown</th>
      <th>utilizationWeight</th>
      <th>utilizationVolume</th>
      <th>utilizationPallets</th>
      <th>overallUtilization</th>
      <th>stopDuration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Standard</td>
      <td>11391</td>
      <td>37</td>
      <td>45</td>
      <td>11391</td>
      <td>37</td>
      <td>45</td>
      <td>142.82</td>
      <td>59.17</td>
      <td>2021-12-16T20:39:30.000Z</td>
      <td>7</td>
      <td>627.0</td>
      <td>402.3</td>
      <td>1503.6</td>
      <td>1501.8</td>
      <td>22.25</td>
      <td>100.00</td>
      <td>35.00</td>
      <td>100.00</td>
      <td>217.5</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>9519</td>
      <td>31</td>
      <td>38</td>
      <td>9519</td>
      <td>31</td>
      <td>38</td>
      <td>60.43</td>
      <td>51.97</td>
      <td>2021-12-16T20:41:00.000Z</td>
      <td>7</td>
      <td>541.0</td>
      <td>412.5</td>
      <td>670.6</td>
      <td>668.8</td>
      <td>20.37</td>
      <td>94.12</td>
      <td>33.33</td>
      <td>94.12</td>
      <td>205.0</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>6394</td>
      <td>20</td>
      <td>26</td>
      <td>6394</td>
      <td>20</td>
      <td>26</td>
      <td>131.72</td>
      <td>37.83</td>
      <td>2021-12-17T21:22:48.000Z</td>
      <td>6</td>
      <td>535.1</td>
      <td>395.6</td>
      <td>1299.3</td>
      <td>1297.1</td>
      <td>17.83</td>
      <td>76.47</td>
      <td>28.33</td>
      <td>76.47</td>
      <td>193.0</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>5082</td>
      <td>16</td>
      <td>20</td>
      <td>5082</td>
      <td>16</td>
      <td>20</td>
      <td>69.05</td>
      <td>36.73</td>
      <td>2021-12-17T22:26:12.000Z</td>
      <td>3</td>
      <td>535.1</td>
      <td>395.6</td>
      <td>724.3</td>
      <td>722.1</td>
      <td>21.18</td>
      <td>94.12</td>
      <td>33.33</td>
      <td>94.12</td>
      <td>108.0</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>4998</td>
      <td>17</td>
      <td>21</td>
      <td>4998</td>
      <td>17</td>
      <td>21</td>
      <td>67.43</td>
      <td>36.77</td>
      <td>2021-12-17T22:39:17.000Z</td>
      <td>3</td>
      <td>535.1</td>
      <td>395.6</td>
      <td>663.8</td>
      <td>661.6</td>
      <td>20.82</td>
      <td>100.00</td>
      <td>35.00</td>
      <td>100.00</td>
      <td>96.5</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>stopName</th>
      <th>drivingTime</th>
      <th>waitingTime</th>
      <th>stopLatitude</th>
      <th>stopLongitude</th>
      <th>distance</th>
      <th>arrivalTimeAtLocation</th>
      <th>departureTimeFromLocation</th>
      <th>routeId</th>
      <th>sequence</th>
      <th>deliveryWeight</th>
      <th>deliveryVolume</th>
      <th>deliveryPallets</th>
      <th>pickupWeight</th>
      <th>pickupVolume</th>
      <th>pickupPallets</th>
      <th>vehicleUtilization</th>
      <th>stopDuration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Depot_Zurich</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>47.371887</td>
      <td>8.423887</td>
      <td>0.00</td>
      <td>2021-12-16T20:39:30.000Z</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>5340</td>
      <td>17</td>
      <td>21</td>
      <td>100.00</td>
      <td>20.5</td>
    </tr>
    <tr>
      <td>break</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.00</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>2021-12-16T21:30:00.000Z</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>30.0</td>
    </tr>
    <tr>
      <td>Store_15_TW01</td>
      <td>15.98</td>
      <td>14.02</td>
      <td>47.368979</td>
      <td>8.540731</td>
      <td>16.16</td>
      <td>2021-12-16T21:45:59.000Z</td>
      <td>2021-12-16T22:17:00.000Z</td>
      <td>1</td>
      <td>3</td>
      <td>2304</td>
      <td>7</td>
      <td>9</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>41.18</td>
      <td>17.0</td>
    </tr>
    <tr>
      <td>break</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.00</td>
      <td>2021-12-16T22:17:00.000Z</td>
      <td>2021-12-16T22:47:00.000Z</td>
      <td>1</td>
      <td>4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>30.0</td>
    </tr>
    <tr>
      <td>Store_10_TW01</td>
      <td>26.92</td>
      <td>0.00</td>
      <td>47.242118</td>
      <td>8.722541</td>
      <td>22.42</td>
      <td>2021-12-16T23:13:55.000Z</td>
      <td>2021-12-16T23:31:55.000Z</td>
      <td>1</td>
      <td>5</td>
      <td>3036</td>
      <td>10</td>
      <td>12</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>58.82</td>
      <td>18.0</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>vehicleType</th>
      <th>deliveryWeight</th>
      <th>deliveryVolume</th>
      <th>deliveryPallets</th>
      <th>pickupWeight</th>
      <th>pickupVolume</th>
      <th>pickupPallets</th>
      <th>drivingTime</th>
      <th>waitingTime</th>
      <th>startTime</th>
      <th>numberOfStops</th>
      <th>maxHeight</th>
      <th>minHeight</th>
      <th>metersUp</th>
      <th>metersDown</th>
      <th>utilizationWeight</th>
      <th>utilizationVolume</th>
      <th>utilizationPallets</th>
      <th>overallUtilization</th>
      <th>stopDuration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Standard</td>
      <td>9791</td>
      <td>32</td>
      <td>39</td>
      <td>9791</td>
      <td>32</td>
      <td>39</td>
      <td>64.15</td>
      <td>61.10</td>
      <td>2021-12-16T20:39:30.000Z</td>
      <td>7</td>
      <td>541.0</td>
      <td>406.4</td>
      <td>659.1</td>
      <td>661.3</td>
      <td>22.47</td>
      <td>100.00</td>
      <td>35.00</td>
      <td>100.00</td>
      <td>207.5</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>11119</td>
      <td>36</td>
      <td>44</td>
      <td>11119</td>
      <td>36</td>
      <td>44</td>
      <td>86.17</td>
      <td>57.75</td>
      <td>2021-12-16T20:40:30.000Z</td>
      <td>7</td>
      <td>592.9</td>
      <td>406.3</td>
      <td>1016.1</td>
      <td>1018.3</td>
      <td>19.91</td>
      <td>94.12</td>
      <td>31.67</td>
      <td>94.12</td>
      <td>215.0</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>4691</td>
      <td>15</td>
      <td>19</td>
      <td>4691</td>
      <td>15</td>
      <td>19</td>
      <td>76.08</td>
      <td>28.32</td>
      <td>2021-12-17T22:19:05.000Z</td>
      <td>4</td>
      <td>535.1</td>
      <td>395.6</td>
      <td>677.0</td>
      <td>679.2</td>
      <td>19.55</td>
      <td>88.24</td>
      <td>31.67</td>
      <td>88.24</td>
      <td>116.5</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>5186</td>
      <td>17</td>
      <td>21</td>
      <td>5186</td>
      <td>17</td>
      <td>21</td>
      <td>75.80</td>
      <td>34.38</td>
      <td>2021-12-17T22:40:18.000Z</td>
      <td>3</td>
      <td>535.1</td>
      <td>395.6</td>
      <td>709.1</td>
      <td>711.3</td>
      <td>21.61</td>
      <td>100.00</td>
      <td>35.00</td>
      <td>100.00</td>
      <td>89.5</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>5160</td>
      <td>17</td>
      <td>21</td>
      <td>5160</td>
      <td>17</td>
      <td>21</td>
      <td>69.55</td>
      <td>26.25</td>
      <td>2021-12-17T22:23:41.000Z</td>
      <td>3</td>
      <td>535.1</td>
      <td>395.6</td>
      <td>695.9</td>
      <td>698.1</td>
      <td>21.50</td>
      <td>100.00</td>
      <td>35.00</td>
      <td>100.00</td>
      <td>120.5</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>stopName</th>
      <th>drivingTime</th>
      <th>waitingTime</th>
      <th>stopLatitude</th>
      <th>stopLongitude</th>
      <th>distance</th>
      <th>arrivalTimeAtLocation</th>
      <th>departureTimeFromLocation</th>
      <th>routeId</th>
      <th>sequence</th>
      <th>deliveryWeight</th>
      <th>deliveryVolume</th>
      <th>deliveryPallets</th>
      <th>pickupWeight</th>
      <th>pickupVolume</th>
      <th>pickupPallets</th>
      <th>vehicleUtilization</th>
      <th>stopDuration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Depot_Zurich</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>47.371149</td>
      <td>8.424263</td>
      <td>0.00</td>
      <td>2021-12-16T20:39:30.000Z</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>5393</td>
      <td>17</td>
      <td>21</td>
      <td>100.00</td>
      <td>20.5</td>
    </tr>
    <tr>
      <td>break</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.00</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>2021-12-16T21:30:00.000Z</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>30.0</td>
    </tr>
    <tr>
      <td>Store_9_TW01</td>
      <td>14.77</td>
      <td>15.23</td>
      <td>47.375383</td>
      <td>8.536080</td>
      <td>15.58</td>
      <td>2021-12-16T21:44:46.000Z</td>
      <td>2021-12-16T22:19:00.000Z</td>
      <td>1</td>
      <td>3</td>
      <td>1764</td>
      <td>6</td>
      <td>7</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>35.29</td>
      <td>19.0</td>
    </tr>
    <tr>
      <td>Store_15_TW01</td>
      <td>3.42</td>
      <td>0.00</td>
      <td>47.368812</td>
      <td>8.540987</td>
      <td>1.53</td>
      <td>2021-12-16T22:22:25.000Z</td>
      <td>2021-12-16T22:39:25.000Z</td>
      <td>1</td>
      <td>4</td>
      <td>2304</td>
      <td>7</td>
      <td>9</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>41.18</td>
      <td>17.0</td>
    </tr>
    <tr>
      <td>break</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.00</td>
      <td>2021-12-16T22:39:25.000Z</td>
      <td>2021-12-16T23:09:25.000Z</td>
      <td>1</td>
      <td>5</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>30.0</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\transport_optimization.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>id</th>
      <th>startDepotName</th>
      <th>startDepotCountry</th>
      <th>startDepotState</th>
      <th>startDepotPostalCode</th>
      <th>startDepotCity</th>
      <th>startDepotStreet</th>
      <th>startDepotLatitude</th>
      <th>startDepotLongitude</th>
      <th>endDepotName</th>
      <th>drivingDuration</th>
      <th>duration</th>
      <th>weight</th>
      <th>utilizationWeight</th>
      <th>volume</th>
      <th>utilizationVolume</th>
      <th>startTime</th>
      <th>endTime</th>
      <th>pallets</th>
      <th>utilizationPallets</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>San Francisco</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>San Diego</td>
      <td>1603</td>
      <td>1716</td>
      <td>23756</td>
      <td>98.98</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T10:36:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>1</td>
      <td>San Francisco</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>San Diego</td>
      <td>1400</td>
      <td>1457</td>
      <td>19022</td>
      <td>79.26</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T06:17:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>2</td>
      <td>San Francisco</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>San Diego</td>
      <td>1400</td>
      <td>1468</td>
      <td>14104</td>
      <td>58.77</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T06:28:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>San Francisco</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>San Diego</td>
      <td>1572</td>
      <td>1695</td>
      <td>23411</td>
      <td>97.55</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T10:15:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>4</td>
      <td>San Francisco</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>San Diego</td>
      <td>1577</td>
      <td>1678</td>
      <td>23232</td>
      <td>96.80</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T09:58:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>id</th>
      <th>routeLeg</th>
      <th>startLocationCountry</th>
      <th>startLocationState</th>
      <th>startLocationPostalCode</th>
      <th>startLocationCity</th>
      <th>startLocationStreet</th>
      <th>startLocationLatitude</th>
      <th>startLocationLongitude</th>
      <th>startTime</th>
      <th>weight</th>
      <th>volume</th>
      <th>distance</th>
      <th>drivingDuration</th>
      <th>duration</th>
      <th>departureLocationName</th>
      <th>endTime</th>
      <th>arrivalLoadingTime</th>
      <th>pallets</th>
      <th>departureLoadingTime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>1</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
      <td>37.779259</td>
      <td>-122.419329</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>0</td>
      <td>0</td>
      <td>87.40</td>
      <td>87</td>
      <td>103</td>
      <td>San Francisco</td>
      <td>2017-11-20T07:27:00.000Z</td>
      <td>16</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>1</td>
      <td>2</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>Santa Rosa</td>
      <td></td>
      <td>38.440492</td>
      <td>-122.714105</td>
      <td>2017-11-20T07:43:00.000Z</td>
      <td>8488</td>
      <td>0</td>
      <td>91.78</td>
      <td>92</td>
      <td>130</td>
      <td>Santa Rosa</td>
      <td>2017-11-20T09:15:00.000Z</td>
      <td>22</td>
      <td>0</td>
      <td>16</td>
    </tr>
    <tr>
      <td>2</td>
      <td>3</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>Fairfield</td>
      <td></td>
      <td>38.249358</td>
      <td>-122.039966</td>
      <td>2017-11-20T09:37:00.000Z</td>
      <td>17043</td>
      <td>0</td>
      <td>15.02</td>
      <td>15</td>
      <td>52</td>
      <td>Fairfield</td>
      <td>2017-11-20T09:52:00.000Z</td>
      <td>15</td>
      <td>0</td>
      <td>22</td>
    </tr>
    <tr>
      <td>3</td>
      <td>4</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>Vacaville</td>
      <td></td>
      <td>38.356577</td>
      <td>-121.987744</td>
      <td>2017-11-20T10:07:00.000Z</td>
      <td>23756</td>
      <td>0</td>
      <td>708.44</td>
      <td>708</td>
      <td>745</td>
      <td>Vacaville</td>
      <td>2017-11-20T21:55:00.000Z</td>
      <td>22</td>
      <td>0</td>
      <td>15</td>
    </tr>
    <tr>
      <td>4</td>
      <td>5</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>Irvine</td>
      <td></td>
      <td>33.685697</td>
      <td>-117.825981</td>
      <td>2017-11-20T22:17:00.000Z</td>
      <td>15201</td>
      <td>0</td>
      <td>9.55</td>
      <td>10</td>
      <td>55</td>
      <td>Irvine</td>
      <td>2017-11-20T22:27:00.000Z</td>
      <td>23</td>
      <td>0</td>
      <td>22</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>name</th>
      <th>earliestPickupTime</th>
      <th>latestPickupTime</th>
      <th>earliestDeliveryTime</th>
      <th>latestDeliveryTime</th>
      <th>weight</th>
      <th>volume</th>
      <th>vehicleType</th>
      <th>senderId</th>
      <th>recipientId</th>
      <th>pallets</th>
      <th>externalCosts</th>
      <th>senderStopDuration</th>
      <th>recipientStopDuration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>1899-12-30T00:00:00.000Z</td>
      <td>1899-12-30T00:00:00.000Z</td>
      <td>1899-12-30T00:00:00.000Z</td>
      <td>1899-12-30T00:00:00.000Z</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>routeId</th>
      <th>name</th>
      <th>country</th>
      <th>state</th>
      <th>postalCode</th>
      <th>city</th>
      <th>street</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>San Francisco</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>San Francisco</td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>Santa Rosa</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>Santa Rosa</td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>Fairfield</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>Fairfield</td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>Vacaville</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>Vacaville</td>
      <td></td>
    </tr>
    <tr>
      <td>0</td>
      <td>Irvine</td>
      <td>US</td>
      <td>CA</td>
      <td></td>
      <td>Irvine</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>routeId</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>San Francisco</td>
      <td>37.779259</td>
      <td>-122.419329</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Santa Rosa</td>
      <td>38.440492</td>
      <td>-122.714105</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Fairfield</td>
      <td>38.249358</td>
      <td>-122.039966</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Vacaville</td>
      <td>38.356577</td>
      <td>-121.987744</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Irvine</td>
      <td>33.685697</td>
      <td>-117.825981</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>id</th>
      <th>startDepotName</th>
      <th>startDepotLatitude</th>
      <th>startDepotLongitude</th>
      <th>endDepotName</th>
      <th>endDepotLatitude</th>
      <th>endDepotLongitude</th>
      <th>vehicleType</th>
      <th>numberOfStops</th>
      <th>totalCosts</th>
      <th>duration</th>
      <th>drivingDuration</th>
      <th>weight</th>
      <th>utilizationWeight</th>
      <th>volume</th>
      <th>utilizationVolume</th>
      <th>startTime</th>
      <th>endTime</th>
      <th>pallets</th>
      <th>utilizationPallets</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>San Francisco</td>
      <td>37.77493</td>
      <td>-122.41942</td>
      <td>San Diego</td>
      <td>32.715738</td>
      <td>-117.16108</td>
      <td>Dry_Van_Trailer</td>
      <td>6</td>
      <td>958.09</td>
      <td>1661</td>
      <td>1565</td>
      <td>21329</td>
      <td>88.87</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T09:41:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>1</td>
      <td>San Francisco</td>
      <td>37.77493</td>
      <td>-122.41942</td>
      <td>San Diego</td>
      <td>32.715738</td>
      <td>-117.16108</td>
      <td>Dry_Van_Trailer</td>
      <td>6</td>
      <td>1138.79</td>
      <td>1695</td>
      <td>1603</td>
      <td>23775</td>
      <td>99.06</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T10:15:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>2</td>
      <td>San Francisco</td>
      <td>37.77493</td>
      <td>-122.41942</td>
      <td>San Diego</td>
      <td>32.715738</td>
      <td>-117.16108</td>
      <td>Dry_Van_Trailer</td>
      <td>6</td>
      <td>987.15</td>
      <td>1736</td>
      <td>1639</td>
      <td>20297</td>
      <td>84.57</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T10:56:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>San Francisco</td>
      <td>37.77493</td>
      <td>-122.41942</td>
      <td>San Diego</td>
      <td>32.715738</td>
      <td>-117.16108</td>
      <td>Dry_Van_Trailer</td>
      <td>6</td>
      <td>1039.14</td>
      <td>1695</td>
      <td>1577</td>
      <td>22712</td>
      <td>94.63</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T10:15:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>4</td>
      <td>San Francisco</td>
      <td>37.77493</td>
      <td>-122.41942</td>
      <td>San Diego</td>
      <td>32.715738</td>
      <td>-117.16108</td>
      <td>Dry_Van_Trailer</td>
      <td>4</td>
      <td>878.92</td>
      <td>1570</td>
      <td>1516</td>
      <td>18674</td>
      <td>77.81</td>
      <td>0</td>
      <td>0</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T08:10:00.000Z</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>id</th>
      <th>routeLeg</th>
      <th>startLocationLatitude</th>
      <th>startLocationLongitude</th>
      <th>startTime</th>
      <th>arrivalLocationName</th>
      <th>arrivalLocationLatitude</th>
      <th>arrivalLocationLongitude</th>
      <th>weight</th>
      <th>volume</th>
      <th>distance</th>
      <th>drivingDuration</th>
      <th>duration</th>
      <th>departureLocationName</th>
      <th>departureLoadingTime</th>
      <th>arrivalLoadingTime</th>
      <th>pallets</th>
      <th>endTime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>1</td>
      <td>37.774930</td>
      <td>-122.41942</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>Redwood City</td>
      <td>37.485215</td>
      <td>-122.23635</td>
      <td>0</td>
      <td>0</td>
      <td>41.58</td>
      <td>42</td>
      <td>62</td>
      <td>San Francisco</td>
      <td>0</td>
      <td>20</td>
      <td>0</td>
      <td>2017-11-20T06:42:00.000Z</td>
    </tr>
    <tr>
      <td>1</td>
      <td>2</td>
      <td>37.485215</td>
      <td>-122.23635</td>
      <td>2017-11-20T07:02:00.000Z</td>
      <td>Sunnyvale</td>
      <td>37.368830</td>
      <td>-122.03635</td>
      <td>6381</td>
      <td>0</td>
      <td>25.07</td>
      <td>25</td>
      <td>55</td>
      <td>Redwood City</td>
      <td>20</td>
      <td>10</td>
      <td>0</td>
      <td>2017-11-20T07:27:00.000Z</td>
    </tr>
    <tr>
      <td>2</td>
      <td>3</td>
      <td>37.368830</td>
      <td>-122.03635</td>
      <td>2017-11-20T07:37:00.000Z</td>
      <td>San Jose</td>
      <td>37.338208</td>
      <td>-121.88633</td>
      <td>12960</td>
      <td>0</td>
      <td>19.66</td>
      <td>20</td>
      <td>43</td>
      <td>Sunnyvale</td>
      <td>10</td>
      <td>13</td>
      <td>0</td>
      <td>2017-11-20T07:57:00.000Z</td>
    </tr>
    <tr>
      <td>3</td>
      <td>4</td>
      <td>37.338208</td>
      <td>-121.88633</td>
      <td>2017-11-20T08:10:00.000Z</td>
      <td>Corona</td>
      <td>33.875294</td>
      <td>-117.56644</td>
      <td>21329</td>
      <td>0</td>
      <td>618.53</td>
      <td>619</td>
      <td>645</td>
      <td>San Jose</td>
      <td>13</td>
      <td>13</td>
      <td>0</td>
      <td>2017-11-20T18:29:00.000Z</td>
    </tr>
    <tr>
      <td>4</td>
      <td>5</td>
      <td>33.875294</td>
      <td>-117.56644</td>
      <td>2017-11-20T18:42:00.000Z</td>
      <td>Mission Viejo</td>
      <td>33.596891</td>
      <td>-117.65816</td>
      <td>12960</td>
      <td>0</td>
      <td>53.68</td>
      <td>54</td>
      <td>88</td>
      <td>Corona</td>
      <td>13</td>
      <td>21</td>
      <td>0</td>
      <td>2017-11-20T19:36:00.000Z</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>name</th>
      <th>earliestPickupTime</th>
      <th>latestPickupTime</th>
      <th>earliestDeliveryTime</th>
      <th>latestDeliveryTime</th>
      <th>weight</th>
      <th>volume</th>
      <th>vehicleType</th>
      <th>sender</th>
      <th>recipient</th>
      <th>senderStopDuration</th>
      <th>recipientStopDuration</th>
      <th>pallets</th>
      <th>externalCosts</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Berkeley --> San Marcos</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-20T18:00:00.000Z</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T18:00:00.000Z</td>
      <td>9752</td>
      <td>0</td>
      <td>Dry_Van_Trailer</td>
      <td>Berkeley</td>
      <td>San Marcos</td>
      <td>13</td>
      <td>11</td>
      <td>0</td>
      <td>14628</td>
    </tr>
    <tr>
      <td>Richmond --> Chula Vista</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-20T18:00:00.000Z</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T18:00:00.000Z</td>
      <td>8976</td>
      <td>0</td>
      <td>Dry_Van_Trailer</td>
      <td>Richmond</td>
      <td>Chula Vista</td>
      <td>25</td>
      <td>13</td>
      <td>0</td>
      <td>13464</td>
    </tr>
    <tr>
      <td>Concord --> Murrieta</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-20T18:00:00.000Z</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T18:00:00.000Z</td>
      <td>10000</td>
      <td>0</td>
      <td>Dry_Van_Trailer</td>
      <td>Concord</td>
      <td>Murrieta</td>
      <td>21</td>
      <td>25</td>
      <td>0</td>
      <td>15000</td>
    </tr>
    <tr>
      <td>Fairfield --> Irvine</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-20T18:00:00.000Z</td>
      <td>2017-11-20T06:00:00.000Z</td>
      <td>2017-11-21T18:00:00.000Z</td>
      <td>8555</td>
      <td>0</td>
      <td>Dry_Van_Trailer</td>
      <td>Fairfield</td>
      <td>Irvine</td>
      <td>22</td>
      <td>22</td>
      <td>0</td>
      <td>12833</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>routeId</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>San Francisco</td>
      <td>37.774930</td>
      <td>-122.41942</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Redwood City</td>
      <td>37.485215</td>
      <td>-122.23635</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Sunnyvale</td>
      <td>37.368830</td>
      <td>-122.03635</td>
    </tr>
    <tr>
      <td>0</td>
      <td>San Jose</td>
      <td>37.338208</td>
      <td>-121.88633</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Corona</td>
      <td>33.875294</td>
      <td>-117.56644</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\transport_optimization_plus.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>vehicleType</th>
      <th>deliveryWeight</th>
      <th>deliveryVolume</th>
      <th>deliveryPallets</th>
      <th>pickupWeight</th>
      <th>pickupVolume</th>
      <th>pickupPallets</th>
      <th>drivingTime</th>
      <th>waitingTime</th>
      <th>startTime</th>
      <th>maxHeight</th>
      <th>minHeight</th>
      <th>metersUp</th>
      <th>metersDown</th>
      <th>utilizationWeight</th>
      <th>utilizationVolume</th>
      <th>utilizationPallets</th>
      <th>overallUtilization</th>
      <th>stopDuration</th>
      <th>costs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Standard</td>
      <td>796</td>
      <td>2</td>
      <td>17</td>
      <td>796</td>
      <td>2</td>
      <td>17</td>
      <td>313.57</td>
      <td>0.00</td>
      <td>2021-12-16T20:50:31.000Z</td>
      <td>673.2</td>
      <td>264.1</td>
      <td>3438.8</td>
      <td>3436.6</td>
      <td>1.92</td>
      <td>5.88</td>
      <td>16.67</td>
      <td>16.67</td>
      <td>110</td>
      <td>724</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>492</td>
      <td>1</td>
      <td>12</td>
      <td>492</td>
      <td>1</td>
      <td>12</td>
      <td>579.75</td>
      <td>0.60</td>
      <td>2021-12-16T20:23:00.000Z</td>
      <td>642.6</td>
      <td>365.6</td>
      <td>6021.1</td>
      <td>6019.3</td>
      <td>2.05</td>
      <td>5.88</td>
      <td>20.00</td>
      <td>20.00</td>
      <td>85</td>
      <td>1210</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>1263</td>
      <td>3</td>
      <td>31</td>
      <td>1263</td>
      <td>3</td>
      <td>31</td>
      <td>460.90</td>
      <td>18.27</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>638.9</td>
      <td>359.0</td>
      <td>4260.6</td>
      <td>4258.4</td>
      <td>2.25</td>
      <td>5.88</td>
      <td>20.00</td>
      <td>20.00</td>
      <td>135</td>
      <td>971</td>
    </tr>
    <tr>
      <td>Truck_12t</td>
      <td>1164</td>
      <td>3</td>
      <td>29</td>
      <td>1164</td>
      <td>3</td>
      <td>29</td>
      <td>565.17</td>
      <td>0.00</td>
      <td>2021-12-16T20:09:44.000Z</td>
      <td>892.7</td>
      <td>365.6</td>
      <td>5775.0</td>
      <td>5772.8</td>
      <td>4.70</td>
      <td>5.88</td>
      <td>40.00</td>
      <td>40.00</td>
      <td>135</td>
      <td>1146</td>
    </tr>
    <tr>
      <td>Truck_12t</td>
      <td>569</td>
      <td>2</td>
      <td>16</td>
      <td>569</td>
      <td>2</td>
      <td>16</td>
      <td>571.87</td>
      <td>0.00</td>
      <td>2021-12-16T20:20:01.000Z</td>
      <td>6313.3</td>
      <td>195.4</td>
      <td>17359.8</td>
      <td>17358.0</td>
      <td>2.70</td>
      <td>5.88</td>
      <td>30.00</td>
      <td>30.00</td>
      <td>110</td>
      <td>1168</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>drivingTime</th>
      <th>waitingTime</th>
      <th>arrivalTimeAtLocation</th>
      <th>stopLatitude</th>
      <th>stopLongitude</th>
      <th>departureTimeFromLocation</th>
      <th>distance</th>
      <th>stopName</th>
      <th>routeId</th>
      <th>sequence</th>
      <th>deliveryWeight</th>
      <th>deliveryVolume</th>
      <th>deliveryPallets</th>
      <th>pickupWeight</th>
      <th>pickupVolume</th>
      <th>pickupPallets</th>
      <th>vehicleUtilization</th>
      <th>stopDuration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0.00</td>
      <td>0.0</td>
      <td>2021-12-16T20:50:31.000Z</td>
      <td>47.371887</td>
      <td>8.423887</td>
      <td>2021-12-16T20:50:31.000Z</td>
      <td>0.00</td>
      <td>Depot_Zurich</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>0</td>
    </tr>
    <tr>
      <td>0.00</td>
      <td>0.0</td>
      <td>2021-12-16T20:50:31.000Z</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>2021-12-16T21:20:31.000Z</td>
      <td>0.00</td>
      <td>break</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>30</td>
    </tr>
    <tr>
      <td>39.48</td>
      <td>0.0</td>
      <td>2021-12-16T22:00:00.000Z</td>
      <td>47.392715</td>
      <td>8.044445</td>
      <td>2021-12-16T22:10:00.000Z</td>
      <td>41.20</td>
      <td>Aarau</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>336</td>
      <td>1</td>
      <td>7</td>
      <td>11.67</td>
      <td>10</td>
    </tr>
    <tr>
      <td>22.55</td>
      <td>0.0</td>
      <td>2021-12-16T22:32:33.000Z</td>
      <td>47.320642</td>
      <td>7.899360</td>
      <td>2021-12-16T22:42:33.000Z</td>
      <td>21.34</td>
      <td>Aarburg</td>
      <td>1</td>
      <td>4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>460</td>
      <td>1</td>
      <td>10</td>
      <td>16.67</td>
      <td>10</td>
    </tr>
    <tr>
      <td>0.00</td>
      <td>0.0</td>
      <td>2021-12-16T22:42:33.000Z</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>2021-12-16T23:12:33.000Z</td>
      <td>0.00</td>
      <td>break</td>
      <td>1</td>
      <td>5</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>30</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>vehicleType</th>
      <th>deliveryWeight</th>
      <th>deliveryVolume</th>
      <th>deliveryPallets</th>
      <th>pickupWeight</th>
      <th>pickupVolume</th>
      <th>pickupPallets</th>
      <th>drivingTime</th>
      <th>waitingTime</th>
      <th>startTime</th>
      <th>maxHeight</th>
      <th>minHeight</th>
      <th>metersUp</th>
      <th>metersDown</th>
      <th>utilizationWeight</th>
      <th>utilizationVolume</th>
      <th>utilizationPallets</th>
      <th>overallUtilization</th>
      <th>stopDuration</th>
      <th>costs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Standard</td>
      <td>1120</td>
      <td>3</td>
      <td>26</td>
      <td>1120</td>
      <td>3</td>
      <td>26</td>
      <td>412.82</td>
      <td>50.85</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>906.0</td>
      <td>264.1</td>
      <td>4766.9</td>
      <td>4769.1</td>
      <td>1.92</td>
      <td>5.88</td>
      <td>16.67</td>
      <td>16.67</td>
      <td>135</td>
      <td>856</td>
    </tr>
    <tr>
      <td>Standard</td>
      <td>1201</td>
      <td>3</td>
      <td>27</td>
      <td>1201</td>
      <td>3</td>
      <td>27</td>
      <td>464.25</td>
      <td>17.92</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>865.8</td>
      <td>359.0</td>
      <td>4834.7</td>
      <td>4836.9</td>
      <td>2.25</td>
      <td>5.88</td>
      <td>20.00</td>
      <td>20.00</td>
      <td>135</td>
      <td>978</td>
    </tr>
    <tr>
      <td>Truck_12t</td>
      <td>1164</td>
      <td>3</td>
      <td>29</td>
      <td>1164</td>
      <td>3</td>
      <td>29</td>
      <td>565.87</td>
      <td>0.00</td>
      <td>2021-12-16T20:09:23.000Z</td>
      <td>892.7</td>
      <td>365.6</td>
      <td>5773.4</td>
      <td>5775.6</td>
      <td>4.70</td>
      <td>5.88</td>
      <td>40.00</td>
      <td>40.00</td>
      <td>135</td>
      <td>1146</td>
    </tr>
    <tr>
      <td>Truck_12t</td>
      <td>335</td>
      <td>2</td>
      <td>10</td>
      <td>335</td>
      <td>2</td>
      <td>10</td>
      <td>519.70</td>
      <td>0.00</td>
      <td>2021-12-16T20:25:21.000Z</td>
      <td>6313.3</td>
      <td>195.4</td>
      <td>16526.2</td>
      <td>16528.4</td>
      <td>2.04</td>
      <td>5.88</td>
      <td>23.33</td>
      <td>23.33</td>
      <td>110</td>
      <td>1085</td>
    </tr>
    <tr>
      <td>Truck_12t</td>
      <td>973</td>
      <td>3</td>
      <td>24</td>
      <td>973</td>
      <td>3</td>
      <td>24</td>
      <td>575.58</td>
      <td>0.00</td>
      <td>2021-12-16T19:59:59.000Z</td>
      <td>865.8</td>
      <td>365.6</td>
      <td>5786.5</td>
      <td>5788.7</td>
      <td>3.75</td>
      <td>5.88</td>
      <td>36.67</td>
      <td>36.67</td>
      <td>135</td>
      <td>1171</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>drivingTime</th>
      <th>waitingTime</th>
      <th>arrivalTimeAtLocation</th>
      <th>stopLatitude</th>
      <th>stopLongitude</th>
      <th>departureTimeFromLocation</th>
      <th>distance</th>
      <th>stopName</th>
      <th>routeId</th>
      <th>sequence</th>
      <th>deliveryWeight</th>
      <th>deliveryVolume</th>
      <th>deliveryPallets</th>
      <th>pickupWeight</th>
      <th>pickupVolume</th>
      <th>pickupPallets</th>
      <th>vehicleUtilization</th>
      <th>stopDuration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0.00</td>
      <td>0.0</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>47.371134</td>
      <td>8.424274</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>0.00</td>
      <td>Depot_Zurich</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>0</td>
    </tr>
    <tr>
      <td>0.00</td>
      <td>0.0</td>
      <td>2021-12-16T21:00:00.000Z</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>2021-12-16T21:30:00.000Z</td>
      <td>0.00</td>
      <td>break</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>30</td>
    </tr>
    <tr>
      <td>39.85</td>
      <td>0.0</td>
      <td>2021-12-16T22:09:51.000Z</td>
      <td>47.392715</td>
      <td>8.044445</td>
      <td>2021-12-16T22:19:51.000Z</td>
      <td>41.29</td>
      <td>Aarau</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>336</td>
      <td>1</td>
      <td>7</td>
      <td>11.67</td>
      <td>10</td>
    </tr>
    <tr>
      <td>0.00</td>
      <td>0.0</td>
      <td>2021-12-16T22:19:51.000Z</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>2021-12-16T22:49:51.000Z</td>
      <td>0.00</td>
      <td>break</td>
      <td>1</td>
      <td>4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.00</td>
      <td>30</td>
    </tr>
    <tr>
      <td>54.95</td>
      <td>0.0</td>
      <td>2021-12-16T23:44:48.000Z</td>
      <td>47.536560</td>
      <td>7.570077</td>
      <td>2021-12-16T23:59:48.000Z</td>
      <td>55.36</td>
      <td>Binningen</td>
      <td>1</td>
      <td>5</td>
      <td>336</td>
      <td>1</td>
      <td>7</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>11.67</td>
      <td>15</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\shipment_analyzer.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>shipmentId</th>
      <th>shipmentLeg</th>
      <th>fromId</th>
      <th>fromCountry</th>
      <th>fromIso2Country</th>
      <th>fromState</th>
      <th>fromCity</th>
      <th>fromPostalCode</th>
      <th>fromStreet</th>
      <th>fromUnLocode</th>
      <th>fromParsedLatitude</th>
      <th>fromParsedLongitude</th>
      <th>toParsedLatitude</th>
      <th>toParsedLongitude</th>
      <th>simulatedCostsPerTkm</th>
      <th>simulatedFreightCosts</th>
      <th>fulfilledOnTime</th>
      <th>co2EmissionTankToWheel</th>
      <th>co2EmissionWheelToTank</th>
      <th>co2Emission</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>s001</td>
      <td>1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>DE</td>
      <td></td>
      <td>Sindelfingen</td>
      <td></td>
      <td></td>
      <td></td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>53.550341</td>
      <td>10.000654</td>
      <td></td>
      <td></td>
      <td>yes</td>
      <td>409.376137</td>
      <td>85.951894</td>
      <td>495.328031</td>
    </tr>
    <tr>
      <td>s002</td>
      <td>1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>DE</td>
      <td></td>
      <td>Sindelfingen</td>
      <td></td>
      <td></td>
      <td></td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>49.019533</td>
      <td>12.097487</td>
      <td>0.74</td>
      <td>1579.09</td>
      <td>yes</td>
      <td>146.897137</td>
      <td>30.842265</td>
      <td>177.739402</td>
    </tr>
    <tr>
      <td>s002</td>
      <td>2</td>
      <td>CU_Regensburg</td>
      <td>DE</td>
      <td>DE</td>
      <td></td>
      <td>Regensburg</td>
      <td></td>
      <td></td>
      <td></td>
      <td>49.019533</td>
      <td>12.097487</td>
      <td>48.974736</td>
      <td>14.474285</td>
      <td>1.53</td>
      <td>1276.76</td>
      <td>yes</td>
      <td>57.087875</td>
      <td>11.986070</td>
      <td>69.073945</td>
    </tr>
    <tr>
      <td>s003</td>
      <td>1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>DE</td>
      <td></td>
      <td>Sindelfingen</td>
      <td></td>
      <td></td>
      <td></td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>46.907388</td>
      <td>19.691721</td>
      <td>0.96</td>
      <td>2899.25</td>
      <td>yes</td>
      <td>205.990355</td>
      <td>43.249373</td>
      <td>249.239728</td>
    </tr>
    <tr>
      <td>s004</td>
      <td>1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>DE</td>
      <td></td>
      <td>Sindelfingen</td>
      <td></td>
      <td></td>
      <td></td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>41.125784</td>
      <td>16.862029</td>
      <td>0.4</td>
      <td>5792.86</td>
      <td>yes</td>
      <td>995.583829</td>
      <td>209.031032</td>
      <td>1204.614861</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>transportId</th>
      <th>shipmentId</th>
      <th>fromId</th>
      <th>fromIso2Country</th>
      <th>toId</th>
      <th>toIso2Country</th>
      <th>distance</th>
      <th>shippingMode</th>
      <th>carrier</th>
      <th>truckShipPlaneType</th>
      <th>Utilization</th>
      <th>co2Emission</th>
      <th>co2EmissionWheelToTank</th>
      <th>co2EmissionTankToWheel</th>
      <th>tkm</th>
      <th>fromParsedLatitude</th>
      <th>fromParsedLongitude</th>
      <th>toParsedLatitude</th>
      <th>toParsedLongitude</th>
      <th>simulatedFreightCosts</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>T1</td>
      <td>s001 leg 1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>WH_Hamburg</td>
      <td>DE</td>
      <td>664.3297</td>
      <td>road</td>
      <td>Carrier 1</td>
      <td>Standard</td>
      <td>76.0</td>
      <td>495.328031</td>
      <td>85.951894</td>
      <td>409.376137</td>
      <td>5978.96730</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>53.550341</td>
      <td>10.000654</td>
      <td></td>
    </tr>
    <tr>
      <td>T2</td>
      <td>s002 leg 1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>CU_Regensburg</td>
      <td>DE</td>
      <td>306.4921</td>
      <td>road</td>
      <td>Carrier 1</td>
      <td>Standard</td>
      <td>64.0</td>
      <td>177.739402</td>
      <td>30.842265</td>
      <td>146.897137</td>
      <td>2145.44470</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>49.019533</td>
      <td>12.097487</td>
      <td>1579.09</td>
    </tr>
    <tr>
      <td>T3</td>
      <td>s002 leg 2</td>
      <td>CU_Regensburg</td>
      <td>DE</td>
      <td>CU_Budejovice</td>
      <td>CZ</td>
      <td>225.3439</td>
      <td>road</td>
      <td>Carrier 1</td>
      <td>Standard</td>
      <td>30.0</td>
      <td>69.073945</td>
      <td>11.986070</td>
      <td>57.087875</td>
      <td>833.77243</td>
      <td>49.019533</td>
      <td>12.097487</td>
      <td>48.974736</td>
      <td>14.474285</td>
      <td>1276.76</td>
    </tr>
    <tr>
      <td>T4</td>
      <td>s003 leg 1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>WH_Kecskemet</td>
      <td>HU</td>
      <td>1002.8354</td>
      <td>road</td>
      <td>Carrier 2</td>
      <td>Standard</td>
      <td>38.0</td>
      <td>249.239728</td>
      <td>43.249373</td>
      <td>205.990355</td>
      <td>3008.50620</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>46.907388</td>
      <td>19.691721</td>
      <td>2899.25</td>
    </tr>
    <tr>
      <td>T5</td>
      <td>s004 leg 1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>CU_Bari</td>
      <td>IT</td>
      <td>1384.8172</td>
      <td>road</td>
      <td>Carrier 2</td>
      <td>Mega</td>
      <td>67.0</td>
      <td>1204.614861</td>
      <td>209.031032</td>
      <td>995.583829</td>
      <td>14540.58060</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>41.125784</td>
      <td>16.862029</td>
      <td>5792.86</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>shipmentId</th>
      <th>shipmentLeg</th>
      <th>fromId</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>fromIso2Country</th>
      <th>toId</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>toIso2Country</th>
      <th>transportId</th>
      <th>tkmShare</th>
      <th>distance</th>
      <th>freightCostsPerTkm</th>
      <th>simulatedCostsPerTkm</th>
      <th>simulatedFreightCosts</th>
      <th>fulfilledOnTime</th>
      <th>co2EmissionTankToWheel</th>
      <th>co2EmissionWheelToTank</th>
      <th>co2Emission</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>s001</td>
      <td>1</td>
      <td>WH_Sindelfingen</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>DE</td>
      <td>WH_Hamburg</td>
      <td>53.550341</td>
      <td>10.000654</td>
      <td>DE</td>
      <td>T1</td>
      <td>5978.97</td>
      <td>664.33</td>
      <td>0.13</td>
      <td>0.42</td>
      <td>2486.4</td>
      <td>yes</td>
      <td>409.376137</td>
      <td>85.951894</td>
      <td>495.328031</td>
    </tr>
    <tr>
      <td>s002</td>
      <td>1</td>
      <td>WH_Sindelfingen</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>DE</td>
      <td>CU_Regensburg</td>
      <td>49.019533</td>
      <td>12.097487</td>
      <td>DE</td>
      <td>T2</td>
      <td>2145.43</td>
      <td>306.49</td>
      <td>0.30</td>
      <td>0.74</td>
      <td>1579.09</td>
      <td>yes</td>
      <td>146.896179</td>
      <td>30.842064</td>
      <td>177.738243</td>
    </tr>
    <tr>
      <td>s002</td>
      <td>2</td>
      <td>CU_Regensburg</td>
      <td>49.019533</td>
      <td>12.097487</td>
      <td>DE</td>
      <td>CU_Budejovice</td>
      <td>48.974736</td>
      <td>14.474285</td>
      <td>CZ</td>
      <td>T3</td>
      <td>833.76</td>
      <td>225.34</td>
      <td>0.72</td>
      <td>1.53</td>
      <td>1276.76</td>
      <td>yes</td>
      <td>57.086860</td>
      <td>11.985857</td>
      <td>69.072717</td>
    </tr>
    <tr>
      <td>s003</td>
      <td>1</td>
      <td>WH_Sindelfingen</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>DE</td>
      <td>WH_Kecskemet</td>
      <td>46.894253</td>
      <td>19.686575</td>
      <td>HU</td>
      <td>T4</td>
      <td>3035.31</td>
      <td>1011.77</td>
      <td>0.49</td>
      <td>0.96</td>
      <td>2899.25</td>
      <td>yes</td>
      <td>207.825676</td>
      <td>43.634714</td>
      <td>251.460390</td>
    </tr>
    <tr>
      <td>s004</td>
      <td>1</td>
      <td>WH_Sindelfingen</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>DE</td>
      <td>CU_Bari</td>
      <td>41.125784</td>
      <td>16.862029</td>
      <td>IT</td>
      <td>T5</td>
      <td>14540.61</td>
      <td>1384.82</td>
      <td>0.14</td>
      <td>0.4</td>
      <td>5792.86</td>
      <td>yes</td>
      <td>995.585986</td>
      <td>209.031484</td>
      <td>1204.617470</td>
    </tr>
  </tbody>
</table>
</div>
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>transportId</th>
      <th>shipmentId</th>
      <th>fromId</th>
      <th>fromIso2Country</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>toId</th>
      <th>toIso2Country</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>capacityPallets</th>
      <th>transportValue</th>
      <th>freightCosts</th>
      <th>benchmarkTariff</th>
      <th>Utilization</th>
      <th>co2Emission</th>
      <th>co2EmissionWheelToTank</th>
      <th>co2EmissionTankToWheel</th>
      <th>tkm</th>
      <th>simulatedFreightCosts</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>T1</td>
      <td>s001 leg 1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>WH_Hamburg</td>
      <td>DE</td>
      <td>53.550341</td>
      <td>10.000654</td>
      <td>66</td>
      <td>50000</td>
      <td>800</td>
      <td>road tariff</td>
      <td>76.0</td>
      <td>495.328031</td>
      <td>85.951894</td>
      <td>409.376137</td>
      <td>5978.970</td>
      <td>2486.4</td>
    </tr>
    <tr>
      <td>T2</td>
      <td>s002 leg 1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>CU_Regensburg</td>
      <td>DE</td>
      <td>49.019533</td>
      <td>12.097487</td>
      <td>66</td>
      <td>42000</td>
      <td>650</td>
      <td>road tariff</td>
      <td>64.0</td>
      <td>177.738243</td>
      <td>30.842064</td>
      <td>146.896179</td>
      <td>2145.430</td>
      <td>1579.09</td>
    </tr>
    <tr>
      <td>T3</td>
      <td>s002 leg 2</td>
      <td>CU_Regensburg</td>
      <td>DE</td>
      <td>49.019533</td>
      <td>12.097487</td>
      <td>CU_Budejovice</td>
      <td>CZ</td>
      <td>48.974736</td>
      <td>14.474285</td>
      <td>66</td>
      <td>18000</td>
      <td>600</td>
      <td>road tariff</td>
      <td>30.0</td>
      <td>69.072717</td>
      <td>11.985857</td>
      <td>57.086860</td>
      <td>833.758</td>
      <td>1276.76</td>
    </tr>
    <tr>
      <td>T4</td>
      <td>s003 leg 1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>WH_Kecskemet</td>
      <td>HU</td>
      <td>46.894253</td>
      <td>19.686575</td>
      <td>66</td>
      <td>15000</td>
      <td>1500</td>
      <td>road tariff</td>
      <td>38.0</td>
      <td>251.460390</td>
      <td>43.634714</td>
      <td>207.825676</td>
      <td>3035.310</td>
      <td>2899.25</td>
    </tr>
    <tr>
      <td>T5</td>
      <td>s004 leg 1</td>
      <td>WH_Sindelfingen</td>
      <td>DE</td>
      <td>48.708416</td>
      <td>9.003545</td>
      <td>CU_Bari</td>
      <td>IT</td>
      <td>41.125784</td>
      <td>16.862029</td>
      <td>90</td>
      <td>50000</td>
      <td>2000</td>
      <td>road tariff</td>
      <td>67.0</td>
      <td>1204.617470</td>
      <td>209.031484</td>
      <td>995.585986</td>
      <td>14540.610</td>
      <td>5792.86</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\freight_matrix_plus.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>shipmentId</th>
      <th>shipmentDate</th>
      <th>fromLocationId</th>
      <th>fromCountry</th>
      <th>fromState</th>
      <th>fromCity</th>
      <th>fromPostalCode</th>
      <th>fromStreet</th>
      <th>fromZone</th>
      <th>toLocationId</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>fromStatus</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>toStatus</th>
      <th>row</th>
      <th>costs</th>
      <th>weightClass</th>
      <th>distanceClass</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>S001</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>1</td>
      <td>DE</td>
      <td></td>
      <td>BadHersfeld</td>
      <td></td>
      <td></td>
      <td>Z1</td>
      <td>1</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>ok</td>
      <td>50.776351</td>
      <td>6.083862</td>
      <td>ok</td>
      <td>1</td>
      <td>1326.875</td>
      <td>8000</td>
      <td>400</td>
    </tr>
    <tr>
      <td>S002</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>1</td>
      <td>DE</td>
      <td></td>
      <td>BadHersfeld</td>
      <td></td>
      <td></td>
      <td>Z1</td>
      <td>2</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>ok</td>
      <td>49.231634</td>
      <td>10.982855</td>
      <td>ok</td>
      <td>2</td>
      <td>1167.65</td>
      <td>8000</td>
      <td>300</td>
    </tr>
    <tr>
      <td>S003</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>1</td>
      <td>DE</td>
      <td></td>
      <td>BadHersfeld</td>
      <td></td>
      <td></td>
      <td>Z1</td>
      <td>3</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>ok</td>
      <td>49.241972</td>
      <td>10.963869</td>
      <td>ok</td>
      <td>3</td>
      <td>1167.65</td>
      <td>8000</td>
      <td>300</td>
    </tr>
    <tr>
      <td>S004</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>1</td>
      <td>DE</td>
      <td></td>
      <td>BadHersfeld</td>
      <td></td>
      <td></td>
      <td>Z1</td>
      <td>4</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>ok</td>
      <td>50.251629</td>
      <td>8.080199</td>
      <td>ok</td>
      <td>4</td>
      <td>1119.813</td>
      <td>20000</td>
      <td>220</td>
    </tr>
    <tr>
      <td>S005</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>1</td>
      <td>DE</td>
      <td></td>
      <td>BadHersfeld</td>
      <td></td>
      <td></td>
      <td>Z1</td>
      <td>5</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>ok</td>
      <td>51.579484</td>
      <td>9.752448</td>
      <td>ok</td>
      <td>5</td>
      <td>718.25</td>
      <td>13000</td>
      <td>120</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>shipmentId</th>
      <th>shipmentDate</th>
      <th>fromLocationId</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>fromZone</th>
      <th>toLocationId</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>toZone</th>
      <th>distance</th>
      <th>weight</th>
      <th>volume</th>
      <th>pallets</th>
      <th>loadingMeters</th>
      <th>fromCountry</th>
      <th>toCountry</th>
      <th>costs</th>
      <th>weightClass</th>
      <th>distanceClass</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>S001</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>BadHersfeld</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>Z1</td>
      <td>Aachen</td>
      <td>50.776351</td>
      <td>6.083862</td>
      <td>Z4</td>
      <td>330.0000</td>
      <td>7291</td>
      <td>12394</td>
      <td>1</td>
      <td>369</td>
      <td>DE</td>
      <td>DE</td>
      <td>1326.875</td>
      <td>8000</td>
      <td>400</td>
    </tr>
    <tr>
      <td>S023</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>BadHersfeld</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>Z1</td>
      <td>Aachen</td>
      <td>50.776351</td>
      <td>6.083862</td>
      <td>Z4</td>
      <td>325.1898</td>
      <td>4005</td>
      <td>15333</td>
      <td>1</td>
      <td>139</td>
      <td>DE</td>
      <td>DE</td>
      <td>1075.625</td>
      <td>5000</td>
      <td>400</td>
    </tr>
    <tr>
      <td>S002</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>BadHersfeld</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>Z1</td>
      <td>AbenbergerWald</td>
      <td>49.231634</td>
      <td>10.982855</td>
      <td>Z4</td>
      <td>295.4166</td>
      <td>6027</td>
      <td>2731</td>
      <td>1</td>
      <td>433</td>
      <td>DE</td>
      <td>DE</td>
      <td>1167.65</td>
      <td>8000</td>
      <td>300</td>
    </tr>
    <tr>
      <td>S003</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>BadHersfeld</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>Z1</td>
      <td>Abenberg</td>
      <td>49.241972</td>
      <td>10.963869</td>
      <td>Z4</td>
      <td>294.3474</td>
      <td>6586</td>
      <td>11141</td>
      <td>1</td>
      <td>147</td>
      <td>DE</td>
      <td>DE</td>
      <td>1167.65</td>
      <td>8000</td>
      <td>300</td>
    </tr>
    <tr>
      <td>S004</td>
      <td>2023-08-07T00:00:00.000Z</td>
      <td>BadHersfeld</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>Z1</td>
      <td>Aarbergen</td>
      <td>50.251629</td>
      <td>8.080199</td>
      <td>Z4</td>
      <td>193.9281</td>
      <td>13830</td>
      <td>14295</td>
      <td>1</td>
      <td>109</td>
      <td>DE</td>
      <td>DE</td>
      <td>1119.813</td>
      <td>20000</td>
      <td>220</td>
    </tr>
  </tbody>
</table>
</div>

You can create a freight matrix on the Log-hub Platform. Therefore, please create a workspace and click within the workspace on "Create Freight Matrix". There you can provide the matrix a name, select the matrix type and define all other parameters. 
To get the matrix id, please click on the "gear" icon. There you can copy & paste the matrix id that is needed in your API request.

<p align="left">
  <img src="examples\assets\CO2_emissions.png" alt="Header Image"  width="980"/>
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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>distanceUnit</th>
      <th>weightUnit</th>
      <th>co2Emission</th>
      <th>co2EmissionUnit</th>
      <th>calculationType</th>
      <th>distance</th>
      <th>shipmentId</th>
      <th>shipmentDate</th>
      <th>fromCountry</th>
      <th>fromState</th>
      <th>wellToTankCO2</th>
      <th>wellToTankCO2Unit</th>
      <th>tankToWheelCO2</th>
      <th>tankToWheelCO2Unit</th>
      <th>electricityGenerationCO2Emissions</th>
      <th>electricityGenerationCO2EmissionsUnit</th>
      <th>electricityTransmissionDistributionAndLosses</th>
      <th>electricityTransmissionDistributionAndLossesUnit</th>
      <th>electricityProduction</th>
      <th>electricityProductionUnit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>31.628705</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>366.14</td>
      <td>shipment_1</td>
      <td>2022-10-27T00:00:00.000Z</td>
      <td>DE</td>
      <td>Hessen</td>
      <td>5.488377</td>
      <td>KG</td>
      <td>26.140328</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>32.623517</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>424.80</td>
      <td>shipment_2</td>
      <td>2022-11-24T00:00:00.000Z</td>
      <td>DE</td>
      <td>Hessen</td>
      <td>5.661002</td>
      <td>KG</td>
      <td>26.962515</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>7.984966</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>251.63</td>
      <td>shipment_3</td>
      <td>2022-10-19T00:00:00.000Z</td>
      <td>DE</td>
      <td>Hessen</td>
      <td>1.385593</td>
      <td>KG</td>
      <td>6.599373</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>10.231794</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>253.50</td>
      <td>shipment_4</td>
      <td>2022-12-01T00:00:00.000Z</td>
      <td>DE</td>
      <td>Hessen</td>
      <td>1.775474</td>
      <td>KG</td>
      <td>8.456320</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>10.961394</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>222.00</td>
      <td>shipment_5</td>
      <td>2022-09-22T00:00:00.000Z</td>
      <td>DE</td>
      <td>Hessen</td>
      <td>1.902078</td>
      <td>KG</td>
      <td>9.059316</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>distanceUnit</th>
      <th>weightUnit</th>
      <th>co2Emission</th>
      <th>co2EmissionUnit</th>
      <th>calculationType</th>
      <th>distance</th>
      <th>shipmentId</th>
      <th>shipmentDate</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>wellToTankCO2</th>
      <th>wellToTankCO2Unit</th>
      <th>tankToWheelCO2</th>
      <th>tankToWheelCO2Unit</th>
      <th>electricityGenerationCO2Emissions</th>
      <th>electricityGenerationCO2EmissionsUnit</th>
      <th>electricityTransmissionDistributionAndLosses</th>
      <th>electricityTransmissionDistributionAndLossesUnit</th>
      <th>electricityProduction</th>
      <th>electricityProductionUnit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>31.628705</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>366.14</td>
      <td>shipment_001</td>
      <td>2022-10-27T00:00:00.000Z</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>5.488377</td>
      <td>KG</td>
      <td>26.140328</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>32.623517</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>424.80</td>
      <td>shipment_002</td>
      <td>2022-11-24T00:00:00.000Z</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>5.661002</td>
      <td>KG</td>
      <td>26.962515</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>7.984966</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>251.63</td>
      <td>shipment_003</td>
      <td>2022-10-19T00:00:00.000Z</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>1.385593</td>
      <td>KG</td>
      <td>6.599373</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>10.214841</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>253.08</td>
      <td>shipment_004</td>
      <td>2022-12-01T00:00:00.000Z</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>1.772532</td>
      <td>KG</td>
      <td>8.442309</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <td>KM</td>
      <td>KG</td>
      <td>10.961394</td>
      <td>KG</td>
      <td>ROAD</td>
      <td>222.00</td>
      <td>shipment_005</td>
      <td>2022-09-22T00:00:00.000Z</td>
      <td>50.868134</td>
      <td>9.706848</td>
      <td>1.902078</td>
      <td>KG</td>
      <td>9.059316</td>
      <td>KG</td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
      <td>0</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>

#### Forward CO2 Emissions Rail
Calculating a CO2 footprint based on your shipments transported by train.

```python
from pyloghub.freight_shipment_emissions_rail import forward_freight_shipment_emissions_rail_sample_data, forward_freight_shipment_emissions_rail

sample_data = forward_freight_shipment_emissions_rail_sample_data()
addresses_df = sample_data['addresses']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

freight_emissions_df = forward_freight_shipment_emissions_rail(addresses_df, parameters, api_key, save_scenario, show_buttons=True)
freight_emissions_df.head()
```

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>weightUnit</th>
      <th>co2Emission</th>
      <th>co2EmissionUnit</th>
      <th>calculationType</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>distance</th>
      <th>distanceUnit</th>
      <th>shipmentId</th>
      <th>shipmentDate</th>
      <th>weight</th>
      <th>wellToTankCO2</th>
      <th>wellToTankCO2Unit</th>
      <th>tankToWheelCO2</th>
      <th>tankToWheelCO2Unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>KG</td>
      <td>13.410046</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>50.10226</td>
      <td>8.69282</td>
      <td>521.881</td>
      <td>KM</td>
      <td>shipment_1</td>
      <td>2022-10-27T00:00:00.000Z</td>
      <td>931</td>
      <td>2.720879</td>
      <td>KG</td>
      <td>10.689167</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>16.467095</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>48.03533</td>
      <td>11.59313</td>
      <td>643.618</td>
      <td>KM</td>
      <td>shipment_2</td>
      <td>2022-10-27T00:00:00.000Z</td>
      <td>927</td>
      <td>3.341150</td>
      <td>KG</td>
      <td>13.125945</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>4.332314</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>52.37660</td>
      <td>9.74135</td>
      <td>263.369</td>
      <td>KM</td>
      <td>shipment_3</td>
      <td>2022-11-24T00:00:00.000Z</td>
      <td>596</td>
      <td>0.879020</td>
      <td>KG</td>
      <td>3.453294</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>15.084405</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>48.76956</td>
      <td>9.25974</td>
      <td>642.984</td>
      <td>KM</td>
      <td>shipment_4</td>
      <td>2022-11-15T00:00:00.000Z</td>
      <td>850</td>
      <td>3.060604</td>
      <td>KG</td>
      <td>12.023801</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>4.489627</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>51.21178</td>
      <td>6.75227</td>
      <td>540.424</td>
      <td>KM</td>
      <td>shipment_5</td>
      <td>2022-11-15T00:00:00.000Z</td>
      <td>301</td>
      <td>0.910939</td>
      <td>KG</td>
      <td>3.578688</td>
      <td>KG</td>
    </tr>
  </tbody>
</table>
</div>

#### Reverse CO2 Emissions Rail
Calculating a CO2 footprint based on your shipments transported by train.

```python
from pyloghub.freight_shipment_emissions_rail import reverse_freight_shipment_emissions_rail_sample_data, reverse_freight_shipment_emissions_rail

sample_data = reverse_freight_shipment_emissions_rail_sample_data()
coordinates_df = sample_data['coordinates']
parameters = sample_data['parameters']

save_scenario = sample_data['saveScenarioParameters']
save_scenario['saveScenario'] = True
save_scenario['workspaceId'] = "YOUR WORKSPACE ID"
save_scenario['scenarioName'] = "YOUR SCENARIO NAME"

freight_emissions_df = reverse_freight_shipment_emissions_rail(coordinates_df, parameters, api_key, save_scenario, show_buttons=True)
freight_emissions_df.head()
```

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>weightUnit</th>
      <th>co2Emission</th>
      <th>co2EmissionUnit</th>
      <th>calculationType</th>
      <th>distance</th>
      <th>distanceUnit</th>
      <th>shipmentId</th>
      <th>shipmentDate</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>weight</th>
      <th>wellToTankCO2</th>
      <th>wellToTankCO2Unit</th>
      <th>tankToWheelCO2</th>
      <th>tankToWheelCO2Unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>KG</td>
      <td>13.410046</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>521.881</td>
      <td>KM</td>
      <td>shipment_1</td>
      <td>2022-10-27T00:00:00.000Z</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>50.10226</td>
      <td>8.69282</td>
      <td>931</td>
      <td>2.720879</td>
      <td>KG</td>
      <td>10.689167</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>16.467095</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>643.618</td>
      <td>KM</td>
      <td>shipment_2</td>
      <td>2022-10-27T00:00:00.000Z</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>48.03533</td>
      <td>11.59313</td>
      <td>927</td>
      <td>3.341150</td>
      <td>KG</td>
      <td>13.125945</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>4.332314</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>263.369</td>
      <td>KM</td>
      <td>shipment_3</td>
      <td>2022-11-24T00:00:00.000Z</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>52.37660</td>
      <td>9.74135</td>
      <td>596</td>
      <td>0.879020</td>
      <td>KG</td>
      <td>3.453294</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>15.084405</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>642.984</td>
      <td>KM</td>
      <td>shipment_4</td>
      <td>2022-11-15T00:00:00.000Z</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>48.76956</td>
      <td>9.25974</td>
      <td>850</td>
      <td>3.060604</td>
      <td>KG</td>
      <td>12.023801</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>4.489627</td>
      <td>KG</td>
      <td>RAIL</td>
      <td>540.424</td>
      <td>KM</td>
      <td>shipment_5</td>
      <td>2022-11-15T00:00:00.000Z</td>
      <td>52.52257</td>
      <td>13.40242</td>
      <td>51.21178</td>
      <td>6.75227</td>
      <td>301</td>
      <td>0.910939</td>
      <td>KG</td>
      <td>3.578688</td>
      <td>KG</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>weightUnit</th>
      <th>co2Emission</th>
      <th>co2EmissionUnit</th>
      <th>calculationType</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>shipmentId</th>
      <th>shipmentDate</th>
      <th>fromIataCode</th>
      <th>toIataCode</th>
      <th>flightNumber</th>
      <th>isRefrigirated</th>
      <th>weight</th>
      <th>distance</th>
      <th>wellToTankCO2</th>
      <th>wellToTankCO2Unit</th>
      <th>tankToWheelCO2</th>
      <th>tankToWheelCO2Unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>KG</td>
      <td>708.924636</td>
      <td>KG</td>
      <td>AIR</td>
      <td>50.03652</td>
      <td>8.56127</td>
      <td>61.1744</td>
      <td>-149.996</td>
      <td>shipment_001</td>
      <td>2022-09-01T00:00:00.000Z</td>
      <td>FRA</td>
      <td>ANC</td>
      <td></td>
      <td>no</td>
      <td>150</td>
      <td>7501.837369</td>
      <td>127.838869</td>
      <td>KG</td>
      <td>581.085767</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>236.308212</td>
      <td>KG</td>
      <td>AIR</td>
      <td>50.03652</td>
      <td>8.56127</td>
      <td>61.1744</td>
      <td>-149.996</td>
      <td>shipment_002</td>
      <td>2022-09-02T00:00:00.000Z</td>
      <td>FRA</td>
      <td>ANC</td>
      <td></td>
      <td>no</td>
      <td>50</td>
      <td>7501.837369</td>
      <td>42.612956</td>
      <td>KG</td>
      <td>193.695256</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>1417.849272</td>
      <td>KG</td>
      <td>AIR</td>
      <td>50.03652</td>
      <td>8.56127</td>
      <td>61.1744</td>
      <td>-149.996</td>
      <td>shipment_003</td>
      <td>2022-09-03T00:00:00.000Z</td>
      <td>FRA</td>
      <td>ANC</td>
      <td></td>
      <td>no</td>
      <td>300</td>
      <td>7501.837369</td>
      <td>255.677738</td>
      <td>KG</td>
      <td>1162.171534</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>1181.541060</td>
      <td>KG</td>
      <td>AIR</td>
      <td>50.03652</td>
      <td>8.56127</td>
      <td>61.1744</td>
      <td>-149.996</td>
      <td>shipment_004</td>
      <td>2022-09-04T00:00:00.000Z</td>
      <td>FRA</td>
      <td>ANC</td>
      <td></td>
      <td>no</td>
      <td>250</td>
      <td>7501.837369</td>
      <td>213.064781</td>
      <td>KG</td>
      <td>968.476279</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>945.232848</td>
      <td>KG</td>
      <td>AIR</td>
      <td>50.03652</td>
      <td>8.56127</td>
      <td>61.1744</td>
      <td>-149.996</td>
      <td>shipment_005</td>
      <td>2022-09-05T00:00:00.000Z</td>
      <td>FRA</td>
      <td>ANC</td>
      <td></td>
      <td>no</td>
      <td>200</td>
      <td>7501.837369</td>
      <td>170.451825</td>
      <td>KG</td>
      <td>774.781023</td>
      <td>KG</td>
    </tr>
  </tbody>
</table>
</div>

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

#### Output
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">🌍 Open Map</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📊 Open Dashboard</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Input Dataset</button>
</a>
<a href="https://production.supply-chain-apps.log-hub.com/sca/login" target="_blank" style="text-decoration: none; display: inline-block; margin-right: 10px;">
    <button class="button-style">📋 Show Output Dataset</button>
</a>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>weightUnit</th>
      <th>co2Emission</th>
      <th>co2EmissionUnit</th>
      <th>calculationType</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>shipmentId</th>
      <th>shipmentDate</th>
      <th>fromUnLocode</th>
      <th>toUnLocode</th>
      <th>vesselId</th>
      <th>isRefrigirated</th>
      <th>weight</th>
      <th>distance</th>
      <th>wellToTankCO2</th>
      <th>wellToTankCO2Unit</th>
      <th>tankToWheelCO2</th>
      <th>tankToWheelCO2Unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>KG</td>
      <td>43.978836</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>31.33460</td>
      <td>121.70620</td>
      <td>shipment_001</td>
      <td>2022-10-03T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>CNSHG</td>
      <td></td>
      <td>no</td>
      <td>336</td>
      <td>25664.551927</td>
      <td>3.449320</td>
      <td>KG</td>
      <td>40.529516</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>23.498787</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>1.26760</td>
      <td>103.75710</td>
      <td>shipment_002</td>
      <td>2022-10-03T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>SGSIN</td>
      <td></td>
      <td>no</td>
      <td>204</td>
      <td>22586.211164</td>
      <td>1.843042</td>
      <td>KG</td>
      <td>21.655745</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>58.253702</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>22.49668</td>
      <td>113.86191</td>
      <td>shipment_003</td>
      <td>2022-10-03T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>CNSZX</td>
      <td></td>
      <td>no</td>
      <td>460</td>
      <td>24830.981719</td>
      <td>4.568918</td>
      <td>KG</td>
      <td>53.684784</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>47.230909</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>29.96419</td>
      <td>121.95943</td>
      <td>shipment_004</td>
      <td>2022-10-03T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>CNZOS</td>
      <td></td>
      <td>no</td>
      <td>360</td>
      <td>25724.861317</td>
      <td>3.704385</td>
      <td>KG</td>
      <td>43.526524</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>38.189898</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>23.07580</td>
      <td>113.44680</td>
      <td>shipment_005</td>
      <td>2022-10-04T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>CNGZG</td>
      <td></td>
      <td>no</td>
      <td>301</td>
      <td>24877.698839</td>
      <td>2.995286</td>
      <td>KG</td>
      <td>35.194612</td>
      <td>KG</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\demand_forecasting.png" alt="Header Image"  width="980"/>
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

#### Output

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>weightUnit</th>
      <th>co2Emission</th>
      <th>co2EmissionUnit</th>
      <th>calculationType</th>
      <th>fromLatitude</th>
      <th>fromLongitude</th>
      <th>toLatitude</th>
      <th>toLongitude</th>
      <th>shipmentId</th>
      <th>shipmentDate</th>
      <th>fromUnLocode</th>
      <th>toUnLocode</th>
      <th>vesselId</th>
      <th>isRefrigirated</th>
      <th>weight</th>
      <th>distance</th>
      <th>wellToTankCO2</th>
      <th>wellToTankCO2Unit</th>
      <th>tankToWheelCO2</th>
      <th>tankToWheelCO2Unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>KG</td>
      <td>43.978836</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>31.33460</td>
      <td>121.70620</td>
      <td>shipment_001</td>
      <td>2022-10-03T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>CNSHG</td>
      <td></td>
      <td>no</td>
      <td>336</td>
      <td>25664.551927</td>
      <td>3.449320</td>
      <td>KG</td>
      <td>40.529516</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>23.498787</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>1.26760</td>
      <td>103.75710</td>
      <td>shipment_002</td>
      <td>2022-10-03T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>SGSIN</td>
      <td></td>
      <td>no</td>
      <td>204</td>
      <td>22586.211164</td>
      <td>1.843042</td>
      <td>KG</td>
      <td>21.655745</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>58.253702</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>22.49668</td>
      <td>113.86191</td>
      <td>shipment_003</td>
      <td>2022-10-03T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>CNSZX</td>
      <td></td>
      <td>no</td>
      <td>460</td>
      <td>24830.981719</td>
      <td>4.568918</td>
      <td>KG</td>
      <td>53.684784</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>47.230909</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>29.96419</td>
      <td>121.95943</td>
      <td>shipment_004</td>
      <td>2022-10-03T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>CNZOS</td>
      <td></td>
      <td>no</td>
      <td>360</td>
      <td>25724.861317</td>
      <td>3.704385</td>
      <td>KG</td>
      <td>43.526524</td>
      <td>KG</td>
    </tr>
    <tr>
      <td>KG</td>
      <td>38.189898</td>
      <td>KG</td>
      <td>SEA</td>
      <td>53.5425</td>
      <td>9.9038</td>
      <td>23.07580</td>
      <td>113.44680</td>
      <td>shipment_005</td>
      <td>2022-10-04T00:00:00.000Z</td>
      <td>DEHAM</td>
      <td>CNGZG</td>
      <td></td>
      <td>no</td>
      <td>301</td>
      <td>24877.698839</td>
      <td>2.995286</td>
      <td>KG</td>
      <td>35.194612</td>
      <td>KG</td>
    </tr>
  </tbody>
</table>
</div>

<p align="left">
  <img src="examples\assets\log_hub_tables.png" alt="Header Image"  width="980"/>
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

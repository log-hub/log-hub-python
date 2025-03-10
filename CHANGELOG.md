# Changelog

All notable changes to the `log_hub` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-03-15

### Added
- `forward_milkrun_optimization` service to improve efficiency in transportation and delivery processes by assign shipments to vehicles in an optimal way, based on shipments addresses and available vehicles.
- `reverse_milkrun_optimization` service to improve efficiency in transportation and delivery processes by assign shipments to vehicles in an optimal way, based on shipments coordinates and available vehicles.
- `forward_transport_optimization` service to find the most efficient and cost-effective ways to plan, organize, and execute the movement of goods and services, based on location addresses, available vehicles and shipments.
- `reverse_transport_optimization` service to find the most efficient and cost-effective ways to plan, organize, and execute the movement of goods and services, based on location coordinates, available vehicles and shipments.
- `forward_isochrone` to depict areas that can be reached within a certain time frame or distance from a specific location address. Calculating isochrones helps in visualizing accessibility and optimizing routes for travel.
- `reverse_isochrone` to depict areas that can be reached within a certain time frame or distance from a specific location coordinates. Calculating isochrones helps in visualizing accessibility and optimizing routes for travel.
- `forward_isochrone_plus` to depict areas that can be reached within a certain time frame or distance from a specific location address, calculating the isochrones with the additional parameters.
- `reverse_isochrone_plus` to depict areas that can be reached within a certain time frame or distance from a specific location coordinates, calculating the isochrones with the additional parameters.
- `get_workspace_entities` to fetch all the entities in the given workspace.

### Changed
- Input data validation is improved by separating mandatory and optional columns, as well as by adding table names in which data validation failed.
- All the functions that have the possibility of saving the scenario on the Log-hub Platform are updated with the `show_buttons` parameter. If the parameter is triggered, the buttons linking to the output results will be created.

### Fixed
- N/A (no fixes in this release).

### Deprecated
- N/A (no deprecations in this release).

### Removed
- N/A (no removals in this release). 

## [0.1.4] - 2025-02-25

### Added
- `forward_center_of_gravity_plus` service to calculate the center of gravity based on the given addresses. The addresses can refer to customers, suppliers or something else, and their respective weights, volumes and revenues.
- `reverse_center_of_gravity_plus` service to calculate the center of gravity based on the given coordinates. The coordinates can refer to customers, suppliers or something else, and their respective weights, volumes and revenues.
- `demand_forecasting` service to help you accurately predict future demand for your products based on historical demand data, future impact factors and parameters that customize the forecasting model for each product. 
- `forward_fixed_center_of_gravity` service to calculate the center of gravity based on the given addresses that refer to customers, suppliers or something else, their respective weights, and the table of the center addresses that are fixed.
- `reverse_fixed_center_of_gravity` service to calculate the center of gravity based on the given coordinates that refer to customers, suppliers or something else, their respective weights, and the table of the center coordinates that are fixed.
- `forward_freight_shipment_emissions_air` service to calculate a CO2 footprint based on your shipments or route legs defined as separate shipments transported by air with the IATA codes provided.
- `forward_freight_shipment_emissions_rail` service to calculate a CO2 footprint based on your shipments or route legs defined as separate shipments transported by train with the UN/LOCODEs provided.
- `reverse_freight_shipment_emissions_rail` service to calculate a CO2 footprint based on your shipments or route legs defined as separate shipments transported by train with the coordinates provided.
- `forward_freight_shipment_emissions_road` service to calculate a CO2 footprint based on your shipments or route legs defined as separate shipments transported by road with the addresses provided.
- `reverse_freight_shipment_emissions_road` service to calculate a CO2 footprint based on your shipments or route legs defined as separate shipments transported by road with the coordinates provided.
- `forward_freight_shipment_emissions_sea` service to calculate a CO2 footprint based on your shipments or route legs defined as separate shipments transported by ship with the UN/LOCODEs provided.
- `forward_location_planning` servise to optimize distribution modeling flows from the warehouses to the customers based on their addresses. For customers are also taken in consideration weight, volume and number of shipments, and for warehouses minimum and maximum capacity along with the penalty and fixed costs. Transport costs can also be adjusted.
- `reverse_location_planning` servise to optimize distribution modeling flows from the warehouses to the customers based on their coordinates. For customers are also taken in consideration weight, volume and number of shipments, and for warehouses minimum and maximum capacity along with the penalty and fixed costs. Transport costs can also be adjusted.
- `forward_nearest_warehouses` servise to find a given number of nearest warehouses from a customer location (based on addresses). 
- `reverse_nearest_warehouses` servise to find a given number of nearest warehouses from a customer location (based on coordinates)
- `forward_network_design_plus` service to help you find the optimal number and location of warehouses that are assigned to the customers and factories, based on their addresses,  transport, handling and fixed warehouse costs. 
- `reverse_network_design_plus` service to help you find the optimal number and location of warehouses that are assigned to the customers and factories, based on their coordinates,  transport, handling and fixed warehouse costs. 
- `forward_supply_chain_map_areas` sevice to help you create a map visualization of the given areas.
- `forward_supply_chain_map_locations` sevice to help you create a map visualization of the locations (based on addresses).
- `reverse_supply_chain_map_locations` sevice to help you create a map visualization of the locations (based on coordinates).
- `reverse_supply_chain_map_polyline` sevice to help you create a map visualization of the polylines based on their coordinates.
- `forward_supply_chain_map_relations` sevice to help you create a map visualization of the relations (based on addresses).
- `reverse_supply_chain_map_relations` sevice to help you create a map visualization of the relations (based on coordinates).
- `forward_supply_chain_map_sea_routes` sevice to help you create a map visualization of the sea routes (based on UN/LOCODEs).
- `reverse_supply_chain_map_sea_routes` sevice to help you create a map visualization of the sea routes (based on coordinates).

### Changed
- Created module with the functions for validation of the input data.
- Added a possibility to save the data on the platform by adjusting the 'saveScenarioParameters'.
- Created a module for generating necessary data for sending requests, as well as sending requests itself.
- Updated documentation to include examples and usage guidelines for the newly added services, providing clear instructions for users to leverage these new features effectively.

### Fixed
- Minor bug fixes and performance improvements in API communication handling, especially regarding removing batches in sending requests to the geocoding and distance calculation API.
- Redused duplicated code.

### Deprecated
- N/A (no deprecations in this release).

### Removed
- N/A (no removals in this release).

### Security
- Strengthened security measures in API communication, especially in the sending get requests to the network design plus and location planning API servises, as well as in the saving output data on the platform. 

## [0.1.3] - 2024-04-16

### Added
- `forward_freight_matrix` service to evaluate shipments (based on addresses) against freight matrices stored on the Log-hub platform. This service enables users to calculate logistics costs by providing detailed shipment data, including origin and destination information, shipment weights, volumes, and other pertinent details. The evaluated shipments are returned as a pandas DataFrame.
- `reverse_freight_matrix` service to evaluate shipments (based on lat/lon) against freight matrices stored on the Log-hub platform. This service enables users to calculate logistics costs by providing detailed shipment data, including origin and destination information, shipment weights, volumes, and other pertinent details. The evaluated shipments are returned as a pandas DataFrame.

### Changed
- Enhanced the package's integration with the Log-hub API to support the newly added freight matrix evaluation services, ensuring seamless data exchange and processing.
- Updated documentation to include examples and usage guidelines for the `forward_freight_matrix` and `reverse_freight_matrix` services, providing clear instructions for users to leverage these new features effectively.

### Fixed
- Minor bug fixes and performance improvements in API communication handling, particularly related to the new freight matrix evaluation services, enhancing the stability and speed of data retrieval and submission processes.

### Deprecated
- N/A (no deprecations in this release).

### Removed
- N/A (no removals in this release).

### Security
- Implemented additional security measures for the new freight matrix evaluation services to protect sensitive shipment data during transmission to and from the Log-hub platform. This includes enhanced encryption for data in transit and stricter authentication checks.


## [0.1.2] - 2024-01-10

### Added
- Two new dataset functions: read_table and update_table.
    - The `read_table` function enables users to read data from a specified table on the Log-hub platform and convert it into a pandas DataFrame. This feature includes secure access via basic authentication and automatically formats DataFrame columns based on the table's metadata.
    - The `update_table` function allows users to update a table on the Log-hub platform using data from a local pandas DataFrame. It supports the inclusion of table metadata for accurate data structure representation.
- Enhanced logging for better tracking and debugging. This includes detailed log messages during various stages of data retrieval, conversion, and updating processes.

### Changed
- Improved error handling and reporting across the newly added functions, ensuring robustness and reliability of the package in various scenarios and data conditions.
- Refinements in the API communication process to enhance security and efficiency.

### Fixed
- N/A (no specific fixes in this release).

### Deprecated
- N/A (no deprecations in this release).

### Removed
- N/A (no removals in this release).

### Security
- Strengthened security measures in API communication, particularly in the read_table and update_table functions, with encoded authentication and improved error handling.

## [0.1.1] - 2023-12-14

### Added
- Rename to `pyloghub` Python package.


## [0.1.0] - 2023-12-14

### Added
- Initial release of the `log_hub` Python package.
- Support for several Supply Chain Visualization, Network Design Optimization, and Transport Optimization services.
- Integration capabilities with the Log-hub API.
    - Features for Forward and Reverse Geocoding.
    - Forward and Reverse Distance Calculation functionalities.
    - Network Design Optimization tools including various Center of Gravity models.
    - Transport Optimization features including Milkrun Optimization and Transport Optimization Plus.
    - Shipment Analyzer for both forward and reverse directions.
- Comprehensive README file for installation, configuration, and usage instructions.
- Sample data and usage examples for key functionalities.
- Support for Python 3.10 and later.
- Virtual environment setup instructions for isolated development.
- MIT License for open and permissive software distribution.
- Secure API key handling for user authentication and data security.

### Fixed
- N/A (initial release).

### Deprecated
- N/A (initial release).

### Removed
- N/A (initial release).

### Security
- Initial implementation of security measures for API communication and data handling.


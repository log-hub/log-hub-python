# Changelog

All notable changes to the `log_hub` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).



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


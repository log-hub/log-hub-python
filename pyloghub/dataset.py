import os
import requests
import pandas as pd
import logging
import json
import base64
from urllib.parse import urlparse
logging.basicConfig(level=logging.INFO)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_table(table_link, email, api_key):
    """
    Reads data from a specified table on the Log-hub platform and converts it into a pandas DataFrame. The function uses basic authentication for secure access and formats the DataFrame columns based on the table's metadata.

    This function is designed to simplify the process of retrieving data from a Log-hub table. It fetches both the data and its associated metadata to ensure the data types in the pandas DataFrame match those in the Log-hub table.

    Parameters:
    table_link (str): The URL link to the specific table on the Log-hub platform. This link should direct to the API endpoint where the table data can be accessed.
    email (str): The email address used for Log-hub authentication.
    api_key (str): The API key associated with your Log-hub account for authentication.

    Returns:
    pd.DataFrame/None: A pandas DataFrame containing the table's data formatted according to its metadata. Returns None if the data retrieval is unsuccessful, or if any errors occur during the process.

    Handling Errors:
    - If there are any issues in fetching the metadata or the data (like network issues, authentication failures, or incorrect URLs), the function logs an error and returns None.
    - Errors are also logged and None is returned in case of any unexpected issues during data type conversion or DataFrame creation.

    Example Usage:
    table_link = "https://production.supply-chain-apps.log-hub.com/api/v1/datasets/.../tables/.../rows"
    email = "your_email@example.com"
    api_key = "your_api_key"
    dataframe = read_table(table_link, email, api_key)

    Note: Replace the 'table_link', 'email', and 'api_key' with actual values from your Log-hub account.
    """


    def js_to_pd_dtype(js_dtype):
        """
        Maps JavaScript data types to pandas data types.

        Parameters:
        js_dtype (str): The JavaScript data type.

        Returns:
        dtype: The corresponding pandas data type.
        """
        return {
            'string': 'object',
            'number': 'float64',
            'date': 'datetime64[ns]',
            'boolean': 'bool'
        }.get(js_dtype, 'object')  # default to object if unknown type

    # Prepare the basic auth string
    auth_str = f"{email}:{api_key}"
    encoded_auth_str = base64.b64encode(auth_str.encode()).decode()

    # Headers for the request, including the basic authentication
    headers = {
        "Authorization": f"Basic {encoded_auth_str}"
    }

    # Construct metadata link from the table link
    metadata_link = '/'.join(table_link.split('/')[:-2])

    try:
        # Get the table metadata
        metadata_response = requests.get(metadata_link, headers=headers)
        if metadata_response.status_code != 200:
            logging.error(f"HTTP Error in metadata request: {metadata_response.status_code} - {metadata_response.text}")
            return None

        metadata_json = metadata_response.json()
        if 'data' not in metadata_json or not metadata_json['data']:
            logging.error("Metadata JSON does not contain 'data' key or it's empty")
            return None

        column_types = {col['propertyName']: js_to_pd_dtype(col['dataType']) for col in metadata_json['data'][0]['columns']}

        # Get the table data
        data_response = requests.get(table_link, headers=headers)
        if data_response.status_code != 200:
            logging.error(f"HTTP Error in data request: {data_response.status_code} - {data_response.text}")
            return None

        # Create DataFrame and format columns
        df = pd.DataFrame(data_response.json())
        for col, dtype in column_types.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception: {e}")
        return None
    except KeyError as e:
        logging.error(f"Key Error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None
    

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_ids_from_link(table_link):
    """
    Extracts dataset_id and table_id from the provided table link.

    Parameters:
    table_link (str): The link to the table.

    Returns:
    tuple: The dataset_id and table_id.
    """
    parsed_url = urlparse(table_link)
    path_segments = parsed_url.path.split('/')
    # Finding indices for 'datasets' and 'tables' in the path
    datasets_index = path_segments.index('datasets')
    tables_index = path_segments.index('tables')

    # The dataset_id is the segment following 'datasets'
    dataset_id = path_segments[datasets_index + 1]
    # The table_id is the segment following 'tables'
    table_id = path_segments[tables_index + 1]
    return dataset_id, table_id


def pd_to_js_dtype(pd_dtype):
    """
    Maps pandas data types to JavaScript data types.
    """
    if pd.api.types.is_string_dtype(pd_dtype):
        return 'string'
    elif pd.api.types.is_numeric_dtype(pd_dtype):
        return 'number'
    elif pd.api.types.is_datetime64_any_dtype(pd_dtype):
        return 'date'
    elif pd.api.types.is_bool_dtype(pd_dtype):
        return 'boolean'
    else:
        return 'string'  # default type

def create_metadata(dataframe, provided_metadata=None):
    """
    Creates metadata for the columns of the dataframe.

    Parameters:
    dataframe (pd.DataFrame): The dataframe to create metadata for.
    provided_metadata (dict, optional): Provided metadata to override defaults.

    Returns:
    list: A list of metadata dictionaries for each column.
    """
    metadata = []
    for col in dataframe.columns:
        col_metadata = {
            'name': col,
            'propertyName': col,
            'dataType': pd_to_js_dtype(dataframe[col].dtype),
            'format': 'General'
        }
        # Overriding with any provided metadata for the column
        if provided_metadata and col in provided_metadata:
            col_metadata.update(provided_metadata[col])
        metadata.append(col_metadata)
    return metadata

def update_table(table_link, dataframe, metadata, email, api_key):
    """
    Updates a table in a specific dataset on the Log-hub platform using data from a pandas DataFrame.

    This function is designed to easily push updates from a local DataFrame to a table hosted on the Log-hub platform. It requires a link to the specific table you wish to update, the DataFrame containing your data, metadata to describe the data structure, and your Log-hub authentication details.

    Parameters:
    table_link (str): A URL pointing to the specific table you want to update on the Log-hub platform. 
                      This link should be in the format provided by Log-hub for accessing tables.
    dataframe (pd.DataFrame): The DataFrame containing the data you want to upload. Ensure that the 
                              DataFrame structure (columns and data types) matches the structure of 
                              the table you're updating.
    metadata (dict): A dictionary that describes the structure and properties of your table and its columns. 
                     It can include the name of the table and detailed descriptions for each column.
                     If column metadata is not provided, it will be generated based on the DataFrame's structure.
    email (str): Your email address used for Log-hub authentication.
    api_key (str): Your Log-hub API key.

    The 'metadata' Dictionary:
    - 'table_name' (optional): A string representing the name of the table. Defaults to "Table 01" if not provided.
    - 'columns' (optional): A list of dictionaries, each representing a column in your table. Each dictionary should have:
        * 'name': The name of the column.
        * 'propertyName': A property name for the column, typically the same as 'name'.
        * 'dataType': The type of data in the column ('string', 'number', 'date', 'boolean').
        * 'format': The format of the data (e.g., 'General', 'Date').

    Example of 'metadata' dictionary:
    {
        'table_name': 'SalesData',  # Optional
        'columns': [  # Optional, but recommended for clarity
            {
                'name': 'ProductID',
                'propertyName': 'ProductID',
                'dataType': 'string',
                'format': 'General'
            },
            {
                'name': 'SaleAmount',
                'propertyName': 'SaleAmount',
                'dataType': 'number',
                'format': 'Currency'
            }
            # Add more columns as needed
        ]
    }

    Example Usage:
    table_link = "https://production.supply-chain-apps.log-hub.com/api/v1/datasets/.../tables/.../rows"
    dataframe = pd.DataFrame({'ProductID': ['P123', 'P456'], 'SaleAmount': [150, 200]})
    metadata = {
        'table_name': 'SalesData',
        'columns': [
            {'name': 'ProductID', 'propertyName': 'ProductID', 'dataType': 'string', 'format': 'General'},
            {'name': 'SaleAmount', 'propertyName': 'SaleAmount', 'dataType': 'number', 'format': 'Currency'}
        ]
    }
    update_table(table_link, dataframe, metadata, 'your_email@example.com', 'your_api_key')
    
    Note: The function handles the connection and data transfer to Log-hub. It logs success or error messages and returns None.
    """
    dataset_id, table_id = extract_ids_from_link(table_link)

    # Prepare the basic auth string
    auth_str = f"{email}:{api_key}"
    encoded_auth_str = base64.b64encode(auth_str.encode()).decode()

    # Headers for the request
    headers = {
        "Authorization": f"Basic {encoded_auth_str}",
        "Content-Type": "application/json"
    }

    # Set table name in metadata
    table_name = metadata.get('table_name', "Table 01")

    # Create metadata if not provided or if it does not contain column information
    if not metadata or 'columns' not in metadata:
        metadata = {'columns': create_metadata(dataframe, provided_metadata=metadata)}

    # Prepare data for update including the table name and columns metadata
    update_data = {
        "name": table_name,
        "columns": metadata['columns'],
        "rows": dataframe.to_dict(orient='records')
    }

    url = f"https://production.supply-chain-apps.log-hub.com/api/v1/datasets/{dataset_id}/tables/{table_id}"

    try:
        # Send PATCH request
        response = requests.patch(url, headers=headers, data=json.dumps(update_data))

        # Check if the request was successful
        if response.status_code == 200:
            logging.info("Table updated successfully.")
            # return response.json()
            return None
        else:
            logging.error(f"Failed to update table. Status code: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception: {e}")
        return None
import logging
import pandas as pd

def validate_and_convert_data_types(df, required_columns):
    """
    Validate and convert the data types of the DataFrame columns.
    Log an error message if a required column is missing or if conversion fails.
    """
    for col, dtype in required_columns.items():
        if col not in df.columns:
            logging.error(f"Missing required column: {col}")
            return None
        try:
            df[col] = df[col].astype(dtype)
        except Exception as e:
            logging.error(f"Data type conversion failed for column '{col}': {e}")
            return None
    return df

def convert_dates(df, date_columns):
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
        return df

def convert_to_string(df, string_columns):
        for col in string_columns:
            df[col] = df[col].astype(str)
        return df

def convert_to_float(df, float_columns):
        for col in float_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

def convert_df_to_dict_excluding_nan(df, columns_to_check):
        """
        Convert a DataFrame to a list of dictionaries, excluding specified keys if their values are NaN.

        Parameters:
        df (pd.DataFrame): The DataFrame to convert.
        columns_to_check (list): List of column names to check for NaN values.

        Returns:
        list: A list of dictionaries representing the rows of the DataFrame, excluding keys for NaN values in specified columns.
        """
        records = []
        for _, row in df.iterrows():
            record = {}
            for column, value in row.items():
                if pd.notna(value) or column not in columns_to_check:
                    record[column] = value
            records.append(record)
        return records

def convert_timestamps(df):
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return df

def validate_boolean(value):
        return isinstance(value, bool)


def exclude_nan_depending_on_dtype(df, columns_to_check):
    """
    Convert a DataFrame to a list of dictionaries, excluding specified keys if their values are NaN.

    Parameters:
    df (pd.DataFrame): The DataFrame to convert.
    columns_to_check (list): List of column names to check for NaN values.

    Returns:
    list: A list of dictionaries representing the rows of the DataFrame, excluding keys for NaN values in specified columns.
    """
    records = []
    for ind, row in df.iterrows():
        record = {}
        for column, value in row.items():
            if column not in columns_to_check:
                logging.error(f"Missing required column: {column}")
                return None
            elif columns_to_check[column] == 'float':
                df.loc[ind, column] = pd.to_numeric(df[column][ind], errors='coerce')
                if pd.notna(df[column][ind]):
                    record[column] = float(df[column][ind])
            elif columns_to_check[column] == 'str':
                df.loc[ind, column] = str(df[column][ind])
                record[column] = df[column].loc[ind]
        records.append(record)
    return records
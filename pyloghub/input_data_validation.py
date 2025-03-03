import logging
import pandas as pd

def validate_and_convert_data_types(df, required_columns, column_type):
    """
    Validate and convert the data types of the DataFrame columns.
    Log an error message if a mandatory column is missing or if conversion fails.
    """
    for col, dtype in required_columns.items():
        if column_type == 'mandatory':
            if col not in df.columns:
                logging.error(f"Missing a mandatory column: {col}")
                return None
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                logging.error(f"Data type conversion failed for column '{col}': {e}")
                return None
        elif column_type == 'optional':
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except Exception as e:
                    logging.error(f"Data type conversion failed for column '{col}': {e}")
                    return None
    return df

def convert_dates(df, date_columns):
        """
        Converts the DataFrame date columns.
        """
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
        return df

def convert_to_string(df, string_columns):
        """
        Converts the DataFrame string columns.
        """
        for col in string_columns:
            df[col] = df[col].astype(str)
        return df

def convert_to_float(df, float_columns, column_type):
        """
        Converts the DataFrame numeric columns.
        """
        for col in float_columns:
            if column_type == 'mandatory':
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif column_type == 'optional':
                 if col in df.columns:
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
        """
        Converts the DataFrame date columns to a timestamp format.
        """
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return df

def validate_boolean(value):
        """
        Validating the boolean values.
        """
        return isinstance(value, bool)


def exclude_nan_depending_on_dtype(df, columns_to_check, df_name):
    """
    Convert a DataFrame to a list of dictionaries, excluding specified keys if their values are NaN.

    Parameters:
    df (pd.DataFrame): The DataFrame to convert.
    columns_to_check (list): List of column names to check for NaN values.

    Returns:
    list: A list of dictionaries representing the rows of the DataFrame, excluding keys for NaN values in specified columns.
    """
    records = []
    if len(set(columns_to_check) - set(df.columns))>0:
        missing_columns = set(columns_to_check) - set(df.columns) 
        logging.error(f"Table {df_name} is missing mandatory column: {', '.join(list(missing_columns))}")
        return None
    else:
        for ind, row in df.iterrows():
            record = {}
            for column, value in row.items():
                if columns_to_check[column] == 'float':
                    df.loc[ind, column] = pd.to_numeric(df[column][ind], errors='coerce')
                    if pd.notna(df[column][ind]):
                        record[column] = float(df[column][ind])
                elif columns_to_check[column] == 'str':
                    df.loc[ind, column] = str(df[column][ind])
                    record[column] = df[column].loc[ind]
            records.append(record)
        return records

def remove_nonexisting_optional_columns(optional_columns, sent_columns):
    updated_optional_columns = optional_columns.copy()
    for col in optional_columns.keys():
        if not col in sent_columns:
            updated_optional_columns.pop(col) 

    return updated_optional_columns
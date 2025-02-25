import os
import requests
import logging
import time


def create_url(app_name):
    """
    Creates an url for the given application.
    """
    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net/"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}/api/applications/v1/"+app_name

    return url

def create_headers(api_key):
    
    headers = {
        "accept": "application/json",
        "authorization": f"apikey {api_key}",
        "content-type": "application/json"
    }

    return headers
def post_method(url, payload, headers, app_name):

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                return response_data
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in {app_name} API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None

def get_method(api_server, url, headers, app_name):

    #api_server = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net/"
    
    retry_delay = 15  # seconds
    timeout = 3600
    start_time = time.time()
    while True:
        response = requests.get(api_server + url, headers = headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data['calculationRunning']:
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    logging.error("Timeout of one hour is reached with the calculation still running. Try running the calculation again.")
                    return None
                
                logging.info(f"Calculation is still running with the progress {response_data['progress']}%.")
                time.sleep(retry_delay)
            else:
                return response_data
        else:
            logging.error(f"Error in {app_name} API: {response.status_code} - {response.text}")
            return None
    
def get_workspace_entities(workspace_id, api_key):

    DEFAULT_LOG_HUB_API_SERVER = "https://supply-chain-app-eu-supply-chain-eu-development.azurewebsites.net/"
    LOG_HUB_API_SERVER = os.getenv('LOG_HUB_API_SERVER', DEFAULT_LOG_HUB_API_SERVER)
    url = f"{LOG_HUB_API_SERVER}api/v1/workspace/"+ workspace_id + "/entitiesWithTables"

    max_retries = 3
    retry_delay = 15  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers={"authorization": f"apikey {api_key}"})
            if response.status_code == 200:
                response_data = response.json()
                return response_data
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Error in Entities With Tables API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

    logging.error("Max retries exceeded.")
    return None


import requests
import logging
from cachetools import cached, TTLCache

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

cache = TTLCache(maxsize=100, ttl=600)

@cached(cache)
def fetch_data(endpoint, **params):
    base_url = "https://external_api_url"
    full_url = f"{base_url}/{endpoint}/"
    
    try:
        response = requests.get(full_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Unexpected error occurred: {req_err}")
    return None

tour_id = 123
tour_details = fetch_data(endpoint="tours", id=tour_id)
logging.info(f"Tour Details: {tour_details}")

destination_id = 456
destination_details = fetch_data(endpoint="destinations", id=destination_id)
logging.info(f"Destination Details: {destination_details}")
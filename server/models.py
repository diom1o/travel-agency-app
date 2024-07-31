# Example: Using a simple caching mechanism for an external API call
import requests
from cachetools import cached, TTLCache

# Cache setup - stores up to 100 items and each cached item expires after 600 seconds (10 minutes)
cache = TTLCache(maxsize=100, ttl=600)

@cached(cache)
def fetch_tour_details(tour_id):
    # Replace 'external_api_url' with the actual API endpoint you're calling
    response = requests.get(f"https://external_api_url/tours/{tour_id}")
    if response.status_code == 200:
        return response.json()
    return None

# Usage example
tour_details = fetch_tour_details(tour_id=123)
import requests
import json
def fetch_realtime_availability(api_url):
    """Fetches real-time availability data from the car park availability API."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

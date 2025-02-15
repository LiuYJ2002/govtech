import requests

def fetch_realtime_availability(api_url):
    """
    Fetches real-time availability data from the car park API.

    Parameters:
    api_url (str): The API endpoint URL.

    Returns:
    dict: The JSON response if successful, None if an error occurs.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

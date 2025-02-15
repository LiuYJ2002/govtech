import pandas as pd

def merge_carpark_data(csv_data, api_data):
    """
    Merges car park data from a CSV file and real-time API data.

    Parameters:
    csv_data (pd.DataFrame): DataFrame containing static car park details.
    api_data (dict): Dictionary containing real-time car park availability data.

    Returns:
    pd.DataFrame: Merged DataFrame by carpark number containing both static and real-time data.
    """
    api_carparks = []
    #extract wanted data
    for item in api_data.get('items', []):
        for carpark in item.get('carpark_data', []):
            api_carparks.append({
                "car_park_no": carpark.get("carpark_number", "NA"),
                "carpark_info": carpark.get("carpark_info", "NA"),
                "update_datetime": carpark.get("update_datetime", "NA"),
            })
            
    api_df = pd.DataFrame(api_carparks)
    merged_data = pd.merge(csv_data, api_df, on="car_park_no", how="left")
    return merged_data



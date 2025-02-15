import pandas as pd

def merge_carpark_data(csv_data, api_data):
    api_carparks = []
    for item in api_data.get('items', []):
        for carpark in item.get('carpark_data', []):
            #carpark_info = carpark.get('carpark_info', [{}])  
            api_carparks.append({
                "car_park_no": carpark.get("carpark_number", "NA"),
                "carpark_info": carpark.get("carpark_info", "NA"),
                "update_datetime": carpark.get("update_datetime", "NA"),
            })

    api_df = pd.DataFrame(api_carparks)
    merged_data = pd.merge(csv_data, api_df, on="car_park_no", how="left")
    return merged_data



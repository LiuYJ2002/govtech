import pandas as pd
import os


def get_country_code(file_path):
    """
    Loads country code data from an Excel file and returns a dictionary mapping country codes to country names.

    Parameters:
    file_path (str): The path to the Excel file containing country codes and names.

    Returns:
    dict: A dictionary with country codes as keys and country names as values.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_excel(file_path)
    return dict(zip(df["Country Code"], df["Country"]))


def get_restaurant_data(json_file, country_codes_file, output_file):
    """
    Extracts restaurant details from a JSON file that matches with country code and saves the data to a CSV file.

    Parameters:
    json_file (str): The path to the JSON file containing restaurant data.
    country_codes (dict): A dictionary mapping country codes to country names.
    output_file (str): The path to the output CSV file where restaurant details will be saved.

    Returns:
    None
    """
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"File not found: {json_file}")
    
    df = pd.read_json(json_file, encoding='utf-8')
    restaurant_list = []

    country_codes = get_country_code(country_codes_file)

    for restaurants in df["restaurants"]:
        for restaurant in restaurants:
            country_code = restaurant["restaurant"]["location"].get("country_id", "NA")
            #check if the restaurant mactehs a country code
            if country_codes.get(country_code):
                event_dates = []
                if restaurant["restaurant"].get("zomato_events", "NA") != "NA":
                    for event in restaurant["restaurant"]["zomato_events"]:
                        event_dates.append(event.get("event", "NA").get("start_date", "NA"))
                else:
                    event_dates.append("NA")
                restaurant_list.append({
                    "Restaurant Id": restaurant["restaurant"]["R"].get("res_id", "NA"),
                    "Restaurant Name": restaurant["restaurant"].get("name", "NA"),
                    "Country": country_codes[country_code],
                    "City": restaurant["restaurant"]["location"].get("city", "NA"),
                    "User Rating Votes": restaurant["restaurant"]["user_rating"].get("votes", "NA"),
                    "User Aggregate Rating": restaurant["restaurant"]["user_rating"].get("aggregate_rating", "NA"),
                    "Cuisines": restaurant["restaurant"].get("cuisines", "NA"),
                    "Event Date": event_dates
                })

    restaurant_df = pd.DataFrame(restaurant_list)
    restaurant_df.to_csv(output_file, index=False)
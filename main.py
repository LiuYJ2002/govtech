import pandas as pd
from datetime import datetime
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


def get_restaurant_data(json_file, country_codes, output_file):
    """
    Extracts restaurant details from a JSON file and saves the data to a CSV file.

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

    for restaurants in df["restaurants"]:
        for restaurant in restaurants:
            country_code = restaurant["restaurant"]["location"].get("country_id", "NA")
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


def is_event_in_april_2019(start_date, end_date):
    """
    Checks if an event overlaps with April 2019.

    Parameters:
    start_date (str): The start date of the event in 'YYYY-MM-DD' format.
    end_date (str): The end date of the event in 'YYYY-MM-DD' format.

    Returns:
    bool: True if the event overlaps with April 2019, otherwise False.
    """
    event_start = datetime.strptime(start_date, "%Y-%m-%d")
    event_end = datetime.strptime(end_date, "%Y-%m-%d")

    april_start = datetime(2019, 4, 1)
    april_end = datetime(2019, 4, 30)

    return event_start <= april_end and event_end >= april_start


def get_restaurant_events(json_file, output_file):
    """
    Extracts restaurant event data for events that occurred in April 2019 and saves it to a CSV file.

    Parameters:
    json_file (str): The path to the JSON file containing restaurant data.
    output_file (str): The path to the output CSV file where event details will be saved.

    Returns:
    None
    """
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"File not found: {json_file}")
    
    df = pd.read_json(json_file, encoding='utf-8')
    event_list = []

    for restaurants in df["restaurants"]:
        for restaurant in restaurants:
            zomato_events = restaurant["restaurant"].get("zomato_events", "NA")
            if zomato_events != "NA":
                    for event in zomato_events:
                        event = event.get("event", "NA")
                        event_start = event.get("start_date", "NA")
                        event_end = event.get("end_date", "NA")
                        if event_start != "NA" and event_end != "NA":
                            if is_event_in_april_2019(event_start, event_end):
                                event_list.append({
                                    "Event Id": event.get("event_id", "NA"),
                                    "Restaurant Id": restaurant["restaurant"]["R"].get("res_id", "NA"),
                                    "Restaurant Name": restaurant["restaurant"].get("name", "NA"),
                                    "Photo URL": restaurant["restaurant"].get("photos_url", "NA"),
                                    "Event Title": event.get("title", "NA"),
                                    "Event Start Date": event_start,
                                    "Event End Date": event_end
                                })
               
    restaurant_df = pd.DataFrame(event_list)
    restaurant_df.to_csv(output_file, index=False)


def analyse_ratings(json_file):
    """
    Analyses and summarises restaurant ratings from a JSON file.

    Parameters:
    json_file (str): The path to the JSON file containing restaurant data.

    Returns:
    None
    """
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"File not found: {json_file}")
    
    df = pd.read_json(json_file, encoding='utf-8')
    ratings_data = []

    for restaurants in df["restaurants"]:
        for restaurant in restaurants:
            rating = restaurant["restaurant"]["user_rating"]["aggregate_rating"]
            rating_text = restaurant["restaurant"]["user_rating"]["rating_text"]
            rating = float(rating)
            ratings_data.append((rating, rating_text))

    df = pd.DataFrame(ratings_data, columns=["Rating", "Rating Text"])
    rating_summary = df.groupby("Rating Text")["Rating"].agg(["min", "max", "mean", "count"]).sort_index()
    print(rating_summary)


if __name__ == "__main__":
    country_codes = get_country_code("data/Country-Code.xlsx")
    get_restaurant_data("data/restaurant_data.json", country_codes, "output/restaurant_details.csv")
    get_restaurant_events("data/restaurant_data.json", "output/restaurant_events.csv")
    analyse_ratings("data/restaurant_data.json")
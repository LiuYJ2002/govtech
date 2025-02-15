import pandas as pd
from datetime import datetime
import os

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
    Extracts restaurant event data for events that overlaps with April 2019 and saves it to a CSV file.

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
            #check if the restaurant has events
            if zomato_events != "NA":
                    for event in zomato_events:
                        event = event.get("event", "NA")
                        event_start = event.get("start_date", "NA")
                        event_end = event.get("end_date", "NA")
                        if event_start != "NA" and event_end != "NA":
                            #check if it overlaps with april 2019
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




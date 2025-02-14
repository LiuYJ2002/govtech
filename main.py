import pandas as pd

def get_country_code(file_path):
    # Load the data
    df = pd.read_excel(file_path)
    return dict(zip(df["Country Code"], df["Country"]))

# Extract restaurant details
# Only include restaurants with matching Country Codes from Country-Code.xlsx
# Fields to extract:
# ●	Restaurant Id
# ●	Restaurant Name
# ●	Country
# ●	City
# ●	User Rating Votes
# ●	User Aggregate Rating (as float)
# ●	Cuisines
# ●	Event Date
#●	Handle missing values by populating with "NA"
def get_restaurant_data(json_file, country_codes, output_file):
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

if __name__ == "__main__":
    country_codes = get_country_code("data/Country-Code.xlsx")
    get_restaurant_data("data/restaurant_data.json", country_codes, "output/restaurant_data.csv")
from events_extractor import get_restaurant_events
from restaurant_extractor import get_restaurant_data
from analyse_ratings import analyse_ratings


if __name__ == "__main__":

    get_restaurant_data("../data/restaurant_data.json", "../data/Country-Code.xlsx", "../output/restaurant_details.csv")
    get_restaurant_events("../data/restaurant_data.json", "../output/restaurant_events.csv")
    analyse_ratings("../data/restaurant_data.json")
from restaurant.events_extractor import get_restaurant_events
from restaurant.restaurant_extractor import get_restaurant_data
from restaurant.analyse_ratings import analyse_ratings

from carpark.carpark_api import fetch_realtime_availability
from carpark.carpark_load_csv import load_carpark_csv
from carpark.carpark_processing import merge_carpark_data
from carpark.carpark_cli import create_parser, query_by_carpark_number, query_by_address, generate_carpark_report

if __name__ == "__main__":
    #case study 1
    get_restaurant_data("../data/restaurant_data.json", "../data/Country-Code.xlsx", "../output/restaurant_details.csv")
    get_restaurant_events("../data/restaurant_data.json", "../output/restaurant_events.csv")
    analyse_ratings("../data/restaurant_data.json")
    print("----------Restaurant data extraction completed successfully----------\n\n")

    #case study 2
    csv_data = load_carpark_csv("../data/HDBCarparkInformation.csv")
    # Fetch real-time data
    api_data = fetch_realtime_availability("https://api.data.gov.sg/v1/transport/carpark-availability")
    if csv_data is None:
        exit(1)
    if api_data is None:
        exit(1)
    # Merge data and clean it
    merged_data = merge_carpark_data(csv_data, api_data)
    
    # Setup Parser
    parser = create_parser()
    args = parser.parse_args()

    # Handle querying logic
    if args.carpark_number:
        result = query_by_carpark_number(args.carpark_number, merged_data)
        if not result.empty:
            print(generate_carpark_report(result))
        else:
            print(f"No car park found with carpark number {args.carpark_number}")
    
    elif args.address:
        result = query_by_address(args.address, merged_data)
        if not result.empty:
            print(generate_carpark_report(result))
        else:
            print(f"No car park found for address {args.address}")
    


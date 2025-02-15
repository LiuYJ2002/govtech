import argparse
import pandas as pd


def create_cli():
    parser = argparse.ArgumentParser(description="Car Park Availability")
    
    # Add arguments for querying by carpark number and searching by address
    parser.add_argument("--carpark_number", help="Carpark number to query")
    parser.add_argument("--address", help="Address to search by")
    parser.add_argument("--view", help="View last update time")
    
    return parser


def query_by_carpark_number(carpark_number, df):
    """Queries the car park data by carpark number."""
    result = df[df['car_park_no'] == carpark_number]
    return result


def query_by_address(address, df):
    """Searches for car parks by address."""
    result = df[df['address'].str.contains(address, case=False, na=False)]
    return result


def generate_carpark_report(df):
    """Generates a comprehensive report of the car park details."""
    report = ""
    for _, row in df.iterrows():
        if pd.isna(row.get('carpark_info', [])):
            capacity = 'NA'
            available = 'NA'
        else:
            capacity = row.get('carpark_info', [])[0].get('total_lots', 'NA')
            available = row.get('carpark_info', [])[0].get('lots_available', 'NA')
        last_updated = row.get('update_datetime', 'NA')
        if pd.isna(last_updated):
            last_updated = 'NA'
        report += f"Carpark Number: { row.get('car_park_no', 'NA')}\n"
        report += f"Address: {row.get('address', 'NA')}\n"
        report += f"Capacity: {capacity}\n"
        report += f"Available: {available}\n"
        report += f"Short term parking hours: {row.get('short_term_parking', 'NA')}\n"
        report += f"Free parking hours: {row.get('free_parking', 'NA')}\n"
        report += f"Night parking: {row.get('night_parking', 'NA')}\n"
        report += f"Coordinates: {row.get('x_coord', 'NA')}, {row.get('y_coord', 'NA')}\n"
        report += f"Last updated: {last_updated}\n\n"
    return report

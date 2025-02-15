import argparse
import pandas as pd


def create_parser():
    """
    Creates the command-line interface (CLI) parser for car park availability queries.

    Returns:
    argparse.ArgumentParser: The CLI parser with added arguments for carpark number and address.
    """
    parser = argparse.ArgumentParser(description="Car Park Availability")
    parser.add_argument("--carpark_number", help="Carpark number to query")
    parser.add_argument("--address", help="Address to search by")
    
    return parser


def query_by_carpark_number(carpark_number, df):
    """
    Queries the car park data by carpark number.

    Parameters:
    carpark_number (str): The car park number to search for.
    df (pd.DataFrame): The DataFrame containing car park data.

    Returns:
    pd.DataFrame: The rows from the DataFrame that match the given carpark number.
    """
    result = df[df['car_park_no'] == carpark_number]
    return result


def query_by_address(address, df):
    """
    Searches for car parks by address.

    Parameters:
    address (str): The address to search for.
    df (pd.DataFrame): The DataFrame containing car park data.

    Returns:
    pd.DataFrame: The rows from the DataFrame that match the given address.
    """
    result = df[df['address'].str.contains(address, case=False, na=False)]
    return result


def generate_carpark_report(df):
    """
    Generates a report of the car park details.

    Parameters:
    df (pd.DataFrame): The DataFrame containing car park data.

    Returns:
    str: A formatted string containing the report of wanted car park details.
    """
    report = ""
    for _, row in df.iterrows():
        #check if the carpark_info is empty
        if pd.isna(row.get('carpark_info', [])):
            capacity = 'NA'
            available = 'NA'
        else:
            capacity = row.get('carpark_info', [])[0].get('total_lots', 'NA')
            available = row.get('carpark_info', [])[0].get('lots_available', 'NA')
        last_updated = row.get('update_datetime', 'NA')
        #check if the last_updated is empty
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

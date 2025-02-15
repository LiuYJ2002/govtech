import pandas as pd
import os

def load_carpark_csv(file_path):
    """
    Loads the static car park details from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file containing car park details.

    Returns:
    pd.DataFrame: A DataFrame containing the car park details if the file is found, 
                  or raises a FileNotFoundError if the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

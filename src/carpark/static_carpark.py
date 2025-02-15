import pandas as pd

def load_carpark_csv(file_path):
    """Loads the static car park details from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

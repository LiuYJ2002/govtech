import pandas as pd
import os


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
    # Extract ratings text and score for each restaurant
    for restaurants in df["restaurants"]:
        for restaurant in restaurants:
            rating = restaurant["restaurant"]["user_rating"]["aggregate_rating"]
            rating_text = restaurant["restaurant"]["user_rating"]["rating_text"]
            rating = float(rating)
            ratings_data.append((rating, rating_text))

    df = pd.DataFrame(ratings_data, columns=["Rating", "Rating Text"])
    rating_summary = df.groupby("Rating Text")["Rating"].agg(["min", "max", "mean", "count"]).sort_index()
    print(rating_summary)
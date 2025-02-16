import unittest
import pandas as pd
from unittest.mock import patch
from src.restaurant.restaurant_extractor import get_country_code, get_restaurant_data

class TestRestaurantData(unittest.TestCase):
    
    @patch("pandas.read_excel")
    def test_get_country_code_valid_file(self, mock_read_excel):
        # Mock Excel data
        mock_df = pd.DataFrame({"Country Code": [1, 14], "Country": ["India", "Australia"]})
        mock_read_excel.return_value = mock_df
        
        expected_output = {1: "India", 14: "Australia"}
        result = get_country_code("tests/mock_file.xlxs")
        
        #assert that output is correct
        self.assertEqual(result, expected_output)
    
    def test_get_country_code_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            get_country_code("non_existent_file.xlsx")
    
    @patch("pandas.read_json")
    @patch("src.restaurant.restaurant_extractor.get_country_code")
    @patch("pandas.DataFrame.to_csv")
    def test_get_restaurant_data_match(self, mock_to_csv, mock_get_country_code, mock_read_json):
        # Mock country codes
        mock_get_country_code.return_value = {1: "USA", 2: "India"}
        
        # Mock JSON data
        mock_json_data = [{
            "restaurants": [
                {"restaurant": {
                    "R": {"res_id": 1},
                    "name": "Mock Restaurant",
                    "location": {"country_id": 1, "city": "New York"},
                    "user_rating": {"votes": 100, "aggregate_rating": "4.5"},
                    "cuisines": "Chinese",
                    "zomato_events": [
                        {"event": {"start_date": "2023-01-01"}}
                    ]
                }},
                {"restaurant": {
                    "R": {"res_id": 2},
                    "name": "Mock2 Restaurant",
                    "location": {"country_id": 2, "city": "Mumbai"},
                    "user_rating": {"votes": 1000, "aggregate_rating": "4.4"},
                    "cuisines": "Indian",
                    "zomato_events": [
                        {"event": {"start_date": "2023-05-01"}}
                    ]
                }},
                {"restaurant": {
                    "R": {"res_id": 100},
                    "name": "Mock-not-match Restaurant",
                    "location": {"country_id": 100, "city": "Singapore"},
                    "user_rating": {"votes": 500, "aggregate_rating": "1.5"},
                    "cuisines": "Italian",
                    "zomato_events": [
                        {"event": {"start_date": "2023-02-01"}}
                    ]
                }}
            ]
        }]
        
        mock_read_json.return_value = pd.DataFrame(mock_json_data)
        
        output_file = "mock_output.csv"
        restaurant_df = get_restaurant_data("tests/mock_data.json", "tests/mock_file.xlsx", output_file)
        
        # Ensure thaty no file is written to output
        mock_to_csv.return_value = None
        mock_to_csv.assert_called_once()
        # 2 restaurant should be processed
        self.assertEqual(restaurant_df.shape[0], 2)  

        # Assert that the DataFrame contains the correct data for the first restaurant
        self.assertEqual(restaurant_df.iloc[0]["Restaurant Name"], "Mock Restaurant")
        self.assertEqual(restaurant_df.iloc[0]["Country"], "USA")
        self.assertEqual(restaurant_df.iloc[0]["City"], "New York")
        self.assertEqual(restaurant_df.iloc[0]["User Rating Votes"], 100)
        self.assertEqual(restaurant_df.iloc[0]["User Aggregate Rating"], "4.5")
        self.assertEqual(restaurant_df.iloc[0]["Cuisines"], "Chinese")
        self.assertEqual(restaurant_df.iloc[0]["Event Date"], ["2023-01-01"])

        # Check for the second restaurant in the DataFrame
        self.assertEqual(restaurant_df.iloc[1]["Restaurant Name"], "Mock2 Restaurant")
        self.assertEqual(restaurant_df.iloc[1]["Country"], "India")
        self.assertEqual(restaurant_df.iloc[1]["City"], "Mumbai")
        self.assertEqual(restaurant_df.iloc[1]["User Rating Votes"], 1000)
        self.assertEqual(restaurant_df.iloc[1]["User Aggregate Rating"], "4.4")
        self.assertEqual(restaurant_df.iloc[1]["Cuisines"], "Indian")
        self.assertEqual(restaurant_df.iloc[1]["Event Date"], ["2023-05-01"])  
    
    
    @patch("pandas.read_json")
    @patch("src.restaurant.restaurant_extractor.get_country_code")
    @patch("pandas.DataFrame.to_csv")
    def test_get_restaurant_data_no_match(self, mock_to_csv, mock_get_country_code, mock_read_json):
        # Mock country codes
        mock_get_country_code.return_value = {1: "USA", 2: "India"}
        
        # Mock JSON data
        mock_json_data = [{
            "restaurants": [
                {"restaurant": {
                    "R": {"res_id": 1},
                    "name": "Mock Restaurant",
                    "location": {"country_id": 5, "city": "Singapore"},
                    "user_rating": {"votes": 100, "aggregate_rating": "4.5"},
                    "cuisines": "Chinese",
                    "zomato_events": [
                        {"event": {"start_date": "2023-01-01"}}
                    ]
                }}
            ]
        }]
        
        mock_read_json.return_value = pd.DataFrame(mock_json_data)
        
        output_file = "mock_output.csv"
        restaurant_df = get_restaurant_data("tests/mock_data.json", "tests/mock_file.xlsx", output_file)
        
        # Ensure thaty no file is written to output
        mock_to_csv.return_value = None
        mock_to_csv.assert_called_once()

        # No restaurant should be processed
        self.assertEqual(restaurant_df.shape[0], 0)  
    
    def test_get_restaurant_data_json_not_found(self):
        with self.assertRaises(FileNotFoundError):
            get_restaurant_data("non_existent.json", "mock_countries.xlsx", "output.csv")

if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch
import pandas as pd
from src.restaurant.events_extractor import is_event_in_april_2019, get_restaurant_events

class TestRestaurantEvents(unittest.TestCase):

    def test_is_event_in_april_2019_valid(self):
        # Test case where the event overlaps with April 2019
        start_date = "2019-03-10"
        end_date = "2019-05-15"
        self.assertTrue(is_event_in_april_2019(start_date, end_date))

    def test_is_event_in_april_2019_not_overlapping(self):
        # Test case where the event does not overlap with April 2019
        start_date = "2019-03-25"
        end_date = "2019-03-30"
        self.assertFalse(is_event_in_april_2019(start_date, end_date))

    def test_is_event_in_april_2019_edge_case_start(self):
        # Test case where the event starts in April
        start_date = "2019-04-01"
        end_date = "2019-04-10"
        self.assertTrue(is_event_in_april_2019(start_date, end_date))

    def test_is_event_in_april_2019_edge_case_end(self):
        # Test case where the event ends in April
        start_date = "2019-04-25"
        end_date = "2019-04-30"
        self.assertTrue(is_event_in_april_2019(start_date, end_date))

    def test_is_event_in_april_2019_edge_case_no_overlap(self):
        # Test case where the event does not overlap with April
        start_date = "2019-05-01"
        end_date = "2019-05-05"
        self.assertFalse(is_event_in_april_2019(start_date, end_date))

    @patch("pandas.read_json")
    @patch("pandas.DataFrame.to_csv")
    def test_get_restaurant_events(self, mock_to_csv, mock_read_json):
        # Mock JSON data
        mock_json_data = [{
            "restaurants": [
                {"restaurant": {
                    "R": {"res_id": 1},
                    "name": "Mock Restaurant",
                    "photos_url": "http://example.com/photo.jpg",
                    "zomato_events": [
                        {"event": {
                            "event_id": "123",
                            "title": "Event in April",
                            "start_date": "2019-04-05",
                            "end_date": "2019-04-10"
                        }}
                    ]
                }},
                {"restaurant": {
                    "R": {"res_id": 2},
                    "name": "Not match Restaurant",
                    "photos_url": "http://example.com/not-match-photo",
                    "zomato_events": [
                        {"event": {
                            "event_id": "1234",
                            "title": "Event in March",
                            "start_date": "2019-03-25",
                            "end_date": "2019-03-30"
                        }}
                    ]
                }},
                {"restaurant": {
                    "R": {"res_id": 3},
                    "name": "Mock second match Restaurant",
                    "photos_url": "http://example.com/mock-second-photo.jpg",
                    "zomato_events": [
                        {"event": {
                            "event_id": "12345",
                            "title": "Event in April",
                            "start_date": "2019-03-19",
                            "end_date": "2019-04-30"
                        }}
                    ]
                }}
            ]
        }]
        mock_read_json.return_value = pd.DataFrame(mock_json_data)

        output_file = "mock_output.csv"
        restaurant_df = get_restaurant_events("tests/mock_data.json", output_file)
        
        # Assert that the to_csv method was called and does not create a new file
        mock_to_csv.return_value = None
        mock_to_csv.assert_called_once()

        # Check that the DataFrame contains 2 event
        self.assertEqual(restaurant_df.shape[0], 2)
        
        # Check if the first restaurant details are correct
        self.assertEqual(restaurant_df.iloc[0]["Restaurant Id"], 1)
        self.assertEqual(restaurant_df.iloc[0]["Event Title"], "Event in April")
        self.assertEqual(restaurant_df.iloc[0]["Event Start Date"], "2019-04-05")
        self.assertEqual(restaurant_df.iloc[0]["Event End Date"], "2019-04-10")
        self.assertEqual(restaurant_df.iloc[0]["Restaurant Name"], "Mock Restaurant")  
        self.assertEqual(restaurant_df.iloc[0]["Photo URL"], "http://example.com/photo.jpg")  
        self.assertEqual(restaurant_df.iloc[0]["Event Id"], "123")  

        # Check if the second restaurant details are correct
        self.assertEqual(restaurant_df.iloc[1]["Restaurant Id"], 3)
        self.assertEqual(restaurant_df.iloc[1]["Event Title"], "Event in April")
        self.assertEqual(restaurant_df.iloc[1]["Event Start Date"], "2019-03-19")
        self.assertEqual(restaurant_df.iloc[1]["Event End Date"], "2019-04-30")
        self.assertEqual(restaurant_df.iloc[1]["Restaurant Name"], "Mock second match Restaurant")  
        self.assertEqual(restaurant_df.iloc[1]["Photo URL"], "http://example.com/mock-second-photo.jpg")  
        self.assertEqual(restaurant_df.iloc[1]["Event Id"], "12345")  


    @patch("pandas.read_json")
    @patch("pandas.DataFrame.to_csv")
    def test_get_restaurant_events_no_events(self, mock_to_csv, mock_read_json):
        # Mock JSON data where there are no events in April 2019
        mock_json_data = [{
            "restaurants": [
                {"restaurant": {
                    "R": {"res_id": 1},
                    "name": "Mock Restaurant",
                    "photos_url": "http://example.com/photo",
                    "zomato_events": [
                        {"event": {
                            "event_id": "123",
                            "title": "Event in March",
                            "start_date": "2019-03-25",
                            "end_date": "2019-03-30"
                        }}
                    ]
                }}
            ]
        }]
        mock_read_json.return_value = pd.DataFrame(mock_json_data)
        
        output_file = "mock_output.csv"
        restaurant_df = get_restaurant_events("tests/mock_data.json", output_file)

        # Assert that the to_csv method was called and does not create a new file
        mock_to_csv.return_value = None
        mock_to_csv.assert_called_once()

        # Check that the DataFrame contains no event
        self.assertEqual(restaurant_df.shape[0], 0)

if __name__ == "__main__":
    unittest.main()

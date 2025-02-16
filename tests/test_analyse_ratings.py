import unittest
from unittest.mock import patch
import pandas as pd
from io import StringIO
from src.restaurant.analyse_ratings import analyse_ratings


class TestAnalyseRatings(unittest.TestCase):
    """Test analyse_ratings function provides the correct summary table"""
    @patch("os.path.exists")
    @patch("pandas.read_json")
    @patch("sys.stdout", new_callable=StringIO)
    def test_analyse_ratings(self, mock_stdout, mock_read_json, mock_exists):
        # Mock os.path.exists to return True as if the file exists
        mock_exists.return_value = True
        
        # Mock JSON data 
        mock_json_data = [{
            "restaurants": [
                {"restaurant": {
                    "user_rating": {"aggregate_rating": "4.5", "rating_text": "Excellent"}
                }},
                {"restaurant": {
                    "user_rating": {"aggregate_rating": "3.0", "rating_text": "Good"}
                }},
                {"restaurant": {
                    "user_rating": {"aggregate_rating": "2.0", "rating_text": "Average"}
                }},
                {"restaurant": {
                    "user_rating": {"aggregate_rating": "4.0", "rating_text": "Good"}
                }}
            ]
        }]
        
        # Mock pd.read_json to return the mock data
        mock_read_json.return_value = pd.DataFrame(mock_json_data)
        
        analyse_ratings("mock_data.json")
        
        printed_output = mock_stdout.getvalue()
        
        expected_keys = ["Good", "Excellent", "Average", "min", "max", "mean", "count"]
        for key in expected_keys:
            self.assertIn(key, printed_output)
        
        # Check if summary values are correct
        self.assertRegex(printed_output, r"Good\s+3\.0\s+4\.0\s+3\.5\s+2")
        self.assertRegex(printed_output, r"Excellent\s+4\.5\s+4\.5\s+4\.5\s+1")
        self.assertRegex(printed_output, r"Average\s+2\.0\s+2\.0\s+2\.0\s+1")

    def test_file_not_found(self):
        """Test FileNotFoundError is raised when file does not exist"""
        with self.assertRaises(FileNotFoundError):
            analyse_ratings("non_existing_file.json")

if __name__ == "__main__":
    unittest.main()

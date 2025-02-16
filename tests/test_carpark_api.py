import unittest
from unittest.mock import patch, MagicMock
import requests
from src.carpark.carpark_api import fetch_realtime_availability  

class TestFetchRealtimeAvailability(unittest.TestCase):

    @patch('requests.get') 
    def test_fetch_realtime_availability_success(self, mock_get):
        """Test a successful API call"""
        # Mock the response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "data": "some_data"}  
        mock_get.return_value = mock_response
        
        result = fetch_realtime_availability('http://api.example.com')
        
        # Check if the result is expected
        self.assertEqual(result, {"status": "success", "data": "some_data"})
        
        # Ensure that requests.get was called with the correct URL
        mock_get.assert_called_once_with('http://api.example.com')

    @patch("requests.get")
    def test_fetch_http_error(self, mock_get):
        """Test API call failing due to HTTP error"""
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")
        result = fetch_realtime_availability('http://api.example.com')
        self.assertIsNone(result)

    @patch("requests.get")
    def test_fetch_connection_error(self, mock_get):
        """Test API call failing due to a network issue"""
        mock_get.side_effect = requests.exceptions.ConnectionError("No Internet Connection")
        result = fetch_realtime_availability('http://api.example.com')
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

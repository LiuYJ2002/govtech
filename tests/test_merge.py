import unittest
import pandas as pd
from src.carpark.carpark_processing import merge_carpark_data  

class TestMergeCarparkData(unittest.TestCase):

    def test_merge_carpark_data(self):
        # fake csv data
        csv_data = pd.DataFrame({
            "car_park_no": ["A01", "B02", "C03"],
            "location": ["Location1", "Location2", "Location3"],
            "x_coord": [1.123, 2.345, 3.456],
            "y_coord": [4.567, 5.678, 6.789]
        })

        # fake api data
        api_data = {
            "items": [
                {
                    "carpark_data": [
                        {"carpark_number": "A01", "carpark_info": "Info1", "update_datetime": "2025-02-16 12:00"},
                        {"carpark_number": "B02", "carpark_info": "Info2", "update_datetime": "2025-02-16 12:05"}
                    ]
                }
            ]
        }

        result = merge_carpark_data(csv_data, api_data)

        expected_result = pd.DataFrame({
            "car_park_no": ["A01", "B02", "C03"],
            "location": ["Location1", "Location2", "Location3"],
            "x_coord": [1.123, 2.345, 3.456],
            "y_coord": [4.567, 5.678, 6.789],
            "carpark_info": ["Info1", "Info2", pd.NA],
            "update_datetime": ["2025-02-16 12:00", "2025-02-16 12:05", pd.NA]
        })

        # Test that the result is the same as the expected result
        pd.testing.assert_frame_equal(result, expected_result)

if __name__ == '__main__':
    unittest.main()

import unittest
import pandas as pd
from src.carpark.carpark_cli import create_parser, query_by_carpark_number, query_by_address, generate_carpark_report  


class TestCarParkFunctions(unittest.TestCase):

    def setUp(self):
        # Sample data to use in tests
        self.sample_data = pd.DataFrame({
            'car_park_no': ['A01', 'B02', 'C03'],
            'address': ['Location1', 'Location2', 'Location3'],
            'carpark_info': [[{'total_lots': 100, 'lots_available': 10}], [{'total_lots': 200, 'lots_available': 50}], [pd.NA]],
            'update_datetime': ['2025-02-16 12:00', '2025-02-16 12:05', pd.NA],
            'short_term_parking': ['9am - 6pm', '9am - 5pm', 'NO'],
            'free_parking': ['SUN & PH FR 7AM-10.30PM', 'NO', 'NO'],
            'night_parking': ['Yes', 'No', 'Yes'],
            'car_park_decks': ['1', '2', '3'],
            'gantry_height': ['1.00', '1.10', '1.20'],
            'car_park_basement': ['Y', 'N', 'Y'],
            'x_coord': [1.123, 1.456, 1.789],
            'y_coord': [2.234, 2.567, 2.890]
        })

    def test_create_parser(self):
        """Test if the parser is created correctly"""
        parser = create_parser()
        # test if it parses carpark number
        args = parser.parse_args(['--carpark_number', 'A01'])
        self.assertEqual(args.carpark_number, 'A01')
        self.assertIsNone(args.address)
        
        # test if it parses address
        args = parser.parse_args(['--address', 'Clementi'])
        self.assertEqual(args.address, 'Clementi')
        self.assertIsNone(args.carpark_number)

    def test_query_by_carpark_number(self):
        """Test if the query by carpark number works correctly"""
        result = query_by_carpark_number('A01', self.sample_data)
        self.assertEqual(result.shape[0], 1)  # Only one row should match
        self.assertEqual(result['car_park_no'].iloc[0], 'A01')

    def test_query_by_address(self):
        """Test if the query by address works correctly"""
        result = query_by_address('Location1', self.sample_data)
        self.assertEqual(result.shape[0], 1)  # Only one row should match
        self.assertEqual(result['address'].iloc[0], 'Location1')
        
        # Test insensitive case
        result = query_by_address('location1', self.sample_data)
        self.assertEqual(result.shape[0], 1)

    def test_generate_carpark_report(self):
        """Test if the carpark report is generated correctly"""
        report = generate_carpark_report(self.sample_data)
        sections = report.strip().split('\n\n')

        # Check each section for relevant columns
        for section in sections:
            self.assertIn("Carpark Number:", section)
            self.assertIn("Address:", section)
            self.assertIn("Capacity:", section)
            self.assertIn("Available:", section)
            self.assertIn("Last updated:", section)
            self.assertIn("Short term parking hours:", section)
            self.assertIn("Free parking hours:", section)
            self.assertIn("Night parking:", section)
            self.assertIn("Coordinates:", section)
            self.assertIn("Last updated:", section)

if __name__ == '__main__':
    unittest.main()

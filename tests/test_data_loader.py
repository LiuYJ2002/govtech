import unittest
from unittest.mock import patch, MagicMock
import os
from src.data_loader import load_json_data, load_excel_data


class TestDataLoader(unittest.TestCase):

    @patch('os.path.exists')
    @patch('pandas.read_json')
    def test_load_json_data_success(self, mock_read_json, mock_exists):
        """Test loading JSON data successfully"""
        mock_exists.return_value = True
        mock_read_json.return_value = MagicMock()
        result = load_json_data("data/restaurant_data.json")
        self.assertIsNotNone(result)

    @patch('os.path.exists')
    def test_load_json_data_file_not_found(self, mock_exists):
        """Test loading JSON data when file is not found"""
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            load_json_data("data/restaurant_data.json")

    @patch('os.path.exists')
    @patch('pandas.read_excel')
    def test_load_excel_data_success(self, mock_read_excel, mock_exists):
        """Test loading Excel data successfully"""
        mock_exists.return_value = True
        mock_read_excel.return_value = MagicMock()
        result = load_excel_data("data/Country-Code.xlsx")
        self.assertIsNotNone(result)

    @patch('os.path.exists')
    def test_load_excel_data_file_not_found(self, mock_exists):
        """Test loading Excel data when file is not found"""
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            load_excel_data("data/Country-Code.xlsx")

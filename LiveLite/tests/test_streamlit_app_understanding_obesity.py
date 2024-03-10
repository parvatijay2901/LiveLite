import unittest
from pathlib import Path
from unittest import mock
import streamlit as st
import LiveLite
import pandas as pd

THIS_DIR = Path(__file__).parent

class TestComprehensiveGuide(unittest.TestCase):
    def setUp(self):
        """
        Sets up the test by loading in the data.
        """
        nhanes_path = THIS_DIR.parent / 'data/input_files/NHANES_Background.csv'
        ihme_path = THIS_DIR.parent / 'data/input_files/IHME/number-of-deaths-by-risk-factor.csv'
        self.nhanes_data = pd.read_csv(nhanes_path)
        self.ihme_data = pd.read_csv(ihme_path)

    @mock.patch("streamlit.button")
    @mock.patch("streamlit.switch_page")
    def test_navigation_not_called(self, mock_switch_page, mock_button):
        with mock.patch('streamlit.session_state', {'data_nhanes':self.nhanes_data, 'data_ihme':self.ihme_data}):
            mock_button.return_value = False
            LiveLite.pagea()
            mock_switch_page.assert_not_called()

    @mock.patch("streamlit.button")
    @mock.patch("streamlit.switch_page")
    def test_navigation_to_obesity_assessment(self, mock_switch_page, mock_button):
        with mock.patch('streamlit.session_state', {'data_nhanes':self.nhanes_data, 'data_ihme':self.ihme_data}):
            mock_button.return_value = True
            LiveLite.pagea()
            mock_switch_page.assert_called_with("pages/b_obesity_assessment.py")

    @mock.patch('os.path.exists')
    @mock.patch('streamlit.button')
    def test_navigation_invalid_path(self, mock_button, mock_path):
        """Testing navigation to other pages - with invalid path"""
        with mock.patch('streamlit.session_state', {'data_nhanes':self.nhanes_data, 'data_ihme':self.ihme_data}):
            mock_button.return_value = True
            mock_path.return_value = False
            with self.assertRaises(FileNotFoundError):
                LiveLite.pagea()

if __name__ == "__main__":
    unittest.main()
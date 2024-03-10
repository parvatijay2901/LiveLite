import unittest
from unittest import mock
import LiveLite

class TestComprehensiveGuide(unittest.TestCase):
    def setUp(self):
        """Mock the necessary dependencies."""
        self.mock_user_inputs = {"age": 37,
                                "sex": "Male",
                                "height": 100,
                                "weight": 100,
                                "ethnicity": "Non-Hispanic White",
                                "activity_level": "Moderately Active",
                                "smoke_cig": "No",
                                "mental_health": "Occasionally these days",
                                "sleep_hrs": 1.0,
                                "health_condition": "Fair",
                                "diet_condition": "Poor",
                                "poor_appetite_overeating": "Nearly every day these days"}

        self.mock_session_state = {"user_inputs": self.mock_user_inputs}

    @mock.patch("streamlit.button")
    @mock.patch("streamlit.switch_page")
    @mock.patch('streamlit.session_state')
    @mock.patch('LiveLite.project_integration.handle_user_input.user_input_mapping.convert_age', return_value=37)
    @mock.patch('LiveLite.project_integration.handle_user_input.user_input_mapping.convert_sex', return_value=1)
    @mock.patch('LiveLite.project_integration.handle_user_input.user_input_mapping.convert_ethnicity', return_value=3)
    @mock.patch('LiveLite.project_integration.handle_user_input.user_input_mapping.convert_activity_level', return_value=3)
    @mock.patch('LiveLite.project_integration.handle_user_input.user_input_mapping.convert_mental_health', return_value=1)
    @mock.patch('LiveLite.project_integration.handle_user_input.user_input_mapping.convert_sleep_hours', return_value=2)
    @mock.patch('LiveLite.project_integration.handle_user_input.user_input_mapping.convert_health_condition', return_value=4)
    def test_navigation_to_personalized_recommendations(self, mock_health_condition, mock_sleep_hours, mock_mental_health, mock_activity_level, mock_ethnicity, mock_sex, mock_age, mock_session_state, mock_switch_page, mock_button):
        mock_session_state.return_value = self.mock_session_state
        mock_button.return_value = True
        LiveLite.pagec()
        mock_switch_page.assert_called_with("pages/d_personalized_recommendations.py")

    @mock.patch('os.path.exists')
    @mock.patch('streamlit.button')
    def test_navigation_invalid_path(self, mock_button, mock_path):
        """Testing navigation to other pages - with invalid path"""
        mock_button.return_value = True
        mock_path.return_value = False
        with self.assertRaises(AssertionError):
            LiveLite.pagec()

if __name__ == "__main__":
    unittest.main()

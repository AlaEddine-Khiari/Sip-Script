import unittest
from unittest.mock import patch, mock_open
from script import fetch_internals_user, update_sip_conf
import os

class TestScript(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_fetch_internals_user(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = ('test_user', 'test_password')

        result = fetch_internals_user()

        self.assertEqual(result, ('test_user', 'test_password'))

    @patch('builtins.open', create=True)
    @patch('builtins.print')
    def test_update_sip_conf(self, mock_print, mock_open):
        # Mock the open function to return a mock file
        mock_open.side_effect = [
            FileNotFoundError,  # Simulate file not found error
            mock_open(),        # Simulate successful write
        ]

        # Mock the fetch_internals_user function
        with patch('script.fetch_internals_user', return_value=('new_user', 'new_password')):
            update_sip_conf('/Test/sip.conf')  # Test file not found scenario
            update_sip_conf('/Test/sip.conf')     # Test successful write scenario

        mock_print.assert_called_with("sip.conf updated successfully")

if __name__ == '__main__':
    unittest.main()

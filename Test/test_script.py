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

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_update_sip_conf(self, mock_print, mock_open):
        # Mock to simulate reading file content
        mock_open_read = mock_open(read_data="[internals]\n[existing_user]\n").return_value
        
        # Mock to assert file opening behavior in update_sip_conf
        mock_open_write = mock_open()
        
        mock_open.side_effect = [mock_open_read, FileNotFoundError]
        
        with patch('builtins.open', mock_open_write):
            update_sip_conf('/Test/sip.conf')  # Assuming the file is in the Test directory

        # Check if the file is opened with the correct mode ('w' for write)
        mock_open_write.assert_called_once_with('/Test/sip.conf', 'w')

        # Check if the required lines are added to the file
        mock_open_write.return_value.write.assert_any_call("[internals]\n")
        mock_open_write.return_value.write.assert_any_call("[existing_user]\n")

        # Check if the success message is printed
        mock_print.assert_called_with("sip.conf updated successfully")

if __name__ == '__main__':
    unittest.main()

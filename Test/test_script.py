import unittest
from unittest.mock import patch, mock_open
from script import fetch_internals_user, update_sip_conf

class TestScript(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_update_sip_conf(self, mock_connect):
        # Mock the fetch_internals_user function to return a valid result
        mock_connect.return_value.cursor.return_value.fetchone.return_value = ('test_user', 'test_password')
        
        # Mock the open function to return a mock file object
        with patch('builtins.open', mock_open()) as mock_open_func:
            update_sip_conf('/Test/sip.conf')  # Assuming the file is in the Test directory
            
            # Assert that the open function was called with the correct mode ('w')
            mock_open_func.assert_called_once_with('/Test/sip.conf', 'w')

if __name__ == '__main__':
    unittest.main()

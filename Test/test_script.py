import unittest
from unittest.mock import patch
from script import update_sip_conf

class TestScript(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_update_sip_conf(self, mock_connect):
        # Mock the fetch_internals_user function to return a valid result
        mock_connect.return_value.cursor.return_value.fetchone.return_value = ('test_user', 'test_password')
        
        # Call the update_sip_conf function and ensure it runs without raising an exception
        try:
            update_sip_conf('/Test/sip.conf')  # Assuming the file is in the Test directory
        except Exception as e:
            self.fail(f"Function raised exception: {e}")

if __name__ == '__main__':
    unittest.main()

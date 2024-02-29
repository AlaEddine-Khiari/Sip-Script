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
            update_sip_conf('/Test/sip.conf') 
if __name__ == '__main__':
    unittest.main()

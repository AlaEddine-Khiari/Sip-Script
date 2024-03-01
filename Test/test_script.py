import unittest
from unittest.mock import patch, mock_open
from app import update_sip_conf, fetch_internals_user

class TestApp(unittest.TestCase):

    @patch('psycopg2.connect')
    @patch('builtins.open', mock_open(read_data='XXXX\n; Configuration for internal extensions\n'))
    def test_update_sip_conf(self, mock_connect):
        # Mock the fetch_internals_user function to return a valid result
        fetch_internals_user.return_value = [('test_user', 'test_password')]

        # Mock the database connection
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [('test_user', 'test_password')]

        # Call the function to be tested
        update_sip_conf('/app/sip.conf')

        # Assert that the database connection is called with the correct parameters
        mock_connect.assert_called_once_with(
            dbname='test_db',
            user='test_user',
            password='test_password',
            host='test_host',
            port='5432'
        )

if __name__ == '__main__':
    unittest.main()

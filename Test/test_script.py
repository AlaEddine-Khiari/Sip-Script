import unittest
from unittest.mock import patch, mock_open
from app import update_sip_conf, fetch_internals_user, update_voicemail_conf

class TestApp(unittest.TestCase):

    @patch('psycopg2.connect')
    @patch('builtins.open', mock_open(read_data='XXXX\n; Configuration for internal extensions\n'))
    def test_app (self, mock_connect):
        # Mock the fetch_internals_user function to return a valid result
        fetch_internals_user.return_value = [('test_user', 'test_password')]

        # Mock the database connection
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [('test_user', 'test_password')]

        # Call the function to be tested
        update_sip_conf('/app/sip.conf')
        update_voicemail_conf('/app/voicemail.conf')
if __name__ == '__main__':
    unittest.main()

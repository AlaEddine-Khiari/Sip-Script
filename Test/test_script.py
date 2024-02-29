import unittest
from unittest.mock import patch
from script import fetch_internals_user, update_sip_conf

class TestScript(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_fetch_internals_user(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = ('test_user', 'test_password')

        result = fetch_internals_user()

        self.assertEqual(result, ('test_user', 'test_password'))

    @patch('builtins.open')
    @patch('builtins.print')
    def test_update_sip_conf(self, mock_print, mock_open):
        sip_conf_path = 'sip.conf'

        update_sip_conf(sip_conf_path)

        mock_print.assert_called_with("sip.conf updated successfully")

if __name__ == '__main__':
    unittest.main()

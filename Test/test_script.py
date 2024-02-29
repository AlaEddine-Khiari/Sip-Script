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

    @patch('builtins.open', create=True)
    @patch('builtins.print')
    def test_update_sip_conf(self, mock_print, mock_open):
        mock_open.side_effect = [
            ['[internals]\n', '[existing_user]\n'],
            None  # Simulate successful write
        ]

        update_sip_conf()

        mock_print.assert_called_with("sip.conf updated successfully")

if __name__ == '__main__':
    unittest.main()

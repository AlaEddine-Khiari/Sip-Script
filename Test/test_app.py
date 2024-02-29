import unittest
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch('script.update_sip_conf')
    def test_apply_changes(self, mock_update_sip_conf):
        response = self.client.get('/apply')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Changes applied successfully', response.data)
        mock_update_sip_conf.assert_called_once()

if __name__ == '__main__':
    unittest.main()

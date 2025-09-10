import unittest
from application import app  # Make sure app.py file is named `app.py`
import json

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Setup test client
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'RECAPI_MOVIEFUSE', response.data)

    def test_recommendations_with_valid_title(self):
        # Use a known movie title from your dataset
        test_title = 'The Matrix'

        response = self.app.post('/', data={'title': test_title})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recommendations for', response.data)
        self.assertIn(b'overview', response.data)

    def test_invalid_title(self):
        response = self.app.post('/', data={'title': 'nonexistentmovietitle'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Title not found in dataset', response.data)

if __name__ == '__main__':
    unittest.main()

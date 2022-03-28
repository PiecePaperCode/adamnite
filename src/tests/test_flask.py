import unittest

from src.main import app


class Flask(unittest.TestCase):
    def test_flask(self):
        client = app.test_client()
        response = client.get('/').json
        self.assertEqual(response['name'], 'Adamnite')

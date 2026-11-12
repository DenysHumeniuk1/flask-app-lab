import unittest
from app import create_app

class MainTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_resume(self):
        self.assertEqual(self.client.get('/resume').status_code, 200)

    def test_contacts_get_post(self):
        self.assertEqual(self.client.get('/contacts').status_code, 200)
        self.assertEqual(self.client.post('/contacts', data={'name':'Test'}).status_code, 200)

    def test_homepage(self):
        self.assertEqual(self.client.get('/homepage').status_code, 200)

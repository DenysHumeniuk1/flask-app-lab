import unittest
from app import app

class ProductBlueprintTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_product_list(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        for name in [b'Laptop', b'Phone', b'PC']:
            self.assertIn(name, response.data)

    def test_product_detail(self):
        response = self.client.get('/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Laptop', response.data)
        self.assertIn(b'1200', response.data)

    def test_missing_product(self):
        self.assertEqual(self.client.get('/products/999').status_code, 404)

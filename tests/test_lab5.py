import io
import os
import unittest
from app import app
from app.products.views import products_table

class Lab5Tests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.client = app.test_client()
        self.original_products = products_table.all()
        products_table.truncate()

    def tearDown(self):
        products_table.truncate()
        if self.original_products:
            products_table.insert_multiple(self.original_products)

    def product_data(self, **changes):
        data = {
            "name": "Test product", "content": "Test description",
            "price": "12.50", "category": "electronics", "quantity": "4"
        }
        data.update(changes)
        return data

    def test_contact_get_and_post_prg(self):
        self.assertEqual(self.client.get("/contact").status_code, 200)
        response = self.client.post("/contact", data={
            "name": "Denys", "email": "denys@example.com",
            "subject": "question", "message": "Hello there"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/contact")

    def test_contact_validation(self):
        response = self.client.post("/contact", data={"name": "abc", "email": "bad", "phone": "123", "subject": "general", "message": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Введіть коректну електронну адресу.".encode(), response.data)

    def test_create_and_read_product(self):
        response = self.client.post("/product/add", data=self.product_data(), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test product", response.data)
        self.assertEqual(len(products_table.all()), 1)
        product_id = products_table.all()[0]["id"]
        self.assertEqual(self.client.get(f"/product/{product_id}").status_code, 200)

    def test_update_product_preserves_metadata(self):
        self.client.post("/product/add", data=self.product_data())
        product = products_table.all()[0]
        response = self.client.post(f"/product/{product['id']}/edit", data=self.product_data(name="Updated product"))
        self.assertEqual(response.status_code, 302)
        updated = products_table.all()[0]
        self.assertEqual(updated["name"], "Updated product")
        self.assertEqual(updated["id"], product["id"])
        self.assertEqual(updated["created_at"], product["created_at"])

    def test_delete_product(self):
        self.client.post("/product/add", data=self.product_data())
        product_id = products_table.all()[0]["id"]
        self.assertEqual(self.client.post(f"/product/{product_id}/delete").status_code, 302)
        self.assertEqual(products_table.all(), [])

    def test_validation_rejects_bad_values(self):
        response = self.client.post("/product/add", data=self.product_data(name="ab", price="-1", quantity="-2"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products_table.all(), [])

    def test_missing_product(self):
        self.assertEqual(self.client.get("/product/999").status_code, 404)

if __name__ == "__main__":
    unittest.main()

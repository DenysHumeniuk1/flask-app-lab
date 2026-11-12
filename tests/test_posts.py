import unittest
from datetime import datetime
from app import create_app
from app.extensions import db
from app.posts.models import Post

class PostCRUDTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_post(self, **overrides):
        data = {
            "title": "Test post",
            "content": "This is a test post content.",
            "category": "news",
            "enabled": "y",
            "publish_date": "2026-11-11T12:00",
        }
        data.update(overrides)
        return self.client.post("/post/create", data=data, follow_redirects=True)

    def test_create_post(self):
        response = self.create_post()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test post", response.data)
        with self.app.app_context():
            post = db.session.scalar(db.select(Post))
            self.assertIsNotNone(post)
            self.assertEqual(post.author, "Anonymous")

    def test_list_posts(self):
        self.create_post()
        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test post", response.data)

    def test_view_post_detail(self):
        self.create_post()
        with self.app.app_context():
            post_id = db.session.scalar(db.select(Post.id))
        response = self.client.get(f"/post/{post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This is a test post content.", response.data)

    def test_update_post(self):
        self.create_post()
        with self.app.app_context():
            post_id = db.session.scalar(db.select(Post.id))
        response = self.client.post(
            f"/post/{post_id}/update",
            data={
                "title": "Updated post",
                "content": "Updated content.",
                "category": "tech",
                "enabled": "y",
                "publish_date": "2026-11-11T13:00",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Updated post", response.data)

    def test_delete_post(self):
        self.create_post()
        with self.app.app_context():
            post_id = db.session.scalar(db.select(Post.id))
        response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertIsNone(db.session.get(Post, post_id))

    def test_missing_post_returns_404(self):
        self.assertEqual(self.client.get("/post/999").status_code, 404)

    def test_invalid_post_is_not_saved(self):
        response = self.client.post("/post/create", data={"title": "", "content": ""})
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertEqual(db.session.scalar(db.select(db.func.count()).select_from(Post)), 0)

if __name__ == "__main__":
    unittest.main()

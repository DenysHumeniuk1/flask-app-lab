import unittest
from app import app

class Lab4Tests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def login(self):
        return self.client.post('/users/login', data={'username':'student','password':'lab4pass'}, follow_redirects=True)

    def test_login_invalid_and_valid(self):
        self.assertIn('Неправильний'.encode(), self.client.post('/users/login',data={'username':'student','password':'wrong'},follow_redirects=True).data)
        response=self.login()
        self.assertEqual(response.status_code,200)
        self.assertIn('student',response.get_data(as_text=True))

    def test_profile_requires_login(self):
        self.assertEqual(self.client.get('/users/profile').status_code,302)

    def test_logout(self):
        self.login()
        self.client.post('/users/logout')
        self.assertEqual(self.client.get('/users/profile').status_code,302)

    def test_cookie_add_delete(self):
        self.login()
        response=self.client.post('/users/cookies/add',data={'key':'example','value':'hello','max_age':'3600'})
        self.assertIn('lab4_example=hello',response.headers['Set-Cookie'])
        self.assertIn('hello',self.client.get('/users/profile').get_data(as_text=True))
        response=self.client.post('/users/cookies/delete',data={'key':'example'})
        self.assertIn('lab4_example=',response.headers['Set-Cookie'])

    def test_cookie_delete_all_and_theme(self):
        self.login()
        self.client.post('/users/cookies/add',data={'key':'a','value':'1','max_age':'60'})
        self.client.post('/users/theme/dark')
        self.assertIn('theme-dark',self.client.get('/users/profile').get_data(as_text=True))
        self.client.post('/users/cookies/delete-all')
        self.assertIn('theme-light',self.client.get('/users/profile').get_data(as_text=True))

if __name__ == '__main__': unittest.main()

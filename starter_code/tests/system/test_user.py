from section_7.starter_code.models.user import UserModel
from section_7.starter_code.tests.base_test import BaseTest

class TestUser(BaseTest):

    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/register',
                                      json={'username': 'test', 'password': '1234'})

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))

    def test_register_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register',
                                      json={'username': 'test', 'password': '1234'})
                request = client.post('/auth',
                                      json={'username': 'test', 'password': '1234'})
                self.assertEqual(request.status_code, 200)
                self.assertIsNotNone(UserModel.find_by_username('test'))

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register',
                            json={'username': 'test', 'password': '1234'})
                self.assertIsNotNone(UserModel.find_by_username('test'))
                request = client.post('/register',
                            json={'username': 'test', 'password': '1234'})
                self.assertEqual(request.status_code, 400)
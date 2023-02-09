import json

from section_7.starter_code.models.item import ItemModel
from section_7.starter_code.models.store import StoreModel
from section_7.starter_code.models.user import UserModel
from section_7.starter_code.tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                requests = client.get('/item/test')
                self.assertEqual(requests.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth = client.post('/auth',
                                      json={'username': 'test', 'password': '1234'})
                auth_token = json.loads(auth.data)['access_token']
                header = {'Authorization': f'JWT {auth_token}'}
                requests = client.get('/item/test', headers=header)
                self.assertEqual(requests.status_code, 404)
    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth = client.post('/auth',
                                   json={'username': 'test', 'password': '1234'})
                StoreModel('test').save_to_db()
                ItemModel('test', 1, 1).save_to_db()
                auth_token = json.loads(auth.data)['access_token']
                header = {'Authorization': f'JWT {auth_token}'}
                requests = client.get('/item/test', headers=header)
                self.assertEqual(requests.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1, 1).save_to_db()
                requests = client.delete('/item/test')
                self.assertEqual(requests.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                requests = client.post('/item/test',
                                       json={'name': 'test', 'store_id': 1, 'price': 1})
                self.assertEqual(requests.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test',
                                       json={'name': 'test', 'store_id': 1, 'price': 1})
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                requests = client.post('/item/test',
                                       json={'name': 'test', 'store_id': 1, 'price': 1})
                self.assertEqual(requests.status_code, 400)
                self.assertIsNotNone(StoreModel.find_by_name('test'))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1, 1).save_to_db()
                requests = client.put('/item/test',
                                       json={'store_id': 1, 'price': 2})
                self.assertEqual(requests.status_code, 200)
                self.assertIsNotNone(ItemModel.find_by_name('test').price, 2)
                self.assertDictEqual(requests.json, {'name': 'test', 'price': 2.0})

    def test_item_lits(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1, 1).save_to_db()
                requests = client.get('/items')
                self.assertEqual(requests.status_code, 200)

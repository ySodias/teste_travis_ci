from section_7.starter_code.models.item import ItemModel
from section_7.starter_code.models.store import StoreModel
from section_7.starter_code.tests.base_test import BaseTest


class StoreTest(BaseTest):

    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/test',
                                      json={'name': 'test'})
                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test',
                                      json={'name': 'test'})
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                request = client.post('/store/test',
                                      json={'name': 'test'})
                self.assertEqual(request.status_code, 400)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test',
                            json={'name': 'test'})
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                request = client.delete('/store/test')
                self.assertEqual(request.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name('test'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/test',
                                json={'name': 'test'})
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                request_get = client.get('/store/test')
                self.assertEqual(request_get.status_code, 200)
                self.assertDictEqual(request_get.json, request.json)
    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                request = client.get('/store/test')
                self.assertEqual(request.status_code, 404)
                self.assertIsNone(StoreModel.find_by_name('test'))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1, 1).save_to_db()
                request = client.get('/store/test')
                self.assertEqual(request.status_code, 200)
                self.assertListEqual(request.json['items'], [{'name': 'test', 'price': 1.0}])
    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                for index in range(0, 10):
                    client.post(f'/store/test{index}',
                                json={'name': f'test{index}'})
                request = client.get('/stores')
                self.assertEqual(request.status_code, 200)

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel(f'test').save_to_db()
                ItemModel(f'test', 1, 1).save_to_db()
                request = client.get('/stores')
                self.assertEqual(request.status_code, 200)

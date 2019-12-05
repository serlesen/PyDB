import json
import unittest

from app.controllers import app
from app.services.indexes_service import IndexesService
from app.services.file_reader import FileReader
from app.test.collections_simulator import CollectionsSimulator
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CrudControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col')

        col_meta_data = CollectionMetaData('col')

        indexes_service = IndexesService()
        file_reader = FileReader()
        docs = file_reader.find_all(col_meta_data, None)
        indexes_service.build_index(col_meta_data, docs, 'id')
	
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()
        DatabaseContext.THREADS_MANAGER_CYCLING = False

    def test_get_document(self):
        response = self.app.get('/col/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 3)

    def test_create_document(self):
        response = self.app.post('/col', data=json.dumps({'id': 1000, 'Name': 'Isaac'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['id'], 1000)
        self.assertEqual(json.loads(response.data)['name'], 'Isaac')

        response = self.app.get('/col/1000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 1000)

    def test_update_document(self):
        response = self.app.put('/col/2', data=json.dumps({'id': 2, 'first_name': 'Isaac'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 2)
        self.assertEqual(json.loads(response.data)['first_name'], 'Isaac')

        response = self.app.get('/col/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 2)
        self.assertEqual(json.loads(response.data)['first_name'], 'Isaac')

    def test_delete_document(self):
        response = self.app.delete('/col/4')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/col/4')
        self.assertEqual(response.status_code, 404)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(CrudControllerTest)
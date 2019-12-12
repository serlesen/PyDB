import json
import unittest

from app.controllers import app
from app.test.collections_simulator import CollectionsSimulator
from app.threads.threads_manager import ThreadsManager
from app.tools.database_context import DatabaseContext

class CollectionsControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if DatabaseContext.THREADS_MANAGER_CYCLING == False:
            DatabaseContext.THREADS_MANAGER_CYCLING = True
            ThreadsManager().start()

        CollectionsSimulator.build_single_col('col')

    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()
        DatabaseContext.THREADS_MANAGER_CYCLING = False

    def test_print_collection_status(self):
        response = self.app.get('/collections/col/status')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['count'], 6)

    def test_create_and_delete_collection(self):
        response = self.app.post('/collections/second-col')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/collections/second-col/status')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['count'], 0)

        response = self.app.delete('/collections/second-col')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/collections/second-col/status')
        self.assertEqual(response.status_code, 404)

    def test_create_and_delete_index(self):
        response = self.app.post('/collections/col/index/id')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/collections/col/status')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(len(response_data['indexes']), 1)
        self.assertEqual(response_data['indexes'][0]['count'], 6)
        self.assertEqual(response_data['indexes'][0]['field'], 'id')

        response = self.app.delete('/collections/col/index/id')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/collections/col/status')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(len(response_data['indexes']), 0)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(CollectionsControllerTest)

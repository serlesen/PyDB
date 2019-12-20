import json
import unittest

from app.controllers import app
from app.test.collections_simulator import CollectionsSimulator
from app.tools.database_context import DatabaseContext
from app.threads.threads_manager import ThreadsManager

class ReplicationControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if DatabaseContext.THREADS_MANAGER_CYCLING == False:
            DatabaseContext.THREADS_MANAGER_CYCLING = True
            ThreadsManager().start()

        CollectionsSimulator.build_single_col('col', ['id'])
        CollectionsSimulator.build_users_col()

    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()
        DatabaseContext.THREADS_MANAGER_CYCLING = False

    def test_sync_upsert(self):
        response = self.app.post('/admin/replicate/sync', data=json.dumps({'collection': 'col', 'doc': {'id': 3, 'first_name': 'serser'}, 'url': 'localhost:5001'}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTExNTksInN1YiI6Mn0.Uf2tyw4vPxKQ95id2iOefp4GcO3UGnYXZLPyX8NoV1U'})
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/col/3', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 3)
        self.assertEqual(json.loads(response.data)['first_name'], 'serser')

    def test_sync_delete(self):
        response = self.app.delete('/admin/replicate/sync', data=json.dumps({'collection': 'col', 'id': 5, 'url': 'localhost:5001'}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTExNTksInN1YiI6Mn0.Uf2tyw4vPxKQ95id2iOefp4GcO3UGnYXZLPyX8NoV1U'})
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/col/5', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 404)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(ReplicationControllerTest)

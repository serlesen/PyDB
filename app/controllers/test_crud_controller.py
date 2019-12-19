import json
import unittest

from app.controllers import app
from app.test.collections_simulator import CollectionsSimulator
from app.tools.database_context import DatabaseContext
from app.threads.threads_manager import ThreadsManager

class CrudControllerTest(unittest.TestCase):

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

    def test_get_document(self):
        response = self.app.get('/col/3', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 3)

    def test_create_document(self):
        response = self.app.post('/col', data=json.dumps({'id': 1000, 'Name': 'Isaac'}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['id'], 1000)
        self.assertEqual(json.loads(response.data)['name'], 'Isaac')

        response = self.app.get('/col/1000', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 1000)

    def test_update_document(self):
        response = self.app.get('/col/2', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data).keys()), 3)

        response = self.app.put('/col/2', data=json.dumps({'id': 2, 'first_name': 'Isaac'}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 2)
        self.assertEqual(json.loads(response.data)['first_name'], 'Isaac')
        self.assertEqual(len(json.loads(response.data).keys()), 2)

        response = self.app.get('/col/2', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 2)
        self.assertEqual(json.loads(response.data)['first_name'], 'Isaac')
        self.assertEqual(len(json.loads(response.data).keys()), 2)

    def test_patch_document(self):
        response = self.app.get('/col/3', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data).keys()), 3)

        response = self.app.patch('/col/3', data=json.dumps({'id': 3, 'first_name': 'Albert'}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 3)
        self.assertEqual(json.loads(response.data)['first_name'], 'Albert')
        self.assertEqual(len(json.loads(response.data).keys()), 3)

        response = self.app.get('/col/3', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], 3)
        self.assertEqual(json.loads(response.data)['first_name'], 'Albert')
        self.assertEqual(len(json.loads(response.data).keys()), 3)

    def test_delete_document(self):
        response = self.app.delete('/col/4', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/col/4', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 404)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(CrudControllerTest)

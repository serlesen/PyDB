import json, unittest

from app.controllers import app
from app.test.collections_simulator import CollectionsSimulator
from app.tools.database_context import DatabaseContext
from app.threads.threads_manager import ThreadsManager

class BulkControllerTest(unittest.TestCase):

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

    def test_bulk_insert(self):
        response = self.app.get('/collections/col/status', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        count = json.loads(response.data)['count']

        response = self.app.post('/col/bulk', data=json.dumps([{'id': 11}, {'id': 12}, {'id': 13}, {'id': 14}, {'id': 15}]), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/collections/col/status', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(json.loads(response.data)['count'], count + 5)

        response = self.app.get('/col/11', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/col/12', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/col/13', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/col/14', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/col/15', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)

    def test_bulk_insert_without_index(self):
        response = self.app.get('/collections/col/status', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        count = json.loads(response.data)['count']

        response = self.app.post('/col/bulk', data=json.dumps([{'my_id': 11}, {'my_id': 12}, {'my_id': 13}, {'my_id': 14}, {'my_id': 15}]), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/collections/col/status', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(json.loads(response.data)['count'], count + 5)

    def test_bulk_delete(self):
        response = self.app.post('/col/search', data=json.dumps({'$filter': {'first_name': 'John'}}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertTrue(len(json.loads(response.data)) > 0)

        response = self.app.delete('/col/bulk', data=json.dumps({'$filter': {'first_name': 'John'}}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/col/search', data=json.dumps({'$filter': {'first_name': 'John'}}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(len(json.loads(response.data)), 0)


    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(BulkControllerTest)

import json
import timeout_decorator
import unittest

from app.controllers import app
from app.test.collections_simulator import CollectionsSimulator
from app.tools.database_context import DatabaseContext
from app.threads.threads_manager import ThreadsManager

class SearchControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if DatabaseContext.THREADS_MANAGER_CYCLING == False:
            DatabaseContext.THREADS_MANAGER_CYCLING = True
            ThreadsManager().start()

        CollectionsSimulator.build_big_col('col', ['id'])
        CollectionsSimulator.build_users_col()
    
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()
        DatabaseContext.THREADS_MANAGER_CYCLING = False

    @timeout_decorator.timeout(4)
    def test_search_over_500000_docs(self):
        response = self.app.post('/col/search', data=json.dumps({'$filter': {'id': 449994}}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['id'], 449994)

    @timeout_decorator.timeout(4)
    def test_not_found_search_over_500000_docs(self):
        response = self.app.post('/col/search', data=json.dumps({'$filter': {'id': 949994}}), content_type='application/json', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE'})
        self.assertEqual(response.status_code, 404)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(SearchControllerTest)

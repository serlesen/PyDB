import json
import unittest

from app.controllers import app
from app.test.collections_simulator import CollectionsSimulator
from app.tools.database_context import DatabaseContext
from app.threads.threads_manager import ThreadsManager

class DatabaseControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if DatabaseContext.THREADS_MANAGER_CYCLING == False:
            DatabaseContext.THREADS_MANAGER_CYCLING = True
            ThreadsManager().start()

        CollectionsSimulator.build_users_col()
    
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()
        DatabaseContext.THREADS_MANAGER_CYCLING = False

    def test_get_database_status(self):
        response = self.app.get('/status', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1NjM3OTcsInN1YiI6Mn0.ZFvT2iTVJS66kCVjIuT97JfLW55Vf6R5HtSk0fNK4NE'})
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(len(response_data['collections']), 1)
        self.assertEqual(response_data['collections'][0]['collection'], 'users')
        self.assertTrue('cleaning_operations' in response_data)
        self.assertTrue('query_operations' in response_data)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(DatabaseControllerTest)

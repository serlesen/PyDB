import time
import unittest

from unittest import mock

from app.services.query_manager import QueryManager
from app.test.collections_simulator import CollectionsSimulator
from app.threads.replication_stack import ReplicationStack
from app.tools.database_context import DatabaseContext
from app.threads.threads_manager import ThreadsManager

class ReplicationThreadTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if DatabaseContext.THREADS_MANAGER_CYCLING == False:
            DatabaseContext.THREADS_MANAGER_CYCLING = True
            ThreadsManager().start()

        CollectionsSimulator.build_single_col('col', ['id'])

    def setUp(self):
        DatabaseContext.SLAVES = {'localhost:5001': 'first_token', 'localhost:5002': None}
        self.query_manager = QueryManager()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()
        DatabaseContext.THREADS_MANAGER_CYCLING = False

    def tearDown(self):
        DatabaseContext.SLAVES = {}

    def mocked_requests(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if kwargs['url'] == 'localhost:5001/admin/replicate/sync' or kwargs['url'] == 'localhost:5002/admin/replicate/sync':
            return MockResponse({}, 200)
        if kwargs['url'] == 'localhost:5002/admin/replicate/auth':
            return MockResponse({'login': 'replicator', 'token': 'second_token'}, 200)

        return MockResponse(None, 404)

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_replicate_upsert(self, mock_post):
        self.assertFalse(ReplicationStack.get_instance().contains_data())
        self.query_manager.upsert('col', {'id': 1, 'first_name': 'fn', 'last_name': 'ln'})

        while ReplicationStack.get_instance().contains_data() is True:
            time.sleep(DatabaseContext.THREADS_CYCLE)

        self.assertEqual(len(ReplicationStack.get_instance().errors), 0)

        self.assertIn(mock.call(url='localhost:5002/admin/replicate/auth'), mock_post.call_args_list)
        self.assertIn(mock.call(url='localhost:5001/admin/replicate/sync', data={'collection': 'col', 'doc': {'id': 1, 'first_name': 'fn', 'last_name': 'ln'}}, headers={'Authorization': 'Bearer first_token'}), mock_post.call_args_list)
        self.assertIn(mock.call(url='localhost:5002/admin/replicate/sync', data={'collection': 'col', 'doc': {'id': 1, 'first_name': 'fn', 'last_name': 'ln'}}, headers={'Authorization': 'Bearer second_token'}), mock_post.call_args_list)

        self.assertEqual(len(mock_post.call_args_list), 3)

    @mock.patch('requests.post', side_effect=mocked_requests)
    @mock.patch('requests.delete', side_effect=mocked_requests)
    def test_replicate_delete(self, mock_delete, mock_post):
        self.assertFalse(ReplicationStack.get_instance().contains_data())
        self.query_manager.delete('col', 3)

        while ReplicationStack.get_instance().contains_data() is True:
            time.sleep(DatabaseContext.THREADS_CYCLE)

        self.assertEqual(len(ReplicationStack.get_instance().errors), 0)

        self.assertIn(mock.call(url='localhost:5002/admin/replicate/auth'), mock_post.call_args_list)
        self.assertIn(mock.call(url='localhost:5001/admin/replicate/sync', data={'collection': 'col', 'id': 3}, headers={'Authorization': 'Bearer first_token'}), mock_delete.call_args_list)
        self.assertIn(mock.call(url='localhost:5002/admin/replicate/sync', data={'collection': 'col', 'id': 3}, headers={'Authorization': 'Bearer second_token'}), mock_delete.call_args_list)

        self.assertEqual(len(mock_delete.call_args_list), 2)
        self.assertEqual(len(mock_post.call_args_list), 1)


    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(ReplicationThreadTest)

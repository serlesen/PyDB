import unittest

from app.exceptions.app_exception import AppException
from app.services.auth_service import AuthService
from app.services.data_service import DataService
from app.services.indexes_service import IndexesService
from app.test.collections_simulator import CollectionsSimulator
from app.threads.threads_manager import ThreadsManager
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext


class AuthServiceTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        if DatabaseContext.THREADS_MANAGER_CYCLING == False:
            DatabaseContext.THREADS_MANAGER_CYCLING = True
            ThreadsManager().start()

        CollectionsSimulator.build_users_col()

        col_meta_data = CollectionMetaData('users')
        indexes_service = IndexesService()
        data_service = DataService()
        docs = data_service.find_all(col_meta_data, None)
        indexes_service.build_index(col_meta_data, docs, 'id')
        indexes_service.build_index(col_meta_data, docs, 'login')

    def setUp(self):
        self.auth_service = AuthService()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()
        DatabaseContext.THREADS_MANAGER_CYCLING = False

    def test_login_success_with_password(self):
        result = self.auth_service.login('admin', 'admin')
        self.assertEqual(result['login'], 'admin')

    def test_login_fail_with_password(self):
        try:
            self.auth_service.login('admin', 'false')
            self.fail()
        except AppException as e:
            self.assertEqual(e.message, 'Authentication failed')

    def test_get_user_by_token(self):
        result = self.auth_service.get_user_by_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzU5OTEwNDUsInN1YiI6MX0._jTMkfDl2RKzY_r6nUDVwFG8xlEuZPFFr7zvqWXJmcM')
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['login'], 'admin')

    def test_fail_get_user_by_invalid_token(self):
        try:
            self.auth_service.get_user_by_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzU5OTEwNDUsInN1YiI6MX0._jTMkfDl2RKzY_r6nUDVwFG8xlEuZPFFr7zvqWXJmcN')
            self.fail()
        except AppException as e:
            self.assertEqual(e.message, 'Authentication failed')

    def test_logout(self):
        token = self.auth_service.login('admin', 'admin')['token']
        result = self.auth_service.logout(token)
        self.assertTrue(token not in result['tokens'])

    def test_logout_all(self):
        token = self.auth_service.login('admin', 'admin')['token']
        result = self.auth_service.logout_all(token)
        self.assertEqual(len(result['tokens']), 0)

    def test_create_user(self):
        new_user = {'login' : 'user', 'password' : 'user'}
        user = self.auth_service.create_user(new_user)
        self.assertEqual(new_user['login'], user['login'])
        self.assertNotEqual(new_user['password'], user['password'])
        self.assertTrue('id' in user)
        self.assertTrue('tokens' in user)

    def suite():
        return unittest.TestLoader.loadTestsFromTestCase(AuthServiceTest)

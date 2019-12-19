import json
import unittest

from app.controllers import app
from app.test.collections_simulator import CollectionsSimulator
from app.tools.database_context import DatabaseContext
from app.threads.threads_manager import ThreadsManager

class AuthControllerTest(unittest.TestCase):

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

    def test_login(self):
        response = self.app.post('/auth/login', data=json.dumps({'login': 'admin', 'password': 'admin'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        login_info = json.loads(response.data)
        self.assertEqual(login_info['login'], 'admin')
        self.assertTrue('token' in login_info)

    def test_logout(self):
        response = self.app.post('/auth/login', data=json.dumps({'login': 'admin', 'password': 'admin'}), content_type='application/json')
        token = json.loads(response.data)['token']

        response = self.app.post('/auth/logout', headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.app.post('/auth/login', data=json.dumps({'login': 'admin', 'password': 'admin'}), content_type='application/json')
        token = json.loads(response.data)['token']

        response = self.app.post('/auth/user', data=json.dumps({'login': 'new-user', 'password': 'new-user'}), headers={'Authorization': 'Bearer {}'.format(token)}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/auth/login', data=json.dumps({'login': 'new-user', 'password': 'new-user'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        login_info = json.loads(response.data)
        self.assertEqual(login_info['login'], 'new-user')
        self.assertTrue('token' in login_info)

    def test_get_user(self):
        response = self.app.post('/auth/login', data=json.dumps({'login': 'admin', 'password': 'admin'}), content_type='application/json')
        token = json.loads(response.data)['token']

        response = self.app.get('/auth/user', headers={'Authorization': 'Bearer {}'.format(token)}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        user = json.loads(response.data)
        self.assertEqual(user['login'], 'admin')
        self.assertNotEqual(user['password'], 'admin')

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(AuthControllerTest)

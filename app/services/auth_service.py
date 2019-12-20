import jwt
import uuid

from datetime import datetime
from flask_bcrypt import Bcrypt

from app.exceptions.app_exception import AppException
from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.crud_service import CrudService
from app.services.query_manager import QueryManager
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

#
# Class to handle the users authentication.
# The authentication method is JWT.
#
class AuthService(object):

    def __init__(self):
        self.crud_service = DependencyInjectionsService.get_instance().get_service(CrudService)
        self.query_manager = DependencyInjectionsService.get_instance().get_service(QueryManager)
        self.bcrypt = Bcrypt()

    def login(self, login, password):
        results = self.query_manager.search('users', {'$filter': {'login': login}, '$size': 1})

        if len(results) != 1:
            raise AppException('Authentication failed', 401)
        user = results[0]

        if not self.bcrypt.check_password_hash(user['password'], password):
            raise AppException('Authentication failed', 401)

        token = self.generate_auth_token(user['id'])
        user['tokens'].append(token)

        col_meta_data = CollectionMetaData('users')
        self.crud_service.upsert(col_meta_data, user)

        return {'login': user['login'], 'token': token}

    def login_for_api(self, login):
        results = self.query_manager.search('users', {'$filter': {'login': login}})

        if len(results) != 1:
            raise AppException('Authentication failed', 401)

        token = self.generate_auth_token(user['id'])
        user['tokens'].append(token)

        col_meta_data = CollectionMetaData('users')
        self.crud_service.upsert(col_meta_data, user)

        return {'login': user['login'], 'token': token}

    def get_user_by_token(self, token):
        payload = jwt.decode(token, DatabaseContext.PASSWORDS_SECRET_KEY, algorithms=['HS256'])
        results = self.query_manager.search('users', {'$filter': {'id': payload['sub'], 'tokens': token}})

        if len(results) != 1:
            raise AppException('Authentication failed', 401)
        return results[0]

    def generate_auth_token(self, user_id):
        payload = {'iat': datetime.utcnow(), 'sub': user_id}
        return jwt.encode(payload, DatabaseContext.PASSWORDS_SECRET_KEY, algorithm='HS256').decode()

    def logout(self, token):
        payload = jwt.decode(token, DatabaseContext.PASSWORDS_SECRET_KEY, algorithms=['HS256'])
        results = self.query_manager.search('users', {'$filter': {'id': payload['sub'], 'tokens': token}})

        if len(results) != 1:
            raise AppException('Authentication failed', 401)
        user = results[0]

        user['tokens'].remove(token)
        self.crud_service.upsert(CollectionMetaData('users'), user)

        return user

    def logout_all(self, token):
        payload = jwt.decode(token, DatabaseContext.PASSWORDS_SECRET_KEY, algorithms=['HS256'])
        results = self.query_manager.search('users', {'$filter': {'id': payload['sub'], 'tokens': token}})

        if len(results) != 1:
            raise AppException('Authentication failed', 401)
        user = results[0]

        user['tokens'].clear()
        self.crud_service.upsert(CollectionMetaData('users'), user)

        return user

    def create_user(self, new_user):
        # FIXME check if login already exists
        user = {'id': str(uuid.uuid4()),
                'login': new_user['login'],
                'password': self.bcrypt.generate_password_hash(new_user['password'], DatabaseContext.BCRYPT_LOG_ROUNDS).decode(),
                'tokens': []
                }
        result = self.crud_service.upsert(CollectionMetaData('users'), user)
        return result


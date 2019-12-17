import functools

from flask import request

from app.auth.permissions import Permissions
from app.auth.roles import Roles
from app.exceptions.app_exception import AppException
from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.auth_service import AuthService


auth_service = DependencyInjectionsService.get_instance().get_service(AuthService)

def has_permission(permission):
    def inner_has_permission(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = identify_authenticated_user(request)
    
            if Permissions.validate(Roles.EDITOR, user['role']):
                return func(*args, **kwargs)
            
            collection = kwargs['collection']
            if collection in user['permissions'] and Permissions.validate(permission, user['permissions'][collection]):
                return func(*args, **kwargs)
    
            raise AppException('Permissions not enough', 403)
        return wrapper
    return inner_has_permission

def has_role(role):
    def inner_has_role(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = identify_authenticated_user(request)
    
            if Roles.validate(role, user['role']):
                return func(*args, **kwargs)
    
            raise AppException('Role not enough', 403)
        return wrapper
    return inner_has_role

def identify_authenticated_user(request):
        bearer_token = request.headers.get('Authorization')
        if not bearer_token:
            raise AppException('Missing authentication token', 401)
        split = bearer_token.split(' ')
        if len(split) != 2:
            raise AppException('Missing authentication token', 401)
        return auth_service.get_user_by_token(split[1])


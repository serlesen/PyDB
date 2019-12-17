from flask import Flask, request, abort, make_response, jsonify

from app.auth.decorators import has_role
from app.auth.roles import Roles
from app.controllers import app, auth_service

@app.route('/auth/login', methods=['POST'])
def login():
    if not request.json:
        abort(405)
    login_info = request.json
    result = auth_service.login(login_info['login'], login_info['password'])
    return jsonify(result)

@app.route('/auth/logout', methods=['POST'])
@has_role(Roles.USER)
def logout():
    bearer_token = request.headers.get('Authorization')
    if not bearer_token:
        abort(401)
    split = bearer_token.split(' ')
    if len(split) != 2:
        abort(401)
    auth_service.logout(split[1])
    return jsonify({})

@app.route('/auth/user', methods=['POST'])
@has_role(Roles.ADMIN)
def create_user():
    if not request.json:
        abort(405)
    new_user = auth_service.create_user(request.json)
    return jsonify(new_user)

@app.route('/auth/user', methods=['GET'])
@has_role(Roles.USER)
def get_user():
    bearer_token = request.headers.get('Authorization')
    if not bearer_token:
        abort(401)
    split = bearer_token.split(' ')
    if len(split) != 2:
        abort(401)
    user = auth_service.get_user_by_token(split[1])
    return jsonify(user)

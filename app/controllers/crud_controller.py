from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import query_manager

from app.auth.decorators import has_permission
from app.auth.permissions import Permissions
from app.exceptions.app_exception import AppException

@app.route('/<collection>', methods=['POST'])
@has_permission(Permissions.WRITE)
def create(collection):
    if not request.json:
        abort(405)
    return jsonify(query_manager.create(collection, request.json)), 201

@app.route('/<collection>/<id>')
@has_permission(Permissions.READ)
def get(collection, id):
    result = query_manager.get_one(collection, int(id))
    if len(result) != 1:
        raise AppException('Unable to find document {}'.format(id), 404)
    return jsonify(result[0])

@app.route('/<collection>/<id>', methods=['PUT'])
@has_permission(Permissions.WRITE)
def update(collection, id):
    if not request.json:
        abort(405)
    result = query_manager.update(collection, request.json, int(id))
    if result is None:
        raise AppException('Unable to find document {}'.format(id), 404)
    return jsonify(result)

@app.route('/<collection>/<id>', methods=['DELETE'])
@has_permission(Permissions.WRITE)
def delete(collection, id):
    result = query_manager.delete(collection, int(id))
    if result is None:
        raise AppException('Unable to find document {}'.format(id), 404)
    return jsonify(result)

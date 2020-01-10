import uuid

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
    doc = request.json
    if 'id' not in doc:
        doc['id'] = str(uuid.uuid4())
    return jsonify(query_manager.upsert(collection, [doc])[0]), 201

@app.route('/<collection>/<id>')
@has_permission(Permissions.READ)
def get(collection, id):
    result = query_manager.get_one(collection, int(id))
    if result is None:
        raise AppException('Unable to find document {}'.format(id), 404)
    return jsonify(result)

@app.route('/<collection>/<id>', methods=['PUT'])
@has_permission(Permissions.WRITE)
def update(collection, id):
    if not request.json:
        abort(405)
    doc = request.json
    doc['id'] = int(id)
    return jsonify(query_manager.upsert(collection, [doc])[0])

@app.route('/<collection>/<id>', methods=['PATCH'])
@has_permission(Permissions.WRITE)
def patch(collection, id):
    if not request.json:
        abort(405)
    previous_doc = query_manager.get_one(collection, int(id))
    if previous_doc is None:
        raise AppException('Unable to find document {}'.format(id), 404)

    doc = dict(previous_doc)
    patch = request.json
    for k in patch.keys():
        doc[k] = patch[k]

    return jsonify(query_manager.patch(collection, [previous_doc], [doc])[0])

@app.route('/<collection>/<id>', methods=['DELETE'])
@has_permission(Permissions.WRITE)
def delete(collection, id):
    results = query_manager.delete(collection, {'$filter': {'id': int(id)}})
    if results is None:
        raise AppException('Unable to find document {}'.format(id), 404)
    return jsonify(results[0])

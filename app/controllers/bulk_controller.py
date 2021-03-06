import random, string, uuid
from operator import itemgetter

from flask import Flask, request, abort, make_response, jsonify
from app.auth.decorators import has_permission
from app.auth.permissions import Permissions
from app.controllers import app
from app.controllers import query_manager
from app.exceptions.app_exception import AppException
from app.tools.argument_parser import ArgumentParser

@app.route('/<collection>/bulk', methods=['POST', 'PUT'])
@has_permission(Permissions.WRITE)
def bulk_upsert(collection):
    if not request.json:
        abort(405)
    docs = request.json
    for idx, d in enumerate(docs):
        if 'id' not in d:
            d['id'] = str(uuid.uuid4())
    query_manager.upsert(collection, docs)
    return jsonify({})

@app.route('/<collection>/bulk', methods=['PATCH'])
@has_permission(Permissions.WRITE)
def bulk_patch(collection):
    """ For bulk patch, the documents must contain their IDs. """
    if not request.json:
        abort(405)

    ids = []
    for d in request.json:
        if 'id' in d:
            ids.append(d['id'])
        else:
            raise AppException('Input documents must contain their ID', 400)

    previous_docs = query_manager.search(collection, {'$filter': {'id': ids}})

    previous_docs = sorted(previous_docs, key=itemgetter('id'))
    docs = sorted(list(previous_docs), key=itemgetter('id'))

    patch = sorted(request.json, key=itemgetter('id'))
    for i, p in enumerate(patch):
        for k in p.keys():
            docs[i][k] = p[k]

    query_manager.patch(collection, previous_docs, docs)
    return jsonify({})

@app.route('/<collection>/bulk', methods=['DELETE'])
@has_permission(Permissions.WRITE)
def bulk_delete(collection):
    if not request.json:
        abort(405)
    if not ArgumentParser.validate(request.json):
        raise AppException('Invalid input format', 400)
    query_manager.delete(collection, request.json)
    return jsonify({})

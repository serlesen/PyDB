import random, string, uuid

from flask import Flask, request, abort, make_response, jsonify
from app.auth.decorators import has_permission
from app.auth.permissions import Permissions
from app.controllers import app
from app.controllers import query_manager
from app.tools.argument_parser import ArgumentParser

@app.route('/<collection>/bulk', methods=['POST'])
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


@app.route('/<collection>/bulk', methods=['DELETE'])
@has_permission(Permissions.WRITE)
def bulk_delete(collection):
    if not request.json:
        abort(405)
    if not ArgumentParser.validate(request.json):
        raise AppException('Invalid input format', 400)
    query_manager.delete(collection, request.json)
    return jsonify({})

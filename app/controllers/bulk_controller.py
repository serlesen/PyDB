import random, string, uuid

from flask import Flask, request, abort, make_response, jsonify
from app.auth.decorators import has_permission
from app.auth.permissions import Permissions
from app.controllers import app
from app.controllers import crud_service
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

@app.route('/<collection>/bulk', methods=['POST'])
@has_permission(Permissions.WRITE)
def bulk(collection):
    if not request.json:
        abort(405)
    docs = request.json
    for idx, d in enumerate(docs):
        if 'id' not in d:
            print(d)
            d['id'] = str(uuid.uuid4())
    crud_service.bulk_upsert(CollectionMetaData(collection), docs)
    return "Done", 200

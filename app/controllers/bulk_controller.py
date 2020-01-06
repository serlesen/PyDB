import random, string

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
    # FIXME use the real input and check for id
    for i in range(5):
        l = []
        for j in range(DatabaseContext.MAX_DOC_PER_FILE):
            l.append({"id":((i*DatabaseContext.MAX_DOC_PER_FILE)+j),
                         "first_name":"al",
                         "last_name":"jym",
                         "age":15,
                         "address":"somewhere",
                         "job":"something",
                         "salary":15352,
                         "email":"my.email@google.com"
                    })
        crud_service.bulk_upsert(CollectionMetaData(collection), l)
    return "Done"

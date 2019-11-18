import random, string

from flask import Flask, request, abort, make_response, jsonify
from app.controllers import app
from app.controllers import crud_service
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

@app.route('/<collection>/bulk')
def bulk(collection):
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
        crud_service.bulk_insert(CollectionMetaData(collection), l)
    return "Done"

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

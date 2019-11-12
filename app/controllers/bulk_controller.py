from flask import Flask, request, abort, make_response, jsonify
from app.controllers import app
from app.controllers import crud_service
import random, string

@app.route('/<collection>/bulk')
def bulk(collection):
    for i in range(250):
        l = []
        for j in range(1000):
            l.append({"id":((i*1000)+j),
                         "first_name":"al",
                         "last_name":"jym",
                         "age":15,
                         "address":"somewhere",
                         "job":"something",
                         "salary":15352,
                         "email":"my.email@google.com"
                    })
        crud_service.bulk_insert(collection, l)
    return "Done"

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

from flask import Flask, request, abort, make_response, jsonify
from app.controllers import app
from app.controllers import crud_service
import random, string

@app.route('/generate')
def generate():
    for i in range(1500):
        crud_service.create({"id":(1000+i),
                     "first_name":"al",
                     "last_name":"jym",
                     "age":15,
                     "address":"somewhere",
                     "job":"something",
                     "salary":15352,
                     "email":"my.email@google.com"
                })
    return "Done"

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

from flask import Flask, request, abort, make_response, jsonify
from app.controllers import app
from app.controllers import crud_service
from app.controllers import search_service
from app.tools.search_context import SearchContext

@app.route('/', methods=['POST'])
def create():
    if not request.json:
        abort(405)
    return crud_service.create(request.json)

@app.route('/<id>')
def get(id):
    result = search_service.search(SearchContext({"filter":{"id":int(id)}}))
    if result is None or len(result) != 1:
        abort(404)
    return result[0]

@app.route('/<id>', methods=['PUT'])
def update(id):
    if not request.json:
        abort(405)
    result = crud_service.update(int(id), request.json)
    if result is None or len(result) != 1:
        abort(404)
    return result[0]

@app.route('/<id>', methods=['DELETE'])
def delete(id):
    result = crud_service.update(int(id), None)
    if result is None or len(result) != 1:
        abort(404)
    return result[0]

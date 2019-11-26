from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import collections_service

@app.route('/collections/<collection>', methods=['GET'])
def collection_status(collection):
    return collections_service.get_status(collection)

@app.route('/collections/<collection>', methods=['POST'])
def create_collection(collection):
    return collections_service.create(collection)

@app.route('/collections/<collection>/index/<field>', methods=['POST'])
def create_index(collection, field):
    return collections_service.create_index(collection, field)

@app.route('/collections/<collection>', methods=['DELETE'])
def delete_collection(collection):
    return collections_service.remove(collection)

@app.route('/collections/<collection>/index/<field>', methods=['DELETE'])
def delete_index(collection, field):
    return collections_service.remove_index(collection, field)

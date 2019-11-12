from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import collections_service

@app.route('/collections/<collection>', methods=['POST'])
def create_collection(collection):
    return collections_service.create(collection)

@app.route('/collections/<collection>', methods=['DELETE'])
def delete_collection(collection):
    return collections_service.remove(collection)

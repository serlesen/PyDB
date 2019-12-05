from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import collections_service

from app.tools.collection_meta_data import CollectionMetaData

@app.route('/collections/<collection>/status', methods=['GET'])
def collection_status(collection):
    return collections_service.get_status(collection)

@app.route('/collections/<collection>', methods=['POST'])
def create_collection(collection):
    return collections_service.create(collection)

@app.route('/collections/<collection>/index/<field>', methods=['POST'])
def create_index(collection, field):
	col_meta_data = CollectionMetaData(collection)
	docs = file_reader.find_all(col_meta_data, None)
    return indexes_service.build_index(col_meta_data, docs, field)

@app.route('/collections/<collection>', methods=['DELETE'])
def delete_collection(collection):
    return collections_service.remove(collection)

@app.route('/collections/<collection>/index/<field>', methods=['DELETE'])
def delete_index(collection, field):
    return indexes_service.remove_index(CollectionMetaData(collection), field)

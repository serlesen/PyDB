from flask import Flask, request, abort, make_response, jsonify
from app.controllers import app
from app.controllers import search_service
from app.tools.argument_parser import ArgumentParser
from app.tools.search_context import SearchContext

@app.route('/<collection>/search', methods=['POST'])
def search(collection):
    if not request.json:
        abort(405)
    if not ArgumentParser.validate(request.json):
        abort(400)
    result = search_service.search(collection, SearchContext(request.json))
    if result is None:
        abort(404)
    return result

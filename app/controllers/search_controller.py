from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import query_manager
from app.exceptions.app_exception import AppException
from app.tools.argument_parser import ArgumentParser
from app.tools.results_mapper import ResultsMapper
from app.tools.search_context import SearchContext

@app.route('/<collection>/search', methods=['POST'])
def search(collection):
    if not request.json:
        abort(405)
    if not ArgumentParser.validate(request.json):
        raise AppException('Invalid input format', 400)
    result = query_manager.search(collection, request.json)
    if len(result) == 0:
        abort(404)
    if SearchContext(request.json).map is None:
        return jsonify(result)
    return jsonify(ResultsMapper.map(result))

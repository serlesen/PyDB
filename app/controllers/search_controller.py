from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import search_service
from app.exceptions.app_exception import AppException
from app.tools.argument_parser import ArgumentParser
from app.tools.results_mapper import ResultsMapper

@app.route('/<collection>/search', methods=['POST'])
def search(collection):
    if not request.json:
        abort(405)
    if not ArgumentParser.validate(request.json):
        raise AppException('Invalid input format', 400)
    result = search_service.search(collection, request.json)
    if len(result) == 0:
        abort(404)
    if search_context.map is None:
        return result
    return ResultsMapper.map(result)

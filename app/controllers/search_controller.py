from flask import Flask, request, abort, make_response, jsonify
from app.controllers import app
from app.controllers import search_service
from app.tools.argument_parser import ArgumentParser
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.results_mapper import ResultsMapper
from app.tools.search_context import SearchContext

@app.route('/<collection>/search', methods=['POST'])
def search(collection):
    if not request.json:
        abort(405)
    if not ArgumentParser.validate(request.json):
        abort(400)
    search_context = SearchContext(request.json)
    result = search_service.search(CollectionMetaData(collection), search_context)
    if len(result) == 0:
        abort(404)
    if search_context.map is None:
        return result
    return ResultsMapper.map(result)

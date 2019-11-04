from flask import Flask, request, abort, make_response, jsonify
from app.controllers import app

@app.errorhandler(405)
def method_not_supported(error):
    return make_response(jsonify({'error': 'Unsupported method'}), 405)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Invalid input'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Document not found'}), 400)

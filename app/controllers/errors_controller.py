from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.exceptions.app_exception import AppException

@app.errorhandler(405)
def method_not_supported(error):
    return make_response(jsonify({'error': 'Unsupported method'}), 405)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Invalid input'}), 400)

@app.errorhandler(401)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid token'}), 401)

@app.errorhandler(403)
def not_found(error):
    return make_response(jsonify({'error': 'Insufficient priviledges'}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify([]), 404)

@app.errorhandler(AppException)
def handle_custom_exception(error):
    return make_response(jsonify({'error': error.message}), error.http_code)

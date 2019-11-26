from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import database_service

@app.route('/status', methods=['GET'])
def database_status():
    return database_service.get_status()

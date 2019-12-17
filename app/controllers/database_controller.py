from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import database_service

from app.auth.decorators import has_role
from app.auth.roles import Roles

@app.route('/status', methods=['GET'])
@has_role(Roles.EDITOR)
def database_status():
    return jsonify(database_service.get_status())

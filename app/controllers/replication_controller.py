from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import query_manager

from app.auth.decorators import has_role
from app.auth.roles import Roles

@app.route('/admin/replicate', methods=['POST', 'DELETE'])
@has_role(Roles.REPLICATOR)
def replicate():
    data = request.json
    if request.method == 'POST':
        return jsonify(query_manager.upsert(data['collection'], data['doc'])), 200
    return jsonify(query_manager.delete(data['collection'], data['id'])), 200

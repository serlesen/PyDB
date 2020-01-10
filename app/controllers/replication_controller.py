from flask import Flask, request, abort, make_response, jsonify

from app.controllers import app
from app.controllers import auth_service
from app.controllers import query_manager

from app.auth.decorators import has_role
from app.auth.roles import Roles
from app.exceptions.app_exception import AppException
from app.tools.database_context import DatabaseContext


@app.route('/admin/replicate/auth', methods=['POST'])
def replicate_auth():
    if request.remote_addr not in DatabaseContext.MASTER:
        raise AppException(f'Auth request coming from unknown host {request.remote_addr}', 403)

    result = auth_service.login_for_api('replicator')
    return jsonify(result)

@app.route('/admin/replicate/sync', methods=['POST', 'PATCH', 'DELETE'])
@has_role(Roles.REPLICATOR)
def replicate_sync():
    data = request.json
    if request.method == 'POST':
        return jsonify(query_manager.upsert(data['collection'], data['doc'])), 200
    if request.method == 'PATCH':
        return jsonify(query_manager.patch(data['collection'], data['previous_doc'], data['doc'])), 200
    return jsonify(query_manager.delete(data['collection'], data['id'])), 200

#!/usr/bin/env python3

"""
Route module for the API
"""

import os
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = os.environ.get('AUTH_TYPE', None)
auth_choices = {'auth': Auth, 'basic_auth': BasicAuth}

if AUTH_TYPE in auth_choices:
    auth = auth_choices[AUTH_TYPE]()


@app.before_request
def before_request():
    """
    Performs actions before each request is processed.

    This function checks if the request path requires authentication
    and authorization.
    If authentication is required, it checks if the request
    has a valid authorization header.
    If authorization is required, it checks if the current user has
    the necessary permissions.
    If any of the checks fail, it aborts the request with
    the appropriate HTTP status code.
    """
    paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if auth is None:
        return
    if auth.require_auth(request.path, paths):
        if auth.authorization_header(request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(debug=True, host=host, port=port)

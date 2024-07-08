#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    _stats = {}
    _stats['users'] = User.count()
    return jsonify(_stats)


@app_views.route('/unauthorized', strict_slashes=False)
def unauthenticated_user() -> str:
    """ Unauthorized unauthenticated user
    """
    abort(401)

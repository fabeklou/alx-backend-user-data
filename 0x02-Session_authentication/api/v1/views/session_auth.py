#!/usr/bin/env python3

"""
This module contains the session authentication views for the API.

It provides the following routes:
- /auth_session/login: POST method to authenticate a user based on
    the provided email and password.

The module also defines the following functions:
- authenticate_user(): Authenticates a user based on the provided
    email and password.

"""

from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, make_response, abort
import os


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def authenticate_user() -> str:
    """
    Authenticates a user based on the provided email and password.

    Returns:
        A response object containing the user's information
        if authentication is successful.
        Otherwise, returns an error response with the appropriate
        status code.

    Raises:
        None
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user_list = User.search({'email': email})
    if not user_list:
        return jsonify({
            "error": "no user found for this email"}), 404

    valid_user = None
    for user in user_list:
        if user.is_valid_password(password):
            valid_user = user
            break

    if valid_user is None:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(valid_user.id)
    cookie_name = os.environ.get('SESSION_NAME')

    user_json = valid_user.to_json()
    response = make_response(jsonify(user_json))
    response.set_cookie(cookie_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=["DELETE"], strict_slashes=False)
def destroy_session() -> str:
    """
    Destroy the current session.

    This function destroys the current session by calling
    the `destroy_session` method from the `auth` module.
    If the session was successfully destroyed, it returns an
    empty JSON response with a status code of 200.
    If the session was not destroyed, it raises a 404 error.

    Returns:
        A JSON response with an empty body and a status code of 200.

    Raises:
        404: If the session was not destroyed.
    """
    from api.v1.app import auth
    was_destroyed = auth.destroy_session(request)

    if not was_destroyed:
        abort(404)

    return jsonify({}), 200

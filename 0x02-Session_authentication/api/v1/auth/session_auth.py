#!/usr/bin/env python3

"""
This module contains the SessionAuth class, which is responsible
for handling session-based authentication.
"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, make_response
import os


class SessionAuth(Auth):
    """
    SessionAuth class represents the session-based authentication mechanism.

    This class inherits from the Auth class and provides the necessary
    methods to handle session-based authentication.

    Attributes:
        user_id_by_session_id (dict): A dictionary that maps
            session IDs to user IDs.

    Methods:
        create_session(user_id: str = None) -> str:
            Creates a session for the given user ID.
        user_id_for_session_id(session_id: str = None) -> str:
            Retrieves the user ID associated with a given session ID.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session for the given user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The session ID generated for the user.
        """
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID associated with the given session ID.

        """
        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        Retrieves the current user based on the session cookie.

        Args:
            request (Request): The request object (default is None).

        Returns:
            User: The User object associated with the session cookie.

        """
        s_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(s_cookie)
        return User.get(user_id)


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

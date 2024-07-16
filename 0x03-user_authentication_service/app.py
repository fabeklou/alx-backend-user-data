#!/usr/bin/env python3

"""
This module contains the Flask application for
the user authentication service.

It provides the following routes:
- GET /: Returns a welcome message.
- POST /users: Registers a new user with the provided
email and password.

The module also imports the Auth class from the auth module.
"""

from flask import Flask, jsonify, request, abort, make_response
from flask import redirect, url_for
from auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route('/', methods=['GET'])
def woezon() -> str:
    """
    This function returns a JSON response with a welcome message.

    Returns:
        A JSON response containing a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Register a new user.

    This function registers a new user by extracting the email
    and password from the request form.
    It then calls the `register_user` function from the `AUTH`
    module to register the user.

    Returns:
        A JSON response containing the email and a message
            indicating the status of the registration.

    Raises:
        ValueError: If the email is already registered.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
        abort(400)

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400
    else:
        return jsonify({'email': email, 'message': 'user created'})


@app.route('/sessions', methods=['POST'])
def login():
    """
    Logs in a user by validating their email and password.

    Returns:
        If the login is successful, returns a response object with
            a JSON payload containing the user's email and
            a success message.
        If the login fails, returns an HTTP 401 Unauthorized error.

    Raises:
        HTTP 400 Bad Request error if the email or password is missing.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
        abort(400)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)

        response = make_response(
            jsonify({"email": email, "message": "logged in"}))
        response.set_cookie('session_id', value=session_id)

        return response

    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Logs out the user by destroying the session.

    Returns:
        A redirect response to the specified URL.

    Raises:
        403 Forbidden: If the user associated with
            the session ID is not found.
    """

    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for('woezon'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

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

from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()

app = Flask(__name__)
app.url_map.strict_slashes = False


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
        return jsonify({'email': email, 'message': 'user created'}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

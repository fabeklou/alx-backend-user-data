#!/usr/bin/env python3

"""
This module is used to perform end-to-end integration tests for an API.
It contains functions that simulate user registration, login,
profile access, logout, password reset, and password update.
These functions make HTTP requests to the API and assert
the expected responses.
The module should only be executed as the main module to run
the integration tests.
"""

import requests

API_URL = 'http://0.0.0.0:5000'
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}


def register_user(email: str, password: str) -> None:
    """
    Register a user with the given email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None

    Raises:
        AssertionError: If the registration request fails or
            returns an unexpected response.
    """
    ROUTE_URL = '{}/users'.format(API_URL)

    # missing password
    form_data = {'email': email}
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 400

    # missing email
    form_data = {'password': password}
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 400

    # valid request
    form_data = {'email': email, 'password': password}
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 200
    assert res.json() == {'email': email, 'message': 'user created'}

    # email already registered
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 400
    assert res.json() == {'message': 'email already registered'}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Sends multiple requests to the authentication service API
    with different combinations of missing email and password
    to simulate a login attempt with a wrong password.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    ROUTE_URL = '{}/sessions'.format(API_URL)

    # missing password
    form_data = {'email': email}
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 400

    # missing email
    form_data = {'password': password}
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 400

    # valid request
    form_data = {'email': email, 'password': password}
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in a user with the provided email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID of the logged-in user.

    Raises:
        AssertionError: If the login request fails or the response
            is not as expected.
    """
    ROUTE_URL = '{}/sessions'.format(API_URL)

    form_data = {'email': email, 'password': password}
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 200
    assert res.json() == {'email': email, 'message': 'logged in'}

    session_id = res.cookies.get('session_id')
    assert isinstance(session_id, str)

    return session_id


def profile_unlogged() -> None:
    """
    Sends a GET request to the profile route without a
    valid session cookie.

    Returns:
        None
    """
    ROUTE_URL = '{}/profile'.format(API_URL)

    # request without cookie
    res = requests.get(ROUTE_URL)
    assert res.status_code == 403

    # set a cookie with fake session id
    cookie = {'session_id': 'I Am Groot'}
    res = requests.get(ROUTE_URL, cookies=cookie)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Retrieves the profile information of a logged-in user.

    Args:
        session_id (str): The session ID of the logged-in user.

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 200
            or if the payload email is not a string.
    """
    ROUTE_URL = '{}/profile'.format(API_URL)

    cookie = {'session_id': session_id}
    res = requests.get(ROUTE_URL, cookies=cookie)
    assert res.status_code == 200
    payload = res.json()
    assert isinstance(payload.get('email'), str)


def log_out(session_id: str) -> None:
    """
    Logs out a user session by sending a DELETE request
    to the API endpoint.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        None
    """
    ROUTE_URL = '{}/sessions'.format(API_URL)

    # request without cookie
    res = requests.delete(ROUTE_URL)
    assert res.status_code == 403

    # set a cookie with fake session id
    cookie = {'session_id': 'I Am The Danger !'}
    res = requests.delete(ROUTE_URL, cookies=cookie)
    assert res.status_code == 403

    # set a cookie with a valid session id
    cookie = {'session_id': session_id}
    res = requests.delete(ROUTE_URL, cookies=cookie)
    assert res.status_code == 200
    assert res.url == '{}/'.format(API_URL)


def reset_password_token(email: str) -> str:
    """
    Sends a request to reset the password for the given email
    address and returns the reset token.

    Args:
        email (str): The email address for which the password
            reset request is being made.

    Returns:
        str: The reset token received from the server.

    Raises:
        AssertionError: If the request fails or the response
            status code is not 200.
    """
    ROUTE_URL = '{}/reset_password'.format(API_URL)

    # request without email
    res = requests.post(ROUTE_URL, headers=HEADERS)
    assert res.status_code == 403

    # request with invalid email
    form_data = {'email': 'makume@gbomadessi.vivina'}
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 403

    # request with valid email
    form_data = {'email': email}
    res = requests.post(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 200
    payload = res.json()
    assert payload.get('email') == email
    reset_token = payload.get('reset_token')
    assert isinstance(reset_token, str)

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password for a user account.

    Args:
        email (str): The email address of the user.
        reset_token (str): The reset token for password reset.
        new_password (str): The new password to be set.

    Returns:
        None

    Raises:
        AssertionError: If any of the requests fail with a
            status code other than 403 or 200.
    """
    ROUTE_URL = '{}/reset_password'.format(API_URL)

    # request without email
    form_data = {'reset_token': reset_token, 'new_password': new_password}
    res = requests.put(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 403

    # request without reset_token
    form_data = {'email': email, 'new_password': new_password}
    res = requests.put(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 403

    # request without new_password
    form_data = {'email': email, 'reset_token': reset_token}
    res = requests.put(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 403

    # request with invalid reset_token
    form_data = {'email': email,
                 'reset_token': 'He who dares not offend cannot be honest.',
                 'new_password': new_password}
    res = requests.put(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 403

    # request with valid reset_token
    form_data = {'email': email,
                 'reset_token': reset_token,
                 'new_password': new_password}
    res = requests.put(ROUTE_URL, data=form_data, headers=HEADERS)
    assert res.status_code == 200
    assert res.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

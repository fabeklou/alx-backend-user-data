#!/usr/bin/env python3

"""
This module provides the Auth class for interacting
with the authentication database.
"""

from sqlalchemy.orm.exc import NoResultFound

import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    password_bytes = bytes(password, 'utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a random UUID (Universally Unique Identifier)
    and returns it as a string.

    Returns:
        str: A randomly generated UUID as a string.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initializes a new instance of the Auth class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly registered user.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the provided email and password combination is valid.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the email and password combination is valid,
                False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(
                bytes(password, 'utf-8'),
                user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Creates a session for the user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID generated for the user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            _session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=_session_id)
            return _session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves a user object based on the provided session ID.

        Args:
            session_id (str): The session ID associated with the user.

        Returns:
            User: The user object corresponding to the session ID,
                or None if no user is found.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the session for a given user.

        Args:
            user_id (int): The ID of the user whose session
                needs to be destroyed.

        Returns:
            None
        """
        if isinstance(user_id, int):
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Retrieves the reset password token for a given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If no user is found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            reset_token_uuid = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token_uuid)
            return reset_token_uuid

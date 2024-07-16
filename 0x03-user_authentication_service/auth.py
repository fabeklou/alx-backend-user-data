#!/usr/bin/env python3

"""
This module provides the Auth class for interacting
with the authentication database.
"""

from sqlalchemy.orm.exc import NoResultFound

import bcrypt
from db import DB
from user import User


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

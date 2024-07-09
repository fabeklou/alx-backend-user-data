#!/usr/bin/env python3

"""
This module provides the BasicAuth class which is a subclass of Auth.
It handles basic authentication for the API.
"""

import base64
import binascii
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth is a subclass of Auth.
    It handles basic authentication for the API.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the base64 encoded authorization header from
        the given authorization header.

        Args:
            authorization_header (str): The authorization header string.

        Returns:
            str: The base64 encoded authorization header.

        """
        prefix = 'Basic '
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith(prefix):
            return None
        return authorization_header[len(prefix):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Decodes a base64-encoded authorization header.

        Args:
            base64_authorization_header (str): The base64-encoded
                authorization header.

        Returns:
            str: The decoded authorization header as a string.

        Raises:
            None
        """
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_base64 = base64.b64decode(
                base64_authorization_header,
                validate=True)
            return decoded_base64.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts the username and password from a decoded
        base64 authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded
                base64 authorization header.

        Returns:
            Tuple[str, str]: A tuple containing the username and password
                extracted from the authorization header.
                If the authorization header is not in the correct format,
                returns (None, None).
        """
        separator = ':'
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if separator not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(separator))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a user object based on the provided
        email and password credentials.

        Args:
            user_email (str): The email address of the user.
            user_pwd (str): The password of the user.

        Returns:
            User: The user object if the credentials are valid,
                None otherwise.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        users = User.all()
        if not users:
            return None
        user = User.search({'email': user_email})
        if not user:
            return None
        valid_user = user[0]
        if valid_user.is_valid_password(user_pwd):
            return valid_user

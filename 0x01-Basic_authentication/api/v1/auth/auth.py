#!/usr/bin/env python3

"""
This module provides authentication functionality for the API.
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """
    Auth class handles authentication and authorization for the API.

    Methods:
        - require_auth(path: str, excluded_paths: List[str]) -> bool:
            Checks if authentication is required for the given path.

        - authorization_header(_request=None) -> str:
            Retrieves the authorization header from the request.

        - current_user(_request=None) -> TypeVar('User'):
            Retrieves the current user based on the request.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path.

        Args:
            path (str): The path of the request.
            excluded_paths (List[str]): List of paths that are excluded
                from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        return False

    def authorization_header(self, _request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Args:
            _request (flask.Request, optional): The request object.
                Defaults to None.

        Returns:
            str: The authorization header value.
        """
        return None

    def current_user(self, _request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Args:
            _request (flask.Request, optional): The request object.
                Defaults to None.

        Returns:
            User: The current user object.
        """
        return None

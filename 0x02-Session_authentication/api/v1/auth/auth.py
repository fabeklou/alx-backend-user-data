#!/usr/bin/env python3

"""
This module provides authentication functionality for the API.
"""

from typing import List, TypeVar
from flask import request
import re


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
        if path is None or not excluded_paths:
            return True

        if len(path) > 0 and path[-1] != "/":
            path = path + '/'

        _excluded_stars_paths = []
        _excluded_paths = []
        for excluded_path in excluded_paths:
            if len(excluded_path) > 0 and excluded_path[-1] == '*':
                _excluded_stars_paths.append(excluded_path[:-1])
            else:
                _excluded_paths.append(excluded_path)

        for p in _excluded_stars_paths:
            if path.startswith(p):
                return False
        for p in _excluded_paths:
            if p == path:
                return False
        return True

    def authorization_header(self, _request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Args:
            _request (flask.Request, optional): The request object.
                Defaults to None.

        Returns:
            str: The authorization header value.
        """
        if _request is None:
            return None
        return _request.headers.get('Authorization', None)

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

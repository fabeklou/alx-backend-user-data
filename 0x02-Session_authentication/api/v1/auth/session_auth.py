#!/usr/bin/env python3

"""
This module contains the SessionAuth class, which is responsible
for handling session-based authentication.
"""

from api.v1.auth.auth import Auth
from uuid import uuid4


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

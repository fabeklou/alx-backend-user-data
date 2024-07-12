#!/usr/bin/env python3

"""
This module contains the SessionDBAuth class, which is responsible
for session-based authentication using a database.

The SessionDBAuth class extends the SessionExpAuth class and
provides methods for creating, retrieving,
and destroying user sessions.

Attributes:
    None

Methods:
    create_session(user_id=None): Creates a new session for the specified
        user ID and saves it in the database.
    user_id_for_session_id(session_id=None): Retrieves the user ID associated
        with the given session ID from the database.
    destroy_session(request=None): Destroys the session associated with
        the given request by removing it from the database.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    This class provides session-based authentication using a database.

    Methods:
        create_session(user_id=None): Creates a new session
            for the specified user.
        user_id_for_session_id(session_id=None): Retrieves the user ID
            associated with the given session ID.
        destroy_session(request=None): Destroys the session
            associated with the given request.

    Attributes:
        session_duration: The duration (in seconds) for which a session
            is considered valid.
    """

    def create_session(self, user_id=None):
        """
        Create a new session for the given user.

        Args:
            user_id (str, optional): The ID of the user. Defaults to None.

        Returns:
            str: The session ID if the session was created successfully,
                None otherwise.
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID associated with the session ID,
                or None if the session ID is invalid or expired.
        """
        if session_id is None:
            return None

        UserSession.load_from_file()
        users = UserSession.search({'session_id': session_id})

        if not users:
            return None

        valid_user = users[0]
        session_created_at = valid_user.created_at

        if session_created_at is None:
            return None

        time_delta = timedelta(seconds=self.session_duration)
        if session_created_at + time_delta < datetime.now():
            return None

        return valid_user.user_id

    def destroy_session(self, request=None):
        """
        Destroys a user session.

        Args:
            request (Request): The request object (default: None).

        Returns:
            bool: True if the session was successfully destroyed,
                False otherwise.
        """
        session_id = self.session_cookie(request)

        if session_id is None or self.user_id_for_session_id(session_id):
            return False

        sessions = UserSession.search({'session_id': session_id})

        if not sessions:
            return False

        session = sessions[0]

        try:
            session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True

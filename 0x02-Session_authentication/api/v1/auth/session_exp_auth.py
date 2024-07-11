#!/usr/bin/env python3

"""
This module contains the `SessionExpAuth` class, which represents a
session-based authentication mechanism with session expiration.

The `SessionExpAuth` class extends the `SessionAuth` class and adds
functionality to handle session expiration. It allows creating sessions
with a specified duration and provides a method to retrieve the user ID
associated with a session ID, taking into account
the session expiration time.

Attributes:
    session_duration (int): The duration of a session in seconds.

Methods:
    create_session(user_id=None): Creates a new session for
        the specified user ID.
    user_id_for_session_id(session_id=None): Retrieves the user ID
        associated with the specified session ID.

Usage:
    session_auth = SessionExpAuth()
    session_id = session_auth.create_session(user_id='12345')
    user_id = session_auth.user_id_for_session_id(session_id=session_id)
"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Represents a session-based authentication mechanism
    with session expiration.

    This class extends the `SessionAuth` class and adds functionality
    to handle session expiration.
    It allows creating sessions with a specified duration and provides
    a method to retrieve the user ID associated with a session ID,
    taking into account the session expiration time.

    Attributes:
        session_duration (int): The duration of a session in seconds.

    Methods:
        create_session(user_id=None): Creates a new session for
        the specified user ID.
        user_id_for_session_id(session_id=None): Retrieves
        the user ID associated with the specified session ID.

    Usage:
        session_auth = SessionExpAuth()
        session_id = session_auth.create_session(user_id='12345')
        user_id = session_auth.user_id_for_session_id(session_id=session_id)
    """

    def __init__(self):
        """
        Initializes a SessionExpAuth object.

        The `__init__` method is called when a new instance of the
        SessionExpAuth class is created.
        It initializes the session duration based on the value of
        the `SESSION_DURATION` environment variable.
        """
        duration = os.environ.get('SESSION_DURATION', 0)

        try:
            duration = int(duration)
        except ValueError:
            duration = 0

        self.session_duration = duration

    def create_session(self, user_id=None):
        """
        Creates a new session for the specified user ID.

        Args:
            user_id (str): The ID of the user associated with the session.

        Returns:
            str: The session ID if the session was created successfully,
                None otherwise.
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {}
        session_dictionary = self.user_id_by_session_id[session_id]
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with the specified session ID.

        Args:
            session_id (str): The ID of the session.

        Returns:
            str: The user ID associated with the session if it is valid
                and not expired, None otherwise.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        user_id = session_dictionary.get('user_id', None)
        session_created_at = session_dictionary.get('created_at', None)

        if self.session_duration <= 0:
            return user_id

        if session_created_at is None:
            return None

        if session_created_at + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return user_id

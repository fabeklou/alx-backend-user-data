#!/usr/bin/env python3

"""
This module contains the UserSession class, which represents
a user session.

The UserSession class inherits from the Base class and has
the following attributes:
- user_id (int): The ID of the user associated with the session.
- session_id (str): The ID of the session.
"""

from models.base import Base


class UserSession(Base):
    """
    UserSession class represents a user session.

    Attributes:
        user_id (int): The ID of the user associated with the session.
        session_id (str): The ID of the session.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a new instance of the UserSession class.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

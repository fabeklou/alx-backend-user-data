#!/usr/bin/env python3

"""
This module contains the DB class and related functions
for user authentication service.

The DB class provides methods for interacting with the database,
including adding users, finding users by specific attributes,
and updating user information.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User
from typing import Dict, Union


users_attributes = {'id',
                    'email',
                    'hashed_password',
                    'session_id',
                    'reset_token'}


class DB:
    """
    DB class provides methods for interacting with the database.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): Email address of the user.
            hashed_password (str): Hashed password of the user.

        Returns:
            The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided attributes.

        Args:
            kwargs (Dict): Dictionary of attributes to search for.

        Returns:
            The found User object if a match is found, None otherwise.

        Raises:
            InvalidRequestError: If an invalid attribute is provided.

        """
        for arg in kwargs:
            if arg not in users_attributes:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update the information of a user in the database.

        Args:
            user_id (int): ID of the user to update.
            kwargs (Dict): Dictionary of attributes to update.

        Raises:
            ValueError: If an invalid attribute is provided.

        """
        for arg in kwargs:
            if arg not in users_attributes:
                raise ValueError

        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            pass
        else:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self._session.commit()

#!/usr/bin/env python3

"""
This module contains the User class,
which represents a user in the system.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str): The session ID of the user.
        reset_token (str): The reset token for the user's password reset.
    """

    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(250), nullable=False)
    hashed_password = Column('hashed_password', String(250), nullable=False)
    session_id = Column('session_id', String(250), nullable=True)
    reset_token = Column('reset_token', String(250), nullable=True)

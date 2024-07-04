#!/usr/bin/env python3

"""
This module provides functions for hashing
and validating passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.

    """
    byte_password = bytes(password, 'utf-8')
    return bcrypt.hashpw(byte_password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if the given password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to be checked.

    Returns:
        bool: True if the password is valid, False otherwise.

    """
    byte_password = bytes(password, 'utf-8')
    return bcrypt.checkpw(byte_password, hashed_password)

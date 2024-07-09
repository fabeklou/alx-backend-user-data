#!/usr/bin/env python3

"""
This module provides the BasicAuth class which is a subclass of Auth.
It handles basic authentication for the API.
"""

import base64
import binascii
from api.v1.auth.auth import Auth


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

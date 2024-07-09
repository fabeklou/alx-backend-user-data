#!/usr/bin/env python3

"""
This module provides the BasicAuth class which is a subclass of Auth.
It handles basic authentication for the API.
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth is a subclass of Auth.
    It handles basic authentication for the API.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        prefix = 'Basic '
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith(prefix):
            return None
        return authorization_header[len(prefix):]

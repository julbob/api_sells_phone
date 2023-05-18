"""
This module contains function to verify the authentication of users.
"""

from base64 import b64decode
from functools import wraps
from binascii import Error as binError
from typing import Any
from flask import Response, make_response, request

def mock_check_user(username: str, password: str):
    """This function is mock to check the username and password for authentification API."""

    return username == "admin" and password == "admin"

def authenticate():
    """
    This function is called as a decorator in all route which need an authentication.
    """

    def wrapper(function):
        @wraps(function)
        def decorator(*args, **kwargs):
            res: Response | Any
            username: str
            password: str
            decode_token: bytes
            header_auth: str
            if "Authorization" in request.headers:
                header_auth = request.headers["Authorization"]

                if header_auth.startswith("Basic "):
                    try:
                        decode_token = b64decode(header_auth.split()[1])
                    except binError:
                        res = make_response("Error during decode token", 400)
                    else:
                        username, password = decode_token.decode().split(":")
                        if mock_check_user(username, password):
                            res = function(*args, **kwargs)
                        else:
                            res = make_response("Wrong username/password", 401)
                else:
                    res = make_response(
                        "The header Authorization not used the correct method of authentication",
                        401,
                    )
            else:
                res = make_response("Header Authorization missing", 401)
            return res

        return decorator

    return wrapper

#!/usr/bin/env python3
""" Basic auth
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        
        # check if path is in excluded_paths
        # allowing * at the end of excluded paths
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None

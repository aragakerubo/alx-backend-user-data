#!/usr/bin/env python3
"""
Auth module that handles the authentication
"""
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
import bcrypt

from db import DB
from user import User


def _hash_password(password: str) -> str:
    """Hashes a password

    Args:
        password (str): password to hash

    Returns:
        str: hashed password
    """
    return bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user

        Args:
            email (str): email of the user
            password (str): password of the user

        Returns:
            User: User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

#!/usr/bin/env python3
"""
Auth module that handles the authentication
"""
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
import bcrypt
import uuid

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


def _generate_uuid() -> str:
    """Generates a UUID

    Returns:
        str: UUID
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a login

        Args:
            email (str): email of the user
            password (str): password of the user

        Returns:
            bool: True if the password is correct, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session

        Args:
            email (str): email of the user

        Returns:
            str: session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """Gets a user from a session ID

        Args:
            session_id (str): session ID

        Returns:
            TypeVar('User'): User object
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

#!/usr/bin/env python3
"""
Encrypting passwords before storing them in the database
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypting passwords before storing them in the database

    Args:
        password (str): password to encrypt

    Returns:
        bytes: encrypted password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password is valid

    Args:
        hashed_password (bytes): encrypted password
        password (str): password to check

    Returns:
        bool: True if password is valid, False otherwise"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

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

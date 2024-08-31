#!/usr/bin/env python3
"""
This module contains a method that returns the obfuscated
password and the obfuscated email
"""
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """
    Returns the log message obfuscated

    Args:
        fields (List[str]): fields to obfuscate
        redaction (str): the obfuscated string
        message (str): the log message
        separator (str): the separator

    Returns:
        str: the obfuscated log message
    """
    for field in fields:
        message = re.sub(rf'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message

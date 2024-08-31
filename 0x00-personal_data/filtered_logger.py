#!/usr/bin/env python3
"""
This module contains a method that returns the obfuscated
password and the obfuscated email
"""
import re
from typing import List
import logging
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor method
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the record
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


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


def get_logger() -> logging.Logger:
    """
    Returns a logging object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database
    """
    return mysql.connector.connect(
        host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME'),
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD'),
    )


def main() -> None:
    """
    Main function
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    logger = get_logger()
    columns = [i[0] for i in cursor.description]
    for row in cursor:
        logger.info("; ".join(
            [f"{columns[i]}={row[i]}" for i in range(len(columns))]
            ) + ";")
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()

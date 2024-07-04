#!/usr/bin/env python3

"""
filtered_logger module

This module provides functionality for logging and filtering
sensitive user data.
It contains functions for redacting sensitive data in log messages,
setting up a logger, retrieving and logging user data from a database.

Author: [Fabrice Eklou]
"""

import logging
from typing import List, Tuple
import re
import mysql.connector
import os


PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replace sensitive data in a message with a redaction string.

    Args:
        fields (List[str]): List of sensitive fields to be redacted.
        redaction (str): The string to be used for redaction.
        message (str): The message containing sensitive data.
        separator (str): The separator used to separate field-value pairs.

    Returns:
        str: The message with sensitive data redacted.
    """
    for field in fields:
        message = re.sub(pattern='{}=.*?{}'.format(field, separator),
                         repl='{}={}{}'.format(field, redaction, separator),
                         string=message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes a RedactingFormatter object.

        Args:
            fields (List[str]): A list of field names to be redacted.

        Returns:
            None
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record by filtering sensitive data.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record with sensitive data filtered.

        """
        record.msg = filter_datum(self.__fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Get a logger instance for logging user data.

    Returns:
        logging.Logger: The logger instance.
    """
    user_data_logger = logging.getLogger('user_data')
    user_data_logger.setLevel(logging.INFO)
    user_data_logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_data_logger.addHandler(handler)

    return user_data_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Get a connection to the database.

    Returns:
        mysql.connector.connection.MySQLConnection:
            The database connection.
    """
    USERNAME = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    PASSWORD = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    HOST = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    DATABASE = os.environ.get('PERSONAL_DATA_DB_NAME')

    config = {
        'user': USERNAME,
        'password': PASSWORD,
        'host': HOST,
        'database': DATABASE
    }

    connection = mysql.connector.connect(**config)
    return connection


def main() -> None:
    """
    Main function to retrieve and log user data from the database.
    """
    connection = get_db()

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users;')
        log_rows = cursor.fetchall()
        fields = ('name', 'email', 'phone', 'ssn',
                  'password', 'ip', 'last_login', 'user_agent')
        for log_row in log_rows:
            field_value = zip(fields, log_row)
            message = ' '.join(
                ['{}={};'.format(field, value)
                 for field, value in field_value])
            logger = logging.LogRecord('user_data', logging.INFO, None, None,
                                       message, None, None)
            print(RedactingFormatter(PII_FIELDS).format(logger))
        cursor.close()
    connection.close()


if __name__ == '__main__':
    main()

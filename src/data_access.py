#!/usr/bin/env python3

import logging
import sqlite3
import sys
from os.path import expanduser

from src import message, platform_finder

logging.basicConfig(level=logging.INFO)


def fetch_db_data(db, command) -> list:
    """Send queries to the sqlite database and return the results.

    :param db: the path to the database
    :param command: the SQL command
    :return: data from the database
    """
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(command)
        return cur.fetchall()
    except Exception as e:
        sys.exit(f"Error reading the database: {e}")


# noinspection PyMethodMayBeStatic
class DataAccess:
    SQL_CMD = (
        "SELECT "
        "text, "
        "datetime((date / 1000000000) + 978307200, 'unixepoch', 'localtime'),"
        "handle.id, "
        "handle.service, "
        "message.destination_caller_id, "
        "message.is_from_me, "
        "message.attributedBody, "
        "message.cache_has_attachments "
        "FROM message "
        "JOIN handle on message.handle_id=handle.ROWID "
        " WHERE datetime((date / 1000000000) + 978307200, 'unixepoch', 'localtime') > '2024-05-11'"
    )

    def __init__(self, db_path: str, system=None):
        self.db_path = db_path
        if system is None:
            self.operating_system = platform_finder.get_platform()

    def _check_supported_os(self):
        if self.operating_system == "WINDOWS":
            sys.exit(f"{platform_finder.get_platform()} is not supported")

    def _read_database(self) -> list[message.Message] | None:
        data = []
        for row in fetch_db_data(self.db_path, self.SQL_CMD):
            text = self._parse_text(row)

            data.append(message.Message(row[2], text, row[1], row[3], row[4], row[5]))

        return data

    def _parse_text(self, row):
        text = row[0]

        if row[7] == 1:
            text = "<ATTACHMENT>"

        if text is None and row[6] is not None:
            # the chat.db has some weird behavior where sometimes the text value is None
            # and the text string is buried in a binary blob under the attributedBody field.
            try:
                text = row[6].split(b"NSString")[1]

                # stripping some preamble which generally looks like this: b'\x01\x94\x84\x01+'
                text = text[5:]

                # this 129 is b'\x81, python indexes byte strings as ints,
                # this is equivalent to text[0:1] == b'\x81'
                if text[0] == 129:
                    length = int.from_bytes(text[1:3], "little")
                    text = text[3 : length + 3]
                else:
                    length = text[0]
                    text = text[1 : length + 1]

                text = text.decode()
                logging.debug(text)
            except Exception as e:
                logging.debug(e)
                sys.exit(str(e))
        return text

    def fetch(self) -> list[message.Message] | None:
        self._check_supported_os()
        return self._read_database()

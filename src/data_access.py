#!/usr/bin/env python3

import logging
import sqlite3
import sys
from os.path import expanduser

from src import message, platform_finder

logging.basicConfig(level=logging.INFO)


# noinspection PyMethodMayBeStatic
class DataAccess:
    _QUERY = (
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

    def __init__(self, database: str):
        self._database = database
        self._os = platform_finder.get_platform()

    def fetch(self) -> list[message.Message] | None:
        self._check_supported_os()
        return self._read_database()

    def _check_supported_os(self):
        if self._os == "WINDOWS":
            sys.exit(f"{platform_finder.get_platform()} is not supported")

    def _do_fetch(self, command: str) -> list:
        try:
            conn = sqlite3.connect(self._database)
            cur = conn.cursor()
            cur.execute(command)
            return cur.fetchall()
        except Exception as e:
            sys.exit(f"Error reading the database: {e}")

    def _read_database(self) -> list[message.Message]:
        data = []
        for row in self._do_fetch(self._QUERY):
            content = self._parse_content(row)
            data.append(
                message.Message(
                    sender=row[2],
                    recipient=row[4],
                    is_from_me=bool(row[5]),
                    content=content,
                    sent_at=row[1],
                    service=row[3],
                )
            )
        return data

    def _parse_content(self, row):
        content = row[0]

        if row[7] == 1:
            content = "<ATTACHMENT>"

        if content is None and row[6] is not None:
            # the chat.db has some weird behavior where sometimes the text value is None
            # and the text string is buried in a binary blob under the attributedBody field.
            try:
                content = row[6].split(b"NSString")[1]

                # stripping some preamble which generally looks like this: b'\x01\x94\x84\x01+'
                content = content[5:]

                # this 129 is b'\x81, python indexes byte strings as ints,
                # this is equivalent to text[0:1] == b'\x81'
                if content[0] == 129:
                    length = int.from_bytes(content[1:3], "little")
                    content = content[3 : length + 3]
                else:
                    length = content[0]
                    content = content[1 : length + 1]

                content = content.decode()
                logging.debug(content)
            except Exception as e:
                logging.debug(e)
                sys.exit(str(e))
        return content

#!/usr/bin/env python3

import logging
import sqlite3
import sys
from datetime import datetime, UTC
from os.path import expanduser

from src import message, platform_finder

_logger = logging.getLogger(__name__)


class DataAccess:
    _QUERY = """
    SELECT
        m.text,
        datetime((m.date / 1000000000) + 978307200, 'unixepoch'),
        h.id,
        h.service,
        m.destination_caller_id,
        m.is_from_me,
        m.attributedBody,
        m.cache_has_attachments,
        m.rowid
    FROM message m
    JOIN handle h ON m.handle_id = h.ROWID
    """

    def __init__(self, database: str):
        self._database = database
        self._os = platform_finder.get_platform()

    def execute(self, command: str) -> list:
        try:
            conn = sqlite3.connect(self._database)
            cur = conn.cursor()
            cur.execute(command)
            return cur.fetchall()
        except Exception as e:
            sys.exit(f"Error reading the database: {e}")

    def fetch(
        self,
        start: str = None,
        end: str = None,
        limit: int = None,
        sender: str = None,
        recipient: str = None,
    ) -> list[message.Message] | None:
        query = self._build_query(start, end, limit, sender, recipient)
        return self._do_fetch(query)

    def _build_query(self, start, end, limit, sender, recipient):
        query = self._QUERY

        where = ""
        clauses = []

        if start:
            clauses.append(
                f"datetime((m.date / 1000000000) + 978307200, 'unixepoch', 'localtime') > '{start}'"
            )

        if end:
            clauses.append(
                f"datetime((m.date / 1000000000) + 978307200, 'unixepoch', 'localtime') < '{end}'"
            )

        if sender:
            clauses.append(f"h.id = '{sender}'")

        if recipient:
            clauses.append(f"m.destination_caller_id = '{recipient}'")

        if clauses:
            where += " WHERE "
            where += " AND ".join(clauses)

        if limit:
            where += f" LIMIT {limit}"

        return query + where

    def _do_fetch(self, query: str) -> list[message.Message]:
        data = []
        for row in self.execute(query):
            content = self._parse_content(row)
            data.append(
                message.Message(
                    id=row[8],
                    sender=row[2],
                    recipient=row[4],
                    is_from_me=bool(row[5]),
                    content=content,
                    sent_at=datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                    .replace(tzinfo=UTC)
                    .astimezone(),
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
                _logger.debug(content)
            except Exception as e:
                _logger.debug(e)
                sys.exit(str(e))
        return content

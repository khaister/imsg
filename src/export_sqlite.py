#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create a SQLite3 database containing iMessage data (user id, text, date, service)
Python 3.9+
Date created: April 30th, 2021
Date modified: August 28th, 2021
"""

import sqlite3


class SqliteExporter:
    def __init__(self, imessage_data: list, file_path: str):
        self.imessage_data = imessage_data
        self.file_path = file_path

    def export(self) -> str:
        """Create a SQLite3 database in the Desktop folder.
        Add user, text, date and service to the database.
        """
        database = self.file_path + "iMessage-Data.sqlite"

        conn = sqlite3.connect(database)
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS Messages")

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Messages (
                from_caller_id TEXT,
                to_caller_id TEXT,
                is_from_me INTEGER,
                content TEXT,
                sent_on TEXT,
                service TEXT
            )
            """
        )

        for data in self.imessage_data:
            cur.execute(
                """INSERT INTO Messages (from_caller_id, to_caller_id, is_from_me, content, sent_on, service)
                VALUES(?, ?, ?, ?, ?, ?)""",
                (
                    data.from_caller_id,
                    data.to_caller_id,
                    data.is_from_me,
                    data.content,
                    data.sent_on,
                    data.service,
                ),
            )

        conn.commit()
        cur.close()
        return database

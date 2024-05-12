#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

from src.message import Message


class SqliteExporter:
    def __init__(self, imessage_data: list, file_path: str):
        self.imessage_data = imessage_data
        self.file_path = file_path

    def export(self) -> str:
        database = self.file_path + "iMessage-Data.sqlite"

        conn = sqlite3.connect(database)
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS Messages")

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Messages (
                sender TEXT,
                recipient TEXT,
                is_from_me INTEGER,
                content TEXT,
                sent_at TEXT,
                service TEXT
            )
            """
        )

        for data in self.imessage_data:
            data: Message
            cur.execute(
                """INSERT INTO Messages (sender, recipient, is_from_me, content, sent_at, service)
                VALUES(?, ?, ?, ?, ?, ?)""",
                (
                    data.sender,
                    data.recipient,
                    data.is_from_me,
                    data.content,
                    data.sent_at,
                    data.service,
                ),
            )

        conn.commit()
        cur.close()
        return database

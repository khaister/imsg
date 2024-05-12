#!/usr/bin/env python3

from datetime import datetime
import csv


class CsvExporter:
    def __init__(self, messages: list, file_path: str):
        self._messages = messages
        self._file_path = file_path

    def export(self) -> str:
        filename = (
            f'{self._file_path}iMessage-Data_{datetime.now().strftime("%Y-%m-%d")}.csv'
        )
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            field = [
                "sender",
                "recipient",
                "is_from_me",
                "sent_at",
                "service",
                "content",
            ]
            writer.writerow(field)

            for message in self._messages:
                writer.writerow(
                    [
                        message.sender,
                        message.recipient,
                        str(message.is_from_me).lower(),
                        message.sent_at,
                        message.service,
                        repr(message.content),
                    ]
                )

        return filename

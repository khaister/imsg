#!/usr/bin/env python3

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    id: int
    sender: str
    recipient: str
    is_from_me: bool
    content: str | None
    sent_at: datetime
    service: str

    def __str__(self):
        return (
            f"<id: {self.id}, "
            f"sender: {self.sender}, "
            f"recipient: {self.recipient} "
            f"is_from_me: {self.is_from_me} "
            f"sent_at: {self.sent_at} "
            f"service: {self.service}>\n"
            f"{self.content}\n"
        )

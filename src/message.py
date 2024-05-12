#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class Message:
    sender: str
    recipient: str
    is_from_me: bool
    content: str | None
    sent_at: str
    service: str

    def __str__(self):
        return (
            f"<sender: {self.sender}, "
            f"recipient: {self.recipient} "
            f"is_from_me: {self.is_from_me} "
            f"timestamp: {self.sent_at} "
            f"service: {self.service}>\n"
            f"{self.content}\n"
        )

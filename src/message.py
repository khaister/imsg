#!/usr/bin/env python3

"""
Data Container
Python 3.9+
Author: niftycode
Modified by: -
Date created: February 19th, 2022
Date modified: -
"""

from dataclasses import dataclass


@dataclass
class Message:
    """This dataclass is the store for the data:
    user id, text, date, service and account (caller id).
    """

    from_caller_id: str
    content: str
    sent_on: str
    service: str
    to_caller_id: str
    is_from_me: int

    def __str__(self):
        """String representation

        :return: the representation of this object
        """
        return (
            f"from_caller_id:\t\t{self.from_caller_id}\n"
            f"to_caller_id:\t\t{self.to_caller_id}\n"
            f"is_from_me:\t\t{self.is_from_me}\n"
            f"sent_on:\t\t{self.sent_on}\n"
            f"service:\t\t{self.service}\n"
            f"\n"
            f"{self.content}\n"
        )

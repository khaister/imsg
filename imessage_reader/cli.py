#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cli.py
Entrypoint to the command line interface.
Python 3.9+
Date created: October 15th, 2020
Date modified: June 2nd, 2023
"""

import argparse
import os
import sys
from os.path import expanduser

from imessage_reader import data_access, info

# Path to the chat.db file on macOS
# Note: This path is used if the user does not specify a path.
MACOS_DB_PATH = expanduser("~") + "/Library/Messages/chat.db"


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A tool for reading iMessage data")

    parser.add_argument(
        "-f",
        "--chat-db",
        type=str,
        nargs="?",
        const=MACOS_DB_PATH,
        default=MACOS_DB_PATH,
        help="path to chat.db, default to ~/Library/Messages/chat.db",
    )

    parser.add_argument(
        "-e",
        "--export",
        nargs="?",
        default="nothing",
        help="output format ('e', 'excel', 's', 'sqlite', 'sqlite3')",
    )

    parser.add_argument(
        "-r", "--recipients", help="show message recipients", action="store_true"
    )

    parser.add_argument("-v", "--version", help="show version", action="store_true")

    return parser


def check(chat_db: str):
    if chat_db != MACOS_DB_PATH and os.path.isdir(chat_db):
        chat_db += "/chat.db"

    if not os.path.isfile(chat_db):
        sys.exit(f"{chat_db} is invalid")

    return chat_db


def evaluate(path: str, output: str, recipients: bool, version: bool):
    """Evaluate the given options and perform the appropriate actions.

    :param path: path to the chat.db file
    :param output: create an Excel/SQLite3 file
    :param recipients: recipients of the messages
    :param version: specify if the version of this program should be shown
    """
    data_fetcher = data_access.DataFetcher(path)

    if version:
        info.app_info()
        sys.exit()

    if recipients:
        data_fetcher.export("recipients")
        sys.exit()

    if output == "e" or output == "excel":
        data_fetcher.export("excel")
    elif output == "s" or output == "sqlite" or output == "sqlite3":
        data_fetcher.export("sqlite")
    else:
        data_fetcher.export("nothing")


def main():
    args = get_parser().parse_args()
    db_path = check(args.chat_db)
    print(f"Reading {db_path}")
    evaluate(db_path, args.export, args.recipients, args.version)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from os.path import expanduser

from imessage_reader import data_access, export_excel, export_sqlite, info

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
        default=None,
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
    if version:
        info.app_info()
        sys.exit()

    fetched_data = data_access.DataAccess(path).fetch()

    if recipients:
        recipients = [i.from_caller_id for i in fetched_data if not i.is_from_me]
        for recipient in recipients:
            print(recipient)
        sys.exit()

    if output in ["e", "excel"]:
        file_path = expanduser("~") + "/Documents/"
        filename = export_excel.ExcelExporter(data, file_path).export()
        print(f"\nSuccessfully created {filename}\n")
        sys.exit()

    if output in ["s", "sqlite", "sqlite3"]:
        file_path = expanduser("~") + "/Documents/"
        filename = export_sqlite.SqliteExporter(data, file_path).export()
        print(f"\nSuccessfully created {filename}\n")
        sys.exit()

    for data in fetched_data:
        print(data)


def main():
    args = get_parser().parse_args()
    db_path = check(args.chat_db)
    print(f"Reading {db_path}\n")
    evaluate(db_path, args.export, args.recipients, args.version)


if __name__ == "__main__":
    main()

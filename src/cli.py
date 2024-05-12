#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from os.path import expanduser

from src import data_access, export_excel, export_sqlite, version

# Default path to chat.db on macOS
MACOS_DB_PATH = expanduser("~") + "/Library/Messages/chat.db"


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A tool for reading iMessage data")

    parser.add_argument(
        "-f",
        "--database",
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
        help="export to file with format (one of: 'e', 'excel', 's', 'sqlite', 'sqlite3')",
    )

    parser.add_argument("-v", "--version", help="show version", action="store_true")

    return parser


def check(chat_db: str):
    if chat_db != MACOS_DB_PATH and os.path.isdir(chat_db):
        chat_db += "/chat.db"

    if not os.path.isfile(chat_db):
        sys.exit(f"{chat_db} is invalid")

    return chat_db


def evaluate(database: str, output: str):
    fetched_data = data_access.DataAccess(database).fetch()

    if output in ["e", "excel"]:
        file_path = expanduser("~") + "/Documents/"
        filename = export_excel.ExcelExporter(data, file_path).export()
        print(f"\nSuccessfully created {filename}\n")
        sys.exit()

    if output in ["s", "sqlite"]:
        file_path = expanduser("~") + "/Documents/"
        filename = export_sqlite.SqliteExporter(data, file_path).export()
        print(f"\nSuccessfully created {filename}\n")
        sys.exit()

    for data in fetched_data:
        print(data)


def main():
    args = get_parser().parse_args()
    if args.version:
        print(version.STABLE)
        sys.exit()

    database = check(args.database)
    print(f"Reading {database}\n")

    evaluate(database, args.export)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from os.path import expanduser

from src import data_access, export_excel, export_sqlite, version

# Default path to chat.db on macOS
MACOS_DB_PATH = expanduser("~") + "/Library/Messages/chat.db"


def get_parser():
    parser = argparse.ArgumentParser()
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
    parser.add_argument(
        "-s",
        "--start",
        nargs="?",
        default=None,
        help="start date, one of formats: 'YYYY-MM-DD HH:MM:SS', 'YYYY-MM-DD'",
    )
    parser.add_argument(
        "-u",
        "--end",
        nargs="?",
        default=None,
        help="end date, one of formats: 'YYYY-MM-DD HH:MM:SS', 'YYYY-MM-DD'",
    )
    parser.add_argument(
        "-l",
        "--limit",
        nargs="?",
        default=None,
        type=int,
        help="limit number of messages to read",
    )
    parser.add_argument(
        "-r", "--recipient", nargs="?", default=None, help="filter by recipient"
    )
    parser.add_argument(
        "-t", "--sender", nargs="?", default=None, help="filter by sender"
    )
    parser.add_argument("-v", "--version", help="show version", action="store_true")

    return parser


def check(database: str):
    if database != MACOS_DB_PATH and os.path.isdir(database):
        database += "/chat.db"

    if not os.path.isfile(database):
        sys.exit(f"{database} is invalid")

    return database


def evaluate(database: str, options):
    fetched_data = data_access.DataAccess(database).fetch(
        start=options.start,
        end=options.end,
        limit=options.limit,
        sender=options.sender,
        recipient=options.recipient,
    )

    output = options.export
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

    evaluate(database, args)


if __name__ == "__main__":
    main()

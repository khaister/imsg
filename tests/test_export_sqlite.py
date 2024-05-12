#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from os import scandir
from src.export_sqlite import SqliteExporter
from src.message import Message


@pytest.fixture()
def create_directory(tmpdir):
    directory = tmpdir.mkdir("sub/")
    yield directory


def message_data_one_row():
    message_data_list = [
        Message(
            from_caller_id="max.mustermann@icloud.com",
            content="Hello Max!",
            sent_on="2021-04-11 17:02:34",
            service="iMessage",
            to_caller_id="+01 555 17172",
            is_from_me=1,
        )
    ]
    return message_data_list


def test_export_sqlite(create_directory):
    db_file_path = create_directory + "/db-"
    test_database = SqliteExporter(message_data_one_row(), db_file_path)
    test_database.export()

    file_name = ""
    dir_entries = scandir(create_directory)
    for entry in dir_entries:
        if entry.is_file():
            file_name = entry.name

    expected_file_name = "db-" + "iMessage-Data.sqlite"

    assert len(create_directory.listdir()) == 1
    assert file_name == expected_file_name

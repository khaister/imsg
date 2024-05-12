#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from datetime import datetime, UTC
from os import scandir
from imessage_reader.export_excel import ExcelExporter
from imessage_reader.message import Message


@pytest.fixture()
def create_directory(tmpdir):
    directory = tmpdir.mkdir("sub/")
    yield directory


def message_data_one_row():
    message_data_list = [
        Message(
            user_id="max.mustermann@icloud.com",
            text="Hello!",
            date="2020-10-27 17:19:20",
            service="SMS",
            account="+01 555 17172",
            is_from_me=1,
        )
    ]
    return message_data_list


def test_export_excel(create_directory):
    excel_file_path = create_directory + "/sub"
    ew = ExcelExporter(message_data_one_row(), excel_file_path)
    ew.write_data()

    file_name = ""
    dir_entries = scandir(create_directory)
    for entry in dir_entries:
        if entry.is_file():
            file_name = entry.name

    expected_file_name = (
        "sub" + f'iMessage-Data_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
    )

    assert len(create_directory.listdir()) == 1
    assert file_name == expected_file_name

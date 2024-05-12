#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from datetime import datetime, UTC
from os import scandir
from src.export_excel import ExcelExporter
from src.message import Message


@pytest.fixture()
def create_directory(tmpdir):
    directory = tmpdir.mkdir("sub/")
    yield directory


def message_data_one_row():
    message_data_list = [
        Message(
            sender="max.mustermann@icloud.com",
            content="Hello!",
            sent_at="2020-10-27 17:19:20",
            service="SMS",
            recipient="+01 555 17172",
            is_from_me=True,
        )
    ]
    return message_data_list


def test_export_excel(create_directory):
    excel_file_path = create_directory + "/sub"
    ew = ExcelExporter(message_data_one_row(), excel_file_path)
    ew.export()

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

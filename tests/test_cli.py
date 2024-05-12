#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from src import cli


@pytest.fixture()
def create_parser():
    """
    Create a parser
    """
    parser = cli.get_parser()
    yield parser


def test_evaluate(create_parser):
    args_version = create_parser.parse_args(["--version"])
    args_recipients = create_parser.parse_args(["--recipients"])
    args_output = create_parser.parse_args(["--export"])

    assert args_version.version is True
    assert args_recipients.recipients is True
    assert args_output.export is None


def test_check_database_path(mocker):
    mocker.patch(
        "sys.argv",
        [
            "imessage_reader",
            "--chat-db",
            "/Users/johnappleseed/Documents",
            "--export",
            "excel",
        ],
    )

    args = cli.get_parser().parse_args()
    assert args.chat_db == "/Users/johnappleseed/Documents"
    assert args.export == "excel"
    assert args.recipients is False
    assert args.version is False

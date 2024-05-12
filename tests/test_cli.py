#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from src import cli


@pytest.fixture()
def create_parser():
    parser = cli.get_parser()
    yield parser


def test_evaluate(create_parser):
    args_version = create_parser.parse_args(["--version"])
    args_output = create_parser.parse_args(["--export"])

    assert args_version.version is True
    assert args_output.export is None


def test_check_database_path(mocker):
    mocker.patch(
        "sys.argv",
        [
            "imsg",
            "--database",
            "~/Library/Messages/chat.db",
            "--export",
            "excel",
        ],
    )

    args = cli.get_parser().parse_args()
    assert args.database == "~/Library/Messages/chat.db"
    assert args.export == "excel"
    assert not args.version

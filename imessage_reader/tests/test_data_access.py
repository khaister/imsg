#!/usr/bin/env python3

import os
import sqlite3
import pytest
from imessage_reader import data_access


data = data_access.DataAccess("/Users/bodo/Documents")


def test_fetch_data(mocker):
    mocker.patch(
        "imessage_reader.data_access.DataAccess.__init__",
        db_path="/Users/bodo/Documents",
        system=None,
    )
    input_path = data.db_path
    input_system = data.operating_system
    assert input_path == "/Users/bodo/Documents"
    assert not None


@pytest.fixture(scope="function")
def initialize_db(tmpdir):
    file = os.path.join(tmpdir.strpath, "test.db")
    conn = sqlite3.connect(file)
    cur = conn.cursor()

    cur.executescript(
        """
    DROP TABLE IF EXISTS handle;

    CREATE TABLE handle (
    ROWID   INTEGER UNIQUE,
    id      TEXT UNIQUE
    );
    """
    )

    cur.execute(
        """INSERT OR IGNORE INTO handle(ROWID, id)
        VALUES ( ?, ?)""",
        (8, "max@mustermann.de"),
    )

    conn.commit()

    yield file
    conn.close()


def test_fetch_db_data(initialize_db):
    sql_command = "SELECT ROWID, id from handle"
    rval = data_access.fetch_db_data(initialize_db, sql_command)
    assert isinstance(rval, object)
    assert rval == [(8, "max@mustermann.de")]

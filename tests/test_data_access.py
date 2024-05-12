#!/usr/bin/env python3

import os
import sqlite3
import pytest
from src import data_access


data = data_access.DataAccess("/Users/bodo/Documents")


def test_fetch_data(mocker):
    mocker.patch(
        "src.data_access.DataAccess.__init__",
        db_path="/Users/bodo/Documents",
        system=None,
    )
    input_path = data._database
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
    rval = data_access.DataAccess(initialize_db)._do_fetch(sql_command)
    assert isinstance(rval, object)
    assert rval == [(8, "max@mustermann.de")]

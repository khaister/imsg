# imsg

![](img/license.svg) ![](img/python.svg)

A utility for fetching data from iMessage on **macOS** (version 10.14 or above).

The following information is currently being read from the database:

* sender's or recipient's phone number or email address
* message's content
* timestamp
* service (iMessage or SMS)
* whether the message was sent by the iMessage account holder

## Overview

Messages (iMessage or SMS) and attachments are stored in `~/Library/Messages` on macOS. This directory contains a `chat.db` file, which is a SQLite3 database with two interesting tables: `handle` and `message`.

* The `handle` table contains the recipients (email address or phone number)
* The received messages are in the `message` table

## Requirements

* Python 3.12+
* [openpyxl](https://pypi.org/project/openpyxl/)
* [rich](https://rich.readthedocs.io/en/latest/)

## Install

    pip install imsg

## Usage

### CLI

> [!note]
> On **macOS** you need access to the *Library* folder in order to read `chat.db`. You can add access (for *Terminal* or *iTerm*) in
> System Preferences > Privacy & Security > Full Disk Access

```sh
usage: imsg [-h] [-f [DATABASE]] [-e [EXPORT]] [-v]

A tool for reading iMessage data

options:
  -h, --help            show this help message and exit
  -f [DATABASE], --database [DATABASE]
                        path to chat.db, default to ~/Library/Messages/chat.db
  -e [EXPORT], --export [EXPORT]
                        export to file with format (one of: 'e', 'excel', 's', 'sqlite', 'sqlite3')
  -v, --version         show version
```

### Library

`imsg` can be used in code as a library. For example:

```python
from imsg import data_access, message

DB_PATH = "/path/to/chat.db"

data: list[message.Message] = data_access.DataAccess(DB_PATH).fetch()
print(data)
```
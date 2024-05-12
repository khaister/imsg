# imsg

![](img/license-MIT-green.svg) ![](img/python-3.9-blue.svg)

A utility for fetching data from iMessage on **macOS** (version 10.14 or above).

The following information is currently being read from the database:

* user id (sender's or recipient's phone number or email address)
* message
* timestamp
* service (iMessage or SMS)
* account (destination caller id)
* is the message from self

## Overview

Received messages (iMessage or SMS) and attachments are stored in `~/Library/Messages`. This directory contains a `chat.db` file, which is a SQLite3 database file, containing two interesting tables: `handle` and `message`.

* The `handle` table contains the recipients (email address or phone number)
* The received messages are in the `message` table

## Requirements

* Python 3.12+
* [openpyxl](https://pypi.org/project/openpyxl/)

## Install

    pip install imsg

## CLI usage

### Specify no options

Start the program with:

    imsg

This will show you all users and messages in the Terminal. On macOS, if `-f` or `--database` is not specified on macOS, `chat.db` is assumed to be in `~/Library/Messages`

### Specify a path for `chat.db`

A different path to `chat.db` can be specified with the `-f` or `--database` option:

    imsg -f <PATH>

If the `-e` or `--export` option is not included, data is printed to standard output.

### Export data

You can create an Excel file containing users, messages, timestamp, and service. The file will be stored in `~/Documents`

    imsg -e e
    imsg --export e
    imsg --export excel

You can create a SQLite3 database containing users, messages, date and service (SMS or iMessage). The file will be stored in `~/Documents`

    imsg -e s
    imsg --export s
    imsg --export sqlite

> [!note]
> On **macOS** you need access to the *Library* folder in order to read `chat.db`. You can add access (for *Terminal* or *iTerm*) in
> System Preferences > Privacy & Security > Full Disk Access

## Library usage

`imsg` can be used in code as a library. For example:

```python
from imsg import data_access

DB_PATH = "/path/to/chat.db"

data = data_access.DataAccess(DB_PATH).fetch()
print(data)
```
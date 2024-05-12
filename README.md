# imessage_reader

![](img/license-MIT-green.svg) ![](img/python-3.9-blue.svg)

This is a forensic tool written in Python 3. Use this tool to fetch the content (phone numbers, email addresses, messages and the account) from the `chat.db` database file on **macOS** (version 10.14 or above).

The following information is currently being read from the database:

* user id (sender's or recipient's phone number or email address)
* message
* date and time
* service (iMessage or SMS)
* account (destination caller id)
* is the message from self

## Background

Received messages (iMessage or SMS) and attachments will be saved in "~/Library/Messages". This directory contains a `chat.db` file, which is a SQLite3 database file, with two tables of interest: `handle` and `message`. The `handle` table contains the recipients (email address or phone number). The received messages are in the `message` table.

## Requirements

* Python 3.9+
* openpyxl

To run tests install **pytest**:

    pip3 install pytest

## Install

    pip3 install imessage-reader

## CLI usage

### Specify no options

Start the program with:

    imessage_reader

This will show you all users and messages in the Terminal. If no option (`-p <PATH>`) is specified, the default directory (under macOS) is searched for the chat.db file.

### Specify a PATH as argument

A different path to chat.db file can be specified with the `-p` option:

    imessage_reader -p <PATH>

Unless the `-o` option is also used, the data is displayed in the terminal.

### Specify an output argument

You can create an Excel file containing users, messages, date and service (SMS or iMessage). The file will be stored in the
Documents folder:

    imessage_reader -o e

or

    imessage_reader -o excel

You can create a SQLite3 database containing users, messages, date and service (SMS or iMessage). The file will be stored in the Documents folder:

    imessage_reader -o s

or

    imessage_reader -o sqlite

If you only want to see a list of recipients use:

    imessage_reader -r

or

    imessage_reader --recipients

**Note**: On **macOS** you need access to the *Library* folder in order to read the iMessage database file ("chat.db"). You can add access (for *Terminal* or *iTerm*) in

    > System Preferences > Security & Privacy > Privacy > Full Disk Access

### Specify a PATH and an output argument

You can combine the `-p` with the `-o` option:

    imessage_reader -p /home/bodo/Downloads -o excel

In this example the chat.db file is located in the Downloads folder (on a Linux machine). And the Excel file will be created in the Documents folder.

## Library usage

To get the messages use following code:

    from imessage_reader import fetch_data

    DB_PATH = /path/to/chat.db

    # Create a FetchData instance
    fd = fetch_data.FetchData(DB_PATH)

    # Store messages in my_data
    # This is a list of tuples containing user id, message and service (iMessage or SMS)
    my_data = fd.get_messages()
    print(my_data)

## Changelog

See [CHANGELOG.rst](https://github.com/niftycode/imessage_reader/blob/master/CHANGELOG.rst)

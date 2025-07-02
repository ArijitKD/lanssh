# File: ./liblocal/dbops.py
#
# lanssh - SSH into LAN devices using just an alias for the remote host. No IPs required.
#
#
# Copyright (C) 2025-Present Arijit Kumar Das <arijitkdgit.official@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import json

from .errno import *
from .const import *
from . import dbck


errno: int = 0
errdesc: str = ""


def read_data() -> dict:
    f'''
    Returns the data from {DATABASE} as a JSON-formatted dictionary.
    '''
    global errno, errdesc
    db = open(DB_EXPAND)
    rawdata: str = db.read()
    db.close()
    data: dict = {}

    try:
        data = json.loads(rawdata)
    except json.decoder.JSONDecodeError:
        errdesc = f"Failed to parse data. Verify if {DATABASE}"\
        " has a valid JSON format."
        errno = ERR_JSON_DECODE_FAILED
        return {}

    if (dbck.check_db_format(data) != 0 or dbck.check_db_values(data) != 0):
        errno, errdesc = dbck.get_last_error()
        return {}

    return data


def write_data(jsondata: dict) -> None:
    '''
    Writes the JSON data to {DATABASE} as a string. Not implemented with
    errno and errdesc to get the stack trace in case json.dumps() crashes.
    '''
    stringdata: str = json.dumps(jsondata, indent=4)
    db = open(DB_EXPAND, "w")
    db.write(stringdata + "\n")
    db.close()


def get_last_error() -> tuple:
    '''
    Returns the most recent error as a tuple after resetting errno and errdesc.
    Tuple format: (errno, errdesc)
    '''
    global errdesc, errno
    last_errdesc: str = errdesc
    last_errno: int = errno
    if (errdesc != ""):
        errdesc = ""
    if (errno != 0):
        errno = 0
    return (last_errno, last_errdesc)

# File: ./liblocal/alias.py
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
from .dbck import *

global_last_errdesc = ""


def add(aliasname: str, mac: str) -> int:
    global global_last_errdesc
    db = open(DB_EXPAND)
    rawdata: str = db.read()
    db.close()
    data: dict = {}
    errcode: int = 0
    try:
        data = json.loads(rawdata)
        errcode = check_db_format(data)
        if (errcode != 0):
            return errcode
        errcode = check_db_values(data)
        if (errcode != 0):
            return errcode
    except json.decoder.JSONDecodeError:
        if (rawdata.strip() != ""):
            global_last_errdesc = f"Failed to parse data. Verify if {DATABASE}"\
            " has a valid JSON format."
            return ERR_JSON_DECODE_FAILED

    if (aliasname == ""):
        global_last_errdesc = f"Alias cannot be an empty string (\"\")."
        return ERR_ALIASNAME_EMPTY

    if (len(aliasname) > MAX_ALIASNAME_LENGTH):
        global_last_errdesc = f"Alias must not exceed {MAX_ALIASNAME_LENGTH} characters in length."
        return ERR_ALIASNAME_TOO_LONG

    if (MAC_PATTERN.fullmatch(mac) is None):
        global_last_errdesc = f"Invalid MAC address received: \"{mac}\"."
        return ERR_MAC_INVALID

    for alias_entry in data["aliases"]:
        if (alias_entry["name"] == aliasname):
            global_last_errdesc = f"Alias name \"{aliasname}\" already exists in database."
            return ERR_ALIAS_EXISTS

    data["aliases"].append({
        "name" : aliasname,
        "mac" : mac,
        "users": []
        })
    string_data: str = json.dumps(data, indent=4)
    db = open(DB_EXPAND, "w")
    db.write(string_data)
    db.close()

    return 0


def get_last_errdesc() -> str:
    '''
    Returns description of the most recent error and flushes the global error
    description variable, if non-empty, otherwise returns an empty string.
    '''
    global global_last_errdesc
    last_errdesc: str = global_last_errdesc
    if (global_last_errdesc != ""):
        global_last_errdesc = ""
    return last_errdesc


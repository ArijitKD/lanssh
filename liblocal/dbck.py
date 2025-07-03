# File: ./liblocal/dbck.py
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


from typing import List

from .errno import *
from .const import *

errno: int = 0
errdesc: str = ""


def check_db_format(json_data: dict) -> int:
    '''
    Checks if json_data has a valid format as recognized by the program
    '''
    global errdesc, errno
    checks: List[bool] = []
    checks.append(list(json_data.keys()) == ["aliases"])
    checks.append(checks[0] and type(json_data["aliases"]) == list)
    if (False in checks):
        errdesc = "Container \"aliases\" is either missing "\
        "or multiple unwanted containers\n"\
        f"present in {DATABASE}."
        errno = ERR_DB_FORMAT_INVALID
        return -1

    for i in range(len(json_data["aliases"])):
        checks.clear()
        alias: dict = json_data["aliases"][i]
        checks.append(type(alias) == dict)
        checks.append(alias != {})
        checks.append(checks[0] and set(alias.keys()) == {"name", "mac", "default_user"})
        if (False in checks):
            errdesc = f"Alias entry at index {[i]} has missing "\
            f"or invalid primary keys in \n{DATABASE}. Verify if \"name\", "\
            "\"mac\" and \"default_user\" are the only\nprimary keys "\
            "present for the given entry. Indexing starts from 0."
            errno = ERR_DB_FORMAT_INVALID
            return -1

    return 0


def check_db_values(json_data: dict) -> int:
    '''
    Assumes json_data has a valid format as recognized by the program.
    Checks if the value fields have correct datatypes and verifies
    integrity of MAC address format.
    '''
    global errdesc, errno
    checks: List[bool] = []
    
    for i in range(len(json_data["aliases"])):
        checks.clear()
        alias: dict = json_data["aliases"][i]
        checks.append(type(alias["name"]) == str)
        checks.append(type(alias["mac"]) == str)
        checks.append(type(alias["default_user"]) == str)

        if (False in checks):
            errdesc = f"Alias entry at index {[i]} has invalid "\
            f"datatype for primary keys in \n{DATABASE}. Verify if \"name\", "\
            "\"mac\" and \"default_user\" have\nvalid datatypes in the given entry. "\
            "Indexing starts from 0."
            errno = ERR_DATATYPE_INVALID
            return -1

        if (MAC_PATTERN.fullmatch(alias["mac"]) is None):
            errdesc = f"Alias entry at index {[i]} has an invalid "\
            f"MAC address in {DATABASE}.\nIndexing starts from 0.\n"\
            f"Helpful search string (cause of error): \"{alias['mac']}\""
            errno = ERR_MAC_INVALID
            return -1

        if (alias["name"] == ""):
            errdesc = f"Alias entry at index {[i]} has an empty value for "\
            f"the \"name\"\nprimary key in {DATABASE}. Indexing starts from 0."
            errno = ERR_ALIASNAME_EMPTY
            return -1

        if (alias["name"].find(" ") != -1):
            errdesc = f"Alias entry at index {[i]} has one or more whitespaces for "\
            f"the \"name\"\nprimary key in {DATABASE}. Indexing starts from 0."
            errno = ERR_ALIASNAME_HAS_SPACE
            return -1

        if (len(alias["name"]) > MAX_ALIASNAME_LENGTH):
            errdesc = f"Alias entry at index {[i]} has a value for "\
            f"the \"name\" primary key longer than the\nmaximum allowed ({MAX_ALIASNAME_LENGTH} "\
            f"characters) in {DATABASE}. Indexing starts from 0.\n"\
            f"Helpful search string (cause of error): \"{alias['name']}\""
            errno = ERR_ALIASNAME_TOO_LONG
            return -1

        if (alias["default_user"] == ""):
            errdesc = f"Alias entry at index {[i]} has an empty value for the "\
            f"\"default_user\"\nprimary key in {DATABASE}. Indexing starts from 0.\n"\
            f"Alias name is \"{alias['name']}\"."
            errno = ERR_USERNAME_EMPTY
            return -1

    return 0


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


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

global_last_errdesc = ""


def check_db_format(json_data: dict) -> int:
    '''
    Checks if json_data has a valid format as recognized by the program
    '''
    global global_last_errdesc
    checks: List[bool] = []
    checks.append(list(json_data.keys()) == ["aliases"])
    checks.append(checks[0] and type(json_data["aliases"]) == list)
    if (False in checks):
        global_last_errdesc = "Container \"aliases\" is either missing "\
        "or multiple unwanted containers\n"\
        f"present in {DATABASE}."
        return ERR_DB_FORMAT_INVALID

    for i in range(len(json_data["aliases"])):
        checks.clear()
        alias: dict = json_data["aliases"][i]
        checks.append(type(alias) == dict)
        checks.append(alias != {})
        checks.append(checks[0] and set(alias.keys()) == {"name", "mac", "users"})
        if (False in checks):
            global_last_errdesc = f"Alias entry at index {[i]} has missing"\
            f" or invalid primary keys in \n{DATABASE}. Verify if \"name\","\
            " \"mac\"and \"users\" are the only\nprimary keys present for"\
            " the given entry. Indexing starts from 0."
            return ERR_DB_FORMAT_INVALID

    return 0


def check_db_values(json_data: dict) -> int:
    '''
    Assumes json_data has a valid format as recognized by the program.
    Checks if the value fields have correct datatypes and verifies
    integrity of MAC address format.
    '''
    global global_last_errdesc
    checks: List[bool] = []
    
    for i in range(len(json_data["aliases"])):
        checks.clear()
        alias: dict = json_data["aliases"][i]
        checks.append(type(alias["name"]) == str)
        checks.append(type(alias["mac"]) == str)
        checks.append(type(alias["users"]) == list)

        if (checks[-1] and (alias["users"] != [])): # Ensure no error for empty users list
            checks.append(
                set(type(user) for user in alias["users"]) == {str}
                )

        if (False in checks):
            global_last_errdesc = f"Alias entry at index {[i]} has invalid"\
            f" datatype for primary keys in \n{DATABASE}. Verify if \"name\","\
            " \"mac\" and \"users\" have valid\ndatatypes in the given entry."\
            " Indexing starts from 0."
            return ERR_DATATYPE_INVALID

        if (MAC_PATTERN.fullmatch(alias["mac"]) is None):
            global_last_errdesc = f"Alias entry at index {[i]} has an invalid "\
            f"MAC address in {DATABASE}.\nIndexing starts from 0.\n"\
            f"Helpful search string (cause of error): \"{alias['mac']}\""
            return ERR_MAC_INVALID

        if (alias["name"] == ""):
            global_last_errdesc = f"Alias entry at index {[i]} has an empty value for "\
            f"the \"name\"\nprimary key in {DATABASE}. Indexing starts from 0."
            return ERR_ALIASNAME_EMPTY

        if (len(alias["name"]) > MAX_ALIASNAME_LENGTH):
            global_last_errdesc = f"Alias entry at index {[i]} has a value for "\
            f"the \"name\" primary key longer than the\nmaximum allowed ({MAX_ALIASNAME_LENGTH}"\
            f" characters) in {DATABASE}. Indexing starts from 0.\n"\
            f"Helpful search string (cause of error): \"{alias['name']}\""
            return ERR_ALIASNAME_TOO_LONG

        if ("" in alias["users"]):
            global_last_errdesc = f"Alias entry at index {[i]} has one or more empty values "\
            f"for the\n\"users\" primary key in {DATABASE}. Indexing starts from 0."
            return ERR_USERNAME_EMPTY

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


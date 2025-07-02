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


from . import dbops
from .errno import *
from .const import *

errno: int = 0
errdesc: str = ""


def add_alias(name: str, mac: str, default_user: str) -> int:
    global errdesc, errno
    data: dict = dbops.read_data()

    if (data == {}):
        errno, errdesc = dbops.get_last_error()
        return -1

    if (name == ""):
        errdesc = f"Alias cannot be an empty string (\"\")."
        errno = ERR_ALIASNAME_EMPTY
        return -1

    if (len(name) > MAX_ALIASNAME_LENGTH):
        errdesc = f"Alias must not exceed {MAX_ALIASNAME_LENGTH} characters in length."
        errno = ERR_ALIASNAME_TOO_LONG
        return -1

    if (MAC_PATTERN.fullmatch(mac) is None):
        errdesc = f"Invalid MAC address received: \"{mac}\"."
        errno = ERR_MAC_INVALID
        return -1

    if (default_user == ""):
        errdesc = f"Username cannot be empty."
        errno = ERR_USERNAME_EMPTY
        return -1

    for alias in data["aliases"]:
        if (alias["name"].lower() == name.lower()):
            errdesc = f"Alias \"{name}\" already exists in database."
            errno = ERR_ALIAS_EXISTS
            return -1
        if (alias["name"].find(" ") != -1):
            errdesc = f"Alias \"{name}\" has one or more whitespaces."
            errno = ERR_ALIASNAME_HAS_SPACE
            return -1

    data["aliases"].append(
        {
            "name" : name.lower(),
            "mac" : mac.lower(),
            "default_user": default_user
        }
    )
    dbops.write_data(data)
    return 0


def get_default_user(aliasname: str) -> list:
    '''
    Returns the default user for the given alias name.
    '''
    global errdesc, errno
    data: dict = dbops.read_data()
    default_user: str = ""

    if (data == {}):
        errno, errdesc = dbops.get_last_error()
        return ""

    aliases: list = data["aliases"]
    for alias in aliases:
        if (alias["name"].lower() == aliasname.lower()):
            default_user = alias["default_user"]
            break

    if (default_user == ""):
        errdesc = f"Alias \"{aliasname}\" does not exist in database."
        errno = ERR_ALIAS_NOT_FOUND

    return default_user


def get_mac(aliasname: str) -> str:
    '''
    Returns the host MAC address for the given alias name.
    '''
    global errdesc, errno
    data: dict = dbops.read_data()
    mac: str = ""

    if (data == {}):
        errno, errdesc = dbops.get_last_error()
        return ""

    aliases: list = data["aliases"]
    for alias in aliases:
        if (alias["name"].lower() == aliasname.lower()):
            mac = alias["mac"]
            break

    if (mac == ""):
        errdesc = f"Alias \"{aliasname}\" does not exist in database."
        errno = ERR_ALIAS_NOT_FOUND

    return mac.lower()


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


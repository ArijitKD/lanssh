# File: ./liblocal/misc.py
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


import os
import shutil
import platform

from .const import *
from .texts import *

def platform_supported() -> bool:
    return (platform.system().lower() in SUPPORTED_PLATFORMS)


def prereq_installed() -> bool:
    for req in ("ip", "ping"):
        if (not shutil.which(req)):
            return False
    return True


def mkdb() -> None:
    dbdir: str = os.path.dirname(DB_EXPAND)
    if (not os.path.isfile(DB_EXPAND)):
        os.makedirs(dbdir, exist_ok=True)
        db = open(DB_EXPAND, "w")
        db.write(
            "{\n"\
            "    \"aliases\": [\n"\
            "    ]\n"\
            "}\n"\
        )
        db.close()

    elif (os.path.isfile(DB_EXPAND) and
        os.path.getsize(DB_EXPAND) == 0):
        db = open(DB_EXPAND, "w")
        db.write(
            "{\n"\
            "    \"aliases\": [\n"\
            "    ]\n"\
            "}\n"\
        )
        db.close()


def rmdb() -> None:
    if (os.path.isfile(DB_EXPAND)):
        db = open(DB_EXPAND, "w")
        db.write(
            "{\n"\
            "    \"aliases\": [\n"\
            "    ]\n"\
            "}\n"\
        )
        db.close()


def show_help() -> None:
    print (HELP_TEXT)


def show_version() -> None:
    print (VERSION_TEXT)


def show_missing_dependency() -> None:
    print (MISSING_DEP_TEXT)


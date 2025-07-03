# File: ./liblocal/const.py
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


import re
import os

__cpu_count = os.cpu_count()

SUPPORTED_PLATFORMS = {
    "linux"
}

MULTIPROC_PCOUNT = __cpu_count if __cpu_count is not None else 5
VERSION = "1.5-beta"
DATABASE = "~/.lanssh/db.json"
DB_EXPAND = os.path.expanduser(DATABASE)
MAC_PATTERN = re.compile(r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})")
MAX_ALIASNAME_LENGTH = 16

VALID_OPTIONS = {
        "U"  : ("-u", "--user"),
        "AA" : ("-aa", "--add-alias"),
        "V"  : ("-v", "--version"),
        "L"  : ("-l", "--list"),
        "F"  : ("-f", "--format"),
        "H"  : ("-h", "--help"),
        "RA" : ("-ra", "--rm-alias"),
        "RD" : ("-rd", "--rmdb")
}

NO_ARGS_SPECIFIED       = 0
ARGS_PATTERN_1          = 1
ARGS_PATTERN_2          = 2
ARGS_PATTERN_3          = 3
ARGS_PATTERN_4          = 4
ARGS_PATTERN_5          = 5
ARGS_PATTERN_6          = 6
ARGS_PATTERN_7          = 7
ARGS_PATTERN_1_OPTIONAL = 11
ARGS_PATTERN_4_OPTIONAL = 14


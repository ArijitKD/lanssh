#!/usr/bin/python3

# File: ./liblocal/argsck.py
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


import sys

from .const import *


def check_valid_args_pattern() -> int:
    argv: list = sys.argv[1:]
    argc: int = len(argv)
    all_options = []
    _ = [
        (
            all_options.append(x[0]),
            all_options.append(x[1])
        ) for x in tuple(VALID_OPTIONS.values())
    ]
    for arg in argv:
        if ((arg.startswith("-") or arg.startswith("--")) and
            arg not in all_options):
            return -1

    if (argc == 0):
        return NO_ARGS_SPECIFIED

    if (argc == 1 and argv[0] not in all_options):
        return ARGS_PATTERN_1

    if (argc == 3 and (argv[1] in VALID_OPTIONS["U"])):
        return ARGS_PATTERN_1_OPTIONAL

    if (argc == 4 and argv[0] in VALID_OPTIONS["AA"]):
        return ARGS_PATTERN_2

    if (argc == 1 and argv[0] in VALID_OPTIONS["V"]):
        return ARGS_PATTERN_3

    if (argc == 1 and argv[0] in VALID_OPTIONS["L"]):
        return ARGS_PATTERN_4

    if (argc == 3 and argv[0] in VALID_OPTIONS["L"] and
        argv[1] in VALID_OPTIONS["F"]):
        return ARGS_PATTERN_4_OPTIONAL

    if (argc == 1 and argv[0] in VALID_OPTIONS["H"]):
        return ARGS_PATTERN_5

    if (argc == 2 and argv[0] in VALID_OPTIONS["RA"]):
        return ARGS_PATTERN_6

    if (argc == 1 and argv[0] in VALID_OPTIONS["RD"]):
        return ARGS_PATTERN_7

    return -1


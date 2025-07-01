# File: ./lanssh.py
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
import subprocess
import sys
import re
import multiprocessing
import os

import liblocal.argsck as argsck
import liblocal.dbck as dbck
import liblocal.alias as alias

from liblocal.errno import *
from liblocal.const import *
from liblocal.misc import *


def get_all_last_errdesc() -> None:
    '''
    Combines all error descriptions, seperates them with a newline where 
    applicable, and returns the entire thing as a single string.
    '''
    last_errdesc: str = ""
    all_errdescs: list = [
        alias.get_last_errdesc(),
        dbck.get_last_errdesc()
    ]
    for desc in all_errdescs:
        last_errdesc += desc
        if (desc != ""):
            last_errdesc += "\n"
    return last_errdesc.strip()


def is_ip_reachable(ip: str) -> bool:
    proc = subprocess.run(["ping", "-c", "1", "-W", "1", ip],
    stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, text = True)
    return (proc.returncode == 0)


def get_all_reachable_lan_devs() -> dict:
    proc = subprocess.run(["ip", "-4", "neigh", "show"],
    stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
    procresultlines: List[str] = list(filter(len, proc.stdout.split("\n")))
    lan_dev: dict = {}

    if (procresultlines == []):
        return {}

    for line in procresultlines:
        mac_match   = MAC_PATTERN.search(line)
        if (mac_match is not None):
            mac: str = mac_match.group(0)
            ip: str  = line.split()[0]
            lan_dev[mac] = ip

    with multiprocessing.Pool(processes = MULTIPROC_PCOUNT) as pool:
        all_macs: tuple = tuple(lan_dev.keys())
        all_ips: tuple = tuple(lan_dev.values())
        result = pool.map(is_ip_reachable, all_ips)
        for i in range(len(result)):
            if (not result[i]): lan_dev.pop(all_macs[i])

    return lan_dev


def main() -> None:
    argv: list = sys.argv[1:]
    argc: int = len(argv)

    argcode: int = argsck.check_valid_args_pattern()

    if (argcode in [NO_ARGS_SPECIFIED, ARGS_PATTERN_6]):
        if (argcode == NO_ARGS_SPECIFIED):
            print("lanssh: No options specified. Help is given below.")
        show_help()
        sys.exit(0)

    if (argcode == ERR_ARGS_INVALID):
        print(
            "lanssh: Invalid arguments or combination of arguments.\n"
            "Use lanssh -h to get help."
        )
        sys.exit(1)

    if (argcode == ARGS_PATTERN_4):
        show_version()
        sys.exit(0)

    if (not platform_supported()):
        print("lanssh: Unsupported platform. Currently only the following platforms are supported:")
        for platform in SUPPORTED_PLATFORMS:
            print (f"- {platform}")
        sys.exit(1)

    if (not prereq_installed()):
        show_missing_dependency()
        sys.exit(1)

    # Create the database file if it does not exist by calling mkdb()
    mkdb()

    if (argcode == ARGS_PATTERN_2):
        aliasname = argv[1]
        mac = argv[2]
        errcode = alias.add(aliasname, mac)
        if (errcode != 0):
            print (
                "lanssh: Error adding alias.\nError message:\n",
                get_all_last_errdesc(), sep = ""
                )
        sys.exit(1)

    reachable_devs: dict = get_all_reachable_lan_devs()

    if (reachable_devs == {}):
        print("No active devices on local network.")
        sys.exit(0)

    print("+" * NPLUS)
    print("|      Device MAC     |    IPv4 Address   |")
    print("+" * NPLUS)
    for dev in reachable_devs:
        print(f"|  {dev}  |  {reachable_devs[dev]}{' '*(17-len(reachable_devs[dev]))}|")
        print("+" * NPLUS)

if (__name__ == "__main__"):
    main()


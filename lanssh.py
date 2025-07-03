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
import liblocal.dbops as dbops

from liblocal.misc import *
from liblocal.errno import *
from liblocal.const import *


def get_last_error() -> tuple:
    '''
    Returns the most recent error from the modules that implement the function
    get_last_error(). Since the program is not multithreaded, only one
    get_last_error() from all modules at any given time will be non-empty. All
    others will be equal to (0, \"\"). This function must be updated if
    get_last_error() is implemented in any of the sub-modules in locallib/,
    specifically the local variable all_errors.
    '''
    all_errors: list = [
        alias.get_last_error(),
        dbck.get_last_error(),
        dbops.get_last_error()
    ]
    for error in all_errors:
        if (error != (0, "")):
            return error

    return (0, "")


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


def __exit(exitcode, suggest_help: bool = False) -> None:
    if (suggest_help):
        print("\nUse \"lanssh -h\" to get help.")
    sys.exit(exitcode)


def main() -> None:
    argv: list = sys.argv[1:]
    argc: int = len(argv)

    argcode: int = argsck.check_valid_args_pattern()

    if (argcode == -1):
        print("lanssh: Invalid arguments or combination of arguments.")
        __exit(1, suggest_help = True)

    if (argcode == NO_ARGS_SPECIFIED or argcode == ARGS_PATTERN_5):
        if (argcode == NO_ARGS_SPECIFIED):
            print("lanssh: No options specified. Help is given below.")
        show_help()
        __exit(0)

    if (argcode == ARGS_PATTERN_3):
        show_version()
        __exit(0)

    if (not platform_supported()):
        print(
            "lanssh: Unsupported platform. Currently only the following platforms are\n"
            "supported:"
        )
        for platform in SUPPORTED_PLATFORMS:
            print (f"  - {platform.capitalize()}")
        __exit(1, suggest_help = True)

    if (not prereq_installed()):
        show_missing_dependency()
        __exit(1, suggest_help = True)

    # Create the database file if it does not exist by calling mkdb()
    mkdb()

    reachable_hosts: dict = get_all_reachable_lan_devs()

    if (argcode == ARGS_PATTERN_1 or argcode == ARGS_PATTERN_1_OPTIONAL):
        aliasname: str = argv[0]
        user: str = ""

        if (argcode == ARGS_PATTERN_1):
            user = alias.get_default_user(aliasname)
        else:
            user = argv[2]

        if (user == "" and argcode == ARGS_PATTERN_1):
            error: tuple = get_last_error()
            print(
                f"lanssh: Error logging in (errorcode: {error[0]}).\n"
                f"Error message:\n{error[1]}"
            )
            __exit(1, suggest_help = True)

        elif (user == "" and argcode == ARGS_PATTERN_1_OPTIONAL):
            print(
                f"lanssh: Error logging in (errorcode: {ERR_USERNAME_EMPTY}).\n"
                "Error message:\nEmpty username received."
            )
            __exit(1, suggest_help = True)

        else:
            mac: str = alias.get_mac(aliasname)
            if (mac == ""):
                error = get_last_error()
                print(
                    f"lanssh: Error logging in (errorcode: {error[0]}).\n"
                    f"Error message:\n{error[1]}"
                )
                __exit(1, suggest_help = True)

            if (mac in reachable_hosts.keys()):
                ip: str = reachable_hosts[mac]
                print (
                    f"lanssh: Connecting to host {mac.upper()} a.k.a \"{aliasname}\" at\n"
                    f"{ip} as user \"{user}\"..."
                )

                ssh_retcode: int = 0
                try:
                    ssh_proc = subprocess.run(["ssh", f"{user}@{ip}"])
                    ssh_retcode = ssh_proc.returncode
                except KeyboardInterrupt:
                    print ("lanssh: Login interrupted by user.")
                    __exit(1)

                print (f"lanssh: Logged out user \"{user}\" from host \"{aliasname}\".")
                __exit(int(ssh_retcode != 0))

            else:
                print (f"lanssh: Host {mac.upper()} a.k.a \"{aliasname}\" is currently unreachable.")
                __exit(1)


    if (argcode == ARGS_PATTERN_2):
        aliasname: str = argv[1]
        mac: str = argv[2]
        default_user: str = argv[3]

        if (alias.add_alias(aliasname, mac, default_user) != 0):
            error: tuple = get_last_error()
            print(
                f"lanssh: Error adding alias (errorcode: {error[0]}).\n"
                f"Error message:\n{error[1]}"
            )
            __exit(1, suggest_help = True)
        else:
            print(f"lanssh: Alias \"{aliasname}\" added successfully.")
            __exit(0)

    if (argcode == ARGS_PATTERN_4 or argcode == ARGS_PATTERN_4_OPTIONAL):
        formatted_data: str = ""
        if (argcode == ARGS_PATTERN_4):
            formatted_data = dbops.get_formatted_data("table")
        else:
            data_format: str = argv[2]
            formatted_data = dbops.get_formatted_data(data_format)

        if (formatted_data == ""):
            error: tuple = get_last_error()
            print(
                f"lanssh: Error while displaying data (errorcode: {error[0]}).\n"
                f"Error message:\n{error[1]}"
            )
            __exit(1, suggest_help = True)
        else:
            print(formatted_data)
            __exit(0)

    if (argcode == ARGS_PATTERN_6):
        aliasname: str = argv[1]
        if (alias.rm_alias(aliasname) == 0):
            print(f"lanssh: Alias \"{aliasname}\" removed successfully.")
            __exit(0)
        else:
            error: tuple = get_last_error()
            print(
                f"lanssh: Error removing alias (errorcode: {error[0]}).\n"
                f"Error message:\n{error[1]}"
            )
            __exit(1, suggest_help = True)

    if (argcode == ARGS_PATTERN_7):
        rmdb()
        print("lanssh: Database cleared successfully.")
        __exit(0)
'''
    if (reachable_devs == {}):
        print("No active devices on local network.")
        sys.exit(0)

    print("+" * NPLUS)
    print("|      Device MAC     |    IPv4 Address   |")
    print("+" * NPLUS)
    for dev in reachable_devs:
        print(f"|  {dev}  |  {reachable_devs[dev]}{' '*(17-len(reachable_devs[dev]))}|")
        print("+" * NPLUS)
'''

if (__name__ == "__main__"):
    main()


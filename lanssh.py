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
import shutil
import platform
import os
import json


SUPPORTED_PLATFORMS = {
    "linux"
}
MULTIPROC_PCOUNT = 5
NPLUS = 43
VERSION = "1.0"
DATABASE = "~/.lanssh/db.json"
DB_EXPAND = os.path.expanduser(DATABASE)
MAC_PATTERN = re.compile(r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})")
MAX_ALIASNAME_LENGTH = 16

ERR_GENERIC            = -1
ERR_JSON_DECODE_FAILED = -2
ERR_DB_FORMAT_INVALID  = -3
ERR_MAC_INVALID        = -4
ERR_DATATYPE_INVALID   = -5
ERR_ALIASNAME_EMPTY    = -6
ERR_USERNAME_EMPTY     = -7
ERR_ALIASNAME_TOO_LONG = -8

global_last_errdesc = ""


def show_help() -> None:
    print (
        f"Help for lanssh (version {VERSION})\n"
        "\n"
        "lanssh: SSH into LAN devices simply using just an alias for the remote host.\n"
        "\n"
        "#1 Possible usage patterns:\n"
        "  1. lanssh <alias> [{-u | --user} <host-username>]\n"
        "  2. lanssh {-aa | --add-alias} <alias> <mac-address>\n"
        "  3. lanssh {-au | --add-user} <host-username> <alias>\n"
        "  4. lanssh {-v | --version}\n"
        "  5. lanssh {-l | --list} [{-f | --format} <format-type>]\n"
        "  6. lanssh [{-h | --help}]\n"
        "  7. lanssh {-ra | --rm-alias} <alias> <mac-address>\n"
        "  8. lanssh {-ru | --rm-user} <host-username> <alias>\n"
        "  9. lanssh {-rd | --rmdb}\n"
        "\n"
        "#2 Meanings of notations used above:\n"
        "  - <...>       :  A mandatory value for the preceding option. A\n"
        "                   value must not contain a space anywhere.\n"
        "\n"
        "  - {... | ...} :  A shorthand and full name for the same option.\n"
        "\n"
        "  - [...]       :  Non-mandatory options.\n"
        "\n"
        "## NOTE:\n"
        "  - From hereon, anywhere the word \"DB_EXPAND\" is encountered, it refers\n"
        "    to the file ~/.lanssh/db.json which contains all the host aliases along\n"
        "    with the associated MAC address and usernames in JSON format. Manually\n"
        "    editing this file is not recommended.\n"
        "\n"
        "  - \"data\" would then refer to the contents of ~/.lanssh/db.json.\n"
        "\n"
        "#3 Description of values:\n"
        "  - <alias>          :  A unique string denoting the host. Length must not\n"
        f"                        exceed {MAX_ALIASNAME_LENGTH} characters. Must not "
        "contain spaces. To\n"
        "                        avoid confusion, aliases are case-insensitive.\n"
        "\n"
        "  - <mac-address>    :  The MAC address of the host. Must be a static MAC.\n"
        "                        It is also case-insensitive as per conventions.\n"
        "\n"
        "  - <host-username>  :  The user to be logged in as to the remote host.\n"
        "                        Case-sensitive in nature for UNIX compatibility.\n"
        "\n"
        "  - <format-type>    :  The format type for displaying the stored information\n"
        "                        from the DB_EXPAND. Case-insensitive for convenience.\n"
        "                        More about supported formats in section #4 point (5).\n"
        "\n"
        "#4 Available options:\n"
        "  1. -aa, --add-alias  :  Add an alias for the given MAC address. Trying\n"
        "                          to add an existing alias will result in an error.\n"
        "                          If the DB_EXPAND is corrupted, will raise an error.\n"
        "                          See pattern (2) from section #1 for usage.\n"
        "\n"
        "  2. -au, --add-user   :  Add a username for logging in to the remote host.\n"
        "                          Multiple users for the same host maybe added, however\n"
        "                          trying to add an already existing username will raise\n"
        "                          an error. If the DB_EXPAND is corrupted, will raise an\n"
        "                          error. See pattern (3) from section #1 for usage.\n"
        "\n"
        "  3. -h, --help        :  Show this help section and exit. It is a non-mandatory\n"
        "                          option, since help section is always displayed when no\n"
        "                          options are specified.\n"
        "\n"
        "  4. -l, --list        :  Show the list of added host aliases along with the\n"
        "                          associated MAC address and usernames. If either -f or\n"
        "                          --format is specified, use the specified format (more\n"
        "                          in point 5). If not, display the data in tabular form.\n"
        "                          If the DB_EXPAND is missing, an appropriate message is\n"
        "                          displayed. If the DB_EXPAND is corrupted, will raise an\n"
        "                          error. See pattern (5) from section #1 for usage.\n"
        "\n"
        "  5. -f, --format      :  A non-mandatory option specifying the format of\n"
        "                          displaying the data. Currently supported values are:\n"
        "                            - json  : Display the data in JSON format.\n"
        "                            - table : Display the data in tabular form (default\n"
        "                                      when this option is unspecified).\n"
        "                          See pattern (5) from section #1 for usage.\n"
        "\n"
        "  6. -u, --user        :  SSH into the host <alias> as the specified user. It\n"
        "                          is a non-mandatory option. When unspecified, the first\n"
        "                          user in order of addition of usernames is selected.\n"
        "                          Specifying a non-existent for <alias> will raise an\n"
        "                          error. See pattern (1) from section #1 for usage.\n"
        "\n"
        "  7. -v, --version     :  Show version and copyright info, then exit.\n"
        "\n"
        "  8. -ra, --rm-alias   :  Remove an alias for the given MAC address. Trying\n"
        "                          to add a non-existent alias will result in an error.\n"
        "                          If the DB_EXPAND is corrupted, will raise an error.\n"
        "                          See pattern (7) from section #1 for usage.\n"
        "\n"
        "  9. -ru, --rm-user    :  Remove a username for logging in to the remote host.\n"
        "                          Trying to remove a non-existent username will raise\n"
        "                          an error. If the DB_EXPAND is corrupted, will raise an\n"
        "                          error. See pattern (8) from section #1 for usage.\n"
        "\n"
        "  10. -rd, --rmdb      :  Clear the DB_EXPAND file ~/.lanssh/db.json. Useful if\n"
        "                          manual correction of the file becomes impossible.\n"
        "\n"
        "## NOTE:\n"
        "  - If the DB_EXPAND file gets corrupted, and some options will raise an error.\n"
        "    In such cases, manual correction must be attempted at first, failing which\n"
        "    it must be removed.\n"
        "\n"
        "  - The DB_EXPAND file ~/.lanssh/db.json follows the JSON format given below:\n"
        "    {\n"
        "        \"aliases\": [\n"
        "            {\n"
        "                \"name\": \"<alias-1>\",\n"
        "                \"mac\": \"<mac-address-1>\",\n"
        "                \"users\": [\n"
        "                    \"<alias-1_user-1>\",\n"
        "                    \"<alias-1_user-2>\",\n"
        "                    .\n"
        "                    .\n"
        "                    .\n"
        "                    \"<alias-1_user-n>\"\n"
        "                ]\n"
        "            }\n"
        "            .\n"
        "            .\n"
        "            .\n"
        "            {\n"
        "                \"name\": \"<alias-n>\",\n"
        "                \"mac\": \"<mac-address-n>\",\n"
        "                \"users\": [\n"
        "                    \"<alias-n_user-1>\",\n"
        "                    \"<alias-n_user-2>\",\n"
        "                    .\n"
        "                    .\n"
        "                    .\n"
        "                    \"<alias-n_user-n>\"\n"
        "                ]\n"
        "            }\n"
        "        ]\n"
        "    }\n"
    )


def show_version() -> None:
    print (
        f"lanssh {VERSION}\n"
        "Copyright (c) 2025-Present Arijit Kumar Das <arijitkdgit.official@gmail.com>\n"
        "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\n"
        "This program is free software; you may redistribute it under the terms of\n"
        "the GNU General Public License version 3 or later.\n"
        "This program has absolutely no warranty."
    )


def show_missing_dependency() -> None:
    print (
        "lanssh: A required program was not found on your system.\n"
        "Required programs are: ip, ping\n"
        "Make sure these packages are installed:\n"
        "- iputils-ping (on Debian/Ubuntu), or iputils (on Arch/RHEL/Fedora)\n"
        "- iproute2 (on Debian/Ubuntu/Arch), or iproute (on RHEL/Fedora)\n"
        "Please note that package name may vary based on your distro repository upstream."
    )


def prereq_installed() -> bool:
    for req in ("ip", "ping"):
        if (not shutil.which(req)):
            return False
    return True


def platform_supported() -> bool:
    return (platform.system().lower() in SUPPORTED_PLATFORMS)


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


def mk_dbdir() -> None:
    dbdir: str = os.path.dirname(DB_EXPAND)
    if (not os.path.isdir(dbdir)):
        os.mkdir(dbdir)


def check_db_format(json_data: dict) -> int:
    '''
    Checks if json_data has a valid format as recognized by the program
    '''
    global global_last_errdesc
    checks: List[bool] = []
    checks.append(list(json_data.keys()) == ["aliases"])
    checks.append(checks[0] and type(json_data["aliases"]) == list)
    checks.append(checks[0] and json_data["aliases"] != [])
    if (False in checks):
        global_last_errdesc = "Container \"aliases\" is either missing "\
        "or empty, or multiple unwanted containers\n"\
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


def add_alias(alias: str, mac: str) -> int:
    global global_last_errdesc
    mk_dbdir()
    db = open(DB_EXPAND, "a+")
    db.seek(0)
    rawdata: str = db.read()
    data: dict = {}
    errcode: int = 0
    try:
        data = json.loads(rawdata)
        errcode = check_db_format(data)
        if (errcode != 0):
            db.close()
            return errcode
        errcode = check_db_values(data)
        if (errcode != 0):
            db.close()
            return errcode
    except json.decoder.JSONDecodeError:
        if (rawdata.strip() != ""):
            db.close()
            global_last_errdesc = f"Failed to parse data. Verify if {DATABASE}"\
            " has a valid JSON format."
            return ERR_JSON_DECODE_FAILED

    if (alias== ""):
        global_last_errdesc = f"Alias cannot be an empty string (\"\")."
        return ERR_ALIASNAME_EMPTY

    if (len(alias) > MAX_ALIASNAME_LENGTH):
        global_last_errdesc = f"Alias must not exceed {MAX_ALIASNAME_LENGTH} characters in length."
        return ERR_ALIASNAME_TOO_LONG

    if (MAC_PATTERN.fullmatch(mac) is None):
        global_last_errdesc = f"Invalid MAC address received: \"{mac}\"."
        return ERR_MAC_INVALID

    data["alias"].append({
        "name" : alias,
        "mac" : mac,
        })
    string_data: str = json.dumps(data, indent=4)
    db.close()
    return 0


def get_args() -> dict:
    pass

def main() -> None:
    argc: int = len(sys.argv)
       
    if ((argc > 1) and (sys.argv[1] in
    ("--help", "-h"))):
        show_help()
        sys.exit(0)

    if (not platform_supported()):
        print("lanssh: Unsupported platform. Currently only the following platforms are supported:")
        for platform in SUPPORTED_PLATFORMS:
            print (f"- {platform}")
        sys.exit(1)

    if (not prereq_installed()):
        show_missing_dependency()
        sys.exit(1)

    if (add_alias("087777777777777777777777", "0") != 0):
        print (
            "lanssh: Error adding alias.\nError message:\n",
            global_last_errdesc, sep = ""
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


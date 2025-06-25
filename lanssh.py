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


SUPPORTED_PLATFORMS = {
    "linux"
}
MULTIPROC_PCOUNT = 5
NPLUS = 43
VERSION = "1.0"


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
        "  - From hereon, anywhere the word \"database\" is encountered, it refers\n"
        "    to the file ~/.lanssh/db.json which contains all the host aliases along\n"
        "    with the associated MAC address and usernames in JSON format. Manually\n"
        "    editing this file is not recommended.\n"
        "\n"
        "  - \"data\" would then refer to the contents of ~/.lanssh/db.json.\n"
        "\n"
        "#3 Description of values:\n"
        "  - <alias>          :  A unique string denoting the host. Length must not\n"
        "                        exceed 16 characters. Must not contain spaces. To\n"
        "                        avoid confusion, aliases are case-insensitive.\n"
        "\n"
        "  - <mac-address>    :  The MAC address of the host. Must be a static MAC.\n"
        "                        It is also case-insensitive as per conventions.\n"
        "\n"
        "  - <host-username>  :  The user to be logged in as to the remote host.\n"
        "                        Case-sensitive in nature for UNIX compatibility.\n"
        "\n"
        "  - <format-type>    :  The format type for displaying the stored information\n"
        "                        from the database. Case-insensitive for convenience.\n"
        "                        More about supported formats in section #4 point (5).\n"
        "\n"
        "#4 Available options:\n"
        "  1. -aa, --add-alias  :  Add an alias for the given MAC address. Trying\n"
        "                          to add an existing alias will result in an error.\n"
        "                          If the database is corrupted, will raise an error.\n"
        "                          See pattern (2) from section #1 for usage.\n"
        "\n"
        "  2. -au, --add-user   :  Add a username for logging in to the remote host.\n"
        "                          Multiple users for the same host maybe added, however\n"
        "                          trying to add an already existing username will raise\n"
        "                          an error. If the database is corrupted, will raise an\n"
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
        "                          If the database is missing, an appropriate message is\n"
        "                          displayed. If the database is corrupted, will raise an\n"
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
        "                          If the database is corrupted, will raise an error.\n"
        "                          See pattern (7) from section #1 for usage.\n"
        "\n"
        "  9. -ru, --rm-user    :  Remove a username for logging in to the remote host.\n"
        "                          Trying to remove a non-existent username will raise\n"
        "                          an error. If the database is corrupted, will raise an\n"
        "                          error. See pattern (8) from section #1 for usage.\n"
        "\n"
        "  10. -rd, --rmdb      :  Clear the database file ~/.lanssh/db.json. Useful if\n"
        "                          manual correction of the file becomes impossible.\n"
        "\n"
        "## NOTE:\n"
        "  - If the database file gets corrupted, and some options will raise an error.\n"
        "    In such cases, manual correction must be attempted at first, failing which\n"
        "    it must be removed.\n"
        "\n"
        "  - The database file ~/.lanssh/db.json follows the JSON format given below:\n"
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
        mac_pattern = re.compile(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")
        mac_match   = mac_pattern.search(line)
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


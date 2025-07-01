# File: ./liblocal/texts.py
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


from .const import *

HELP_TEXT = \
f'''Help for lanssh (version {VERSION})

lanssh: SSH into LAN devices simply using just an alias for the remote host.
'''\
'''
#1 Possible usage patterns:
  1. lanssh <alias> [{-u | --user} <host-username>]
  2. lanssh {-aa | --add-alias} <alias> <mac-address>
  3. lanssh {-au | --add-user} <host-username> <alias>
  4. lanssh {-v | --version}
  5. lanssh {-l | --list} [{-f | --format} <format-type>]
  6. lanssh [{-h | --help}]
  7. lanssh {-ra | --rm-alias} <alias> <mac-address>
  8. lanssh {-ru | --rm-user} <host-username> <alias>
  9. lanssh {-rd | --rmdb}

#2 Meanings of notations used above:
  - <...>       :  A mandatory value for the preceding option. A
                   value must not contain a space anywhere.

  - {... | ...} :  A shorthand and full name for the same option.

  - [...]       :  Non-mandatory options.
'''\
f'''
## NOTE:
  - From hereon, anywhere the word "database" is encountered, it refers
    to the file {DATABASE} which contains all the host aliases along
    with the associated MAC address and usernames in JSON format. Manually
    editing this file is not recommended, unless under specific circumstances.

  - "data" would then refer to the contents of {DATABASE}.

#3 Description of values:
  - <alias>          :  A unique string denoting the host. Length must not
                        exceed {MAX_ALIASNAME_LENGTH} characters. Must not contain spaces. To
                        avoid confusion, aliases are case-insensitive.

  - <mac-address>    :  The MAC address of the host. Must be a static MAC.
                        It is also case-insensitive as per conventions.

  - <host-username>  :  The user to be logged in as to the remote host.
                        Case-sensitive in nature for UNIX compatibility.

  - <format-type>    :  The format type for displaying the stored information
                        from the database. Case-insensitive for convenience.
                        More about supported formats in section #4 point (5).

#4 Available options:
  1. -aa, --add-alias  :  Add an alias for the given MAC address. Trying
                          to add an existing alias will result in an error.
                          If the database is corrupted, will raise an error.
                          See pattern (2) from section #1 for usage.

  2. -au, --add-user   :  Add a username for logging in to the remote host.
                          Multiple users for the same host maybe added, however
                          trying to add an already existing username will raise
                          an error. If the database is corrupted, will raise an
                          error. See pattern (3) from section #1 for usage.

  3. -h, --help        :  Show this help section and exit. It is a non-mandatory
                          option, since help section is always displayed when no
                          options are specified.

  4. -l, --list        :  Show the list of added host aliases along with the
                          associated MAC address and usernames. If either -f or
                          --format is specified, use the specified format (more
                          in point 5). If not, display the data in tabular form.
                          If the database is missing, an appropriate message is
                          displayed. If the database is corrupted, will raise an
                          error. See pattern (5) from section #1 for usage.

  5. -f, --format      :  A non-mandatory option specifying the format of
                          displaying the data. Currently supported values are:
                            - json  : Display the data in JSON format.
                            - table : Display the data in tabular form (default
                                      when this option is unspecified).
                          See pattern (5) from section #1 for usage.

  6. -u, --user        :  SSH into the host <alias> as the specified user. It
                          is a non-mandatory option. When unspecified, the first
                          user in order of addition of usernames is selected.
                          Specifying a non-existent for <alias> will raise an
                          error. See pattern (1) from section #1 for usage.

  7. -v, --version     :  Show version and copyright info, then exit.

  8. -ra, --rm-alias   :  Remove an alias for the given MAC address. Trying
                          to add a non-existent alias will result in an error.
                          If the database is corrupted, will raise an error.
                          See pattern (7) from section #1 for usage.

  9. -ru, --rm-user    :  Remove a username for logging in to the remote host.
                          Trying to remove a non-existent username will raise
                          an error. If the database is corrupted, will raise an
                          error. See pattern (8) from section #1 for usage.

  10. -rd, --rmdb      :  Clear the database file {DATABASE}. Useful if
                          manual correction of the file becomes impossible.

## NOTE:
  - If the database file gets corrupted, and some options will raise an error.
    In such cases, manual correction must be attempted at first, failing which
    it must be removed.

  - The database file {DATABASE} follows the JSON format given below:'''\
'''
    {
        "aliases": [
            {
                "name": "<alias-1>",
                "mac": "<mac-address-1>",
                "users": [
                    "<alias-1_user-1>",
                    "<alias-1_user-2>",
                    .
                    .
                    .
                    "<alias-1_user-n>"
                ]
            }
            .
            .
            .
            {
                "name": "<alias-n>",
                "mac": "<mac-address-n>",
                "users": [
                    "<alias-n_user-1>",
                    "<alias-n_user-2>",
                    .
                    .
                    .
                    "<alias-n_user-n>"
                ]
            }
        ]
    }'''

VERSION_TEXT = \
f'''lanssh {VERSION}
Copyright (c) 2025-Present Arijit Kumar Das <arijitkdgit.official@gmail.com>
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This program is free software; you may redistribute it under the terms of
the GNU General Public License version 3 or later.
This program has absolutely no warranty.'''

MISSING_DEP_TEXT = \
'''lanssh: A required program was not found on your system.
Required programs are: ip, ping
Make sure these packages are installed:
    - iputils-ping (on Debian/Ubuntu), or iputils (on Arch/RHEL/Fedora)
    - iproute2 (on Debian/Ubuntu/Arch), or iproute (on RHEL/Fedora)
Please note that package name may vary based on your distro repository upstream.'''


# File: ./liblocal/errno.py
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


ERR_GENERIC              = -1
ERR_JSON_DECODE_FAILED   = -2
ERR_DB_FORMAT_INVALID    = -3
ERR_MAC_INVALID          = -4
ERR_DATATYPE_INVALID     = -5
ERR_ALIASNAME_EMPTY      = -6
ERR_USERNAME_EMPTY       = -7
ERR_ALIASNAME_TOO_LONG   = -8
ERR_ALIAS_EXISTS         = -9
ERR_ALIASNAME_HAS_SPACE  = -10
ERR_ALIAS_NOT_FOUND      = -11
ERR_UNSUPPORTED_FORMAT   = -12


errno: int = 0
errdesc: str = ""


def get_last_error() -> tuple:
    '''
    Should be implemented by the importer of this module. Every call
    to this function must reset errno and errdesc, before returning
    their present values as a tuple (errno, errdesc).
    '''
    return (errno, errdesc)


# lanssh

`lanssh` is a command-line utility that allows you to SSH into local network (LAN) devices using simple aliases instead of IP addresses. It internally resolves the IP address using the MAC address associated with each alias, thus eliminating the need to remember or look up dynamic IP addresses of known hosts.

This tool is ideal for network setups involving devices such as Raspberry Pi boards, home servers, or other computers with dynamic IPs but static MAC addresses. `lanssh` wraps around OpenSSH (`ssh`) and simplifies the workflow for accessing LAN hosts.

---

## Features

- **Alias-based SSH login**: SSH into LAN hosts using predefined alias names instead of IP addresses.
- **MAC-to-IP resolution**: Resolves the IP of a host dynamically at runtime based on MAC address.
- **Persistent alias database**: Stores mappings in `~/.lanssh/db.json` for reuse across sessions.
- **Custom default user per host**: Specify a default user for each alias for ease of use.
- **Database management**: Add, remove, list aliases, and clear the entire database.
- **Static MAC reliance**: Works as long as the target device has a static MAC address.

---

## Platform Support

- Linux only. Tested on Debian-based distributions such as Ubuntu and Linux Mint.

---

## Installation

To install `lanssh` from a `.deb` package:

```bash
sudo dpkg -i lanssh_<version>.deb
```

This installs the core logic to `/usr/lib/lanssh/`, adds a symlink in `/usr/bin/`, and installs documentation to `/usr/share/doc/lanssh/`.

---

## Usage

### SSH into a device:
```bash
lanssh <alias> [-u <username>]
```

If the `-u` option is not specified, the default user saved during alias registration is used.

### Add a new alias:
```bash
lanssh --add-alias <alias> <mac-address> <default-user>
```

### Remove an alias:
```bash
lanssh --rm-alias <alias>
```

### Clear the database:
```bash
lanssh --rmdb
```

### List aliases:
```bash
lanssh --list [--format <table|json>]
```

### Get help:
```bash
lanssh --help
```

### Show version:
```bash
lanssh --version
```

---

## Database Format

Stored at `~/.lanssh/db.json`, the alias database follows this JSON structure:

```json
{
  "aliases": [
    {
      "name": "pi",
      "mac": "dc:a6:32:xx:xx:xx",
      "default_user": "pi"
    }
  ]
}
```

Manual editing is discouraged unless recovery is necessary.

---

## Dependencies

- Python 3.x
- `arp-scan` (used for MAC-to-IP mapping)
- OpenSSH client (`ssh`)

You can install the dependency using:

```bash
sudo apt install arp-scan
```

---

## Design Philosophy

`lanssh` follows the UNIX design philosophy:

- Each function and subroutine does exactly one job.
- No dynamic typing or duck-typing abuses — types are consistent and explicit.
- Functions are deterministic and side-effect free unless absolutely required.
- Errors are traceable and reported meaningfully.

This utility is meant to behave like a part of GNU coreutils — dependable, scriptable, and straightforward.

---

## License

This software is licensed under the GNU General Public License v3+.  
You may redistribute and/or modify it under the terms of the GPL.  
There is no warranty, express or implied.

For more details, see [LICENSE](./LICENSE).

---

## Author

**Arijit Kumar Das**  
Email: <arijitkdgit.official@gmail.com>

---

## Contribution

Contributions, bug reports, and suggestions are welcome. Please adhere to UNIX programming principles while contributing.

---

## Man Page

For a condensed and structured reference, see the manual page after installation:

```bash
man lanssh
```
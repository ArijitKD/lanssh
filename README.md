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

- Currently supports **Linux-based systems only**.

---

## Tested Systems

- Debian "Bookworm"
- Android 12 (Termux)

---

## Installation

Currently, installable packages are available for Debian-based disributions only. Manual installation is possible via `make` for others.

### Install via APT (Recommended)

You can install `lanssh` using the APT package manager from the official GitHub-hosted `stable` repository.

#### Step 1: Add the APT repository

- For **Termux**, run:

```bash
export TERMUX_ROOT="$HOME/../usr"
mkdir -p $TERMUX_ROOT/etc/apt/sources.list.d
echo "deb [trusted=yes arch=all] https://arijitkd.github.io/lanssh/packages/apt stable termux" | tee $TERMUX_ROOT/etc/apt/sources.list.d/lanssh.list
```

- For other **Debian-based distributions**, run:

```bash
echo "deb [trusted=yes arch=all] https://arijitkd.github.io/lanssh/packages/apt stable main" | sudo tee /etc/apt/sources.list.d/lanssh.list
```

> `trusted=yes` is used here because the repository is not signed with a GPG key.

#### Step 2: Update APT cache

- For **Termux**, run:

```bash
pkg update
```

- For other **Debian-based distributions**, run:

```bash
sudo apt update
```

#### Step 3: Install `lanssh`

- For **Termux**, run:

```bash
pkg install lanssh
```

- For other **Debian-based distributions**, run:

```bash
sudo apt install lanssh
```

---

### Installation from Releases

If you prefer, you can manually download and install the `.deb` package from the [Releases](https://github.com/ArijitKD/lanssh/releases) section of the GitHub repository.

#### Step 1: Download the `.deb` package

Visit: [https://github.com/ArijitKD/lanssh/releases](https://github.com/ArijitKD/lanssh/releases)  
Download the latest `.deb` file corresponding to your architecture (usually `amd64` for most systems).

#### Step 2: Install using `dpkg`

```bash
sudo dpkg -i lanssh_<version>_all.deb
```

> Replace `<version>` with the actual version number of the downloaded package.

#### Step 3: Fix dependencies (if required)

```bash
sudo apt install -f
```

---

### Manaul installation using `make` (for non-Debian-based systems)

#### Step 1: Get `make` and `git`

Install `make` and `git` if you don't have it already. Installation procedure may vary depending on your package manager. Consult your system documentation for guidance.

#### Step 2: Clone the repository

In your preferred workspace directory, run:

```bash
git clone https://github.com/ArijitKD/lanssh.git lanssh-main
```

#### Step 3: Install using `make`

Run as `root`:

```bash
cd lanssh-main
make install
```

#### Step 4 (optional): Uninstallation

To uninstall, assuming you are in the toplevel directory of the repository (`lanssh-main` as per above), run as `root`:

```bash
make uninstall
```

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

- python3
- iproute2
- iputils-ping
- openssh-client

For manual installation using `make`, ensure these packages are installed. Note that package name may differ by distro, and the actual programs required are:

- python3
- ip
- ping
- ssh

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

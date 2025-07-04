#!/usr/bin/make
#
# File: Makefile
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


PREFIX       ?= /usr
LIBDIR       := $(PREFIX)/lib/lanssh
BINDIR       := $(PREFIX)/bin
SCRIPT_PATH  := $(BINDIR)/lanssh
MAIN_SCRIPT  := $(LIBDIR)/lanssh.py
LOCAL_LIBSRC := src/liblocal
LOCAL_LIBDST := $(LIBDIR)/liblocal

.PHONY: all help install uninstall

all: help

help:
	@echo "Run as root"
	@echo "  - To install: make install"
	@echo "  - To uninstall: make uninstall"
	@echo "You can also specify PREFIX=<dir> to specify the top-level install directory."


install:
	@if [ "$$(id -u)" -ne 0 ]; then \
		echo "Please run 'make install' as root."; \
		exit 1; \
	fi

	@echo "Creating shell wrapper at: $(SCRIPT_PATH)"
	@echo '#!/bin/bash' 																				>  lanssh_temp
	@echo '#'																							>> lanssh_temp
	@echo '# File: lanssh'																				>> lanssh_temp
	@echo '#'																							>> lanssh_temp
	@echo '# lanssh - SSH into LAN devices using just an alias for the remote host. No IPs required.'	>> lanssh_temp
	@echo '#'																							>> lanssh_temp
	@echo '#'																							>> lanssh_temp
	@echo '# Copyright (C) 2025-Present Arijit Kumar Das <arijitkdgit.official@gmail.com>'				>> lanssh_temp
	@echo '#'																							>> lanssh_temp
	@echo '# License: GPLv3+'																			>> lanssh_temp
	@echo '#'																							>> lanssh_temp
	@echo 'exec /usr/bin/python3 $(MAIN_SCRIPT) "$$@"'													>> lanssh_temp
	@install -Dm755 lanssh_temp $(SCRIPT_PATH)
	@rm -f lanssh_temp

	@echo "Creating directory: $(LIBDIR)"
	@install -d $(LIBDIR)

	@echo "Copying main script to: $(MAIN_SCRIPT)"
	@install -Dm644 src/lanssh.py $(MAIN_SCRIPT)

	@echo "Copying liblocal to: $(LOCAL_LIBDST)"
	@rm -rf $(LOCAL_LIBDST)
	@mkdir -p $(LOCAL_LIBDST)
	@cp -r $(LOCAL_LIBSRC)/* $(LOCAL_LIBDST)/

	@echo "Installation successful."
	@echo "Run 'lanssh -h' to read the Help section."

uninstall:
	@if [ "$$(id -u)" -ne 0 ]; then \
		echo "Please run 'make uninstall' as root."; \
		exit 1; \
	fi

	@echo "Removing shell wrapper: $(SCRIPT_PATH)"
	@rm -f $(SCRIPT_PATH)

	@echo "Removing installed files from: $(LIBDIR)"
	@rm -rf $(LIBDIR)

	@echo "Uninstallation complete."


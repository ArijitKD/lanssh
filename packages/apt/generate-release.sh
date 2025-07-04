#!/bin/bash
set -e

do_hash() {
    HASH_NAME=$1
    HASH_CMD=$2
    echo "${HASH_NAME}:"
    for f in $(find -type f); do
        f=$(echo $f | cut -c3-) # remove ./ prefix
        if [ "$f" = "Release" ]; then
            continue
        fi
        echo " $(${HASH_CMD} ${f}  | cut -d" " -f1) $(wc -c $f)"
    done
}

cat << EOF
Origin: lanssh repository
Label: lanssh
Suite: stable
Codename: stable
Version: 1.0
Architectures: all
Components: main
Description: SSH into LAN devices using an alias instead of an IP
 lanssh allows quick SSH login to LAN devices by mapping aliases to
 MAC addresses and dynamically resolving the host’s current IP.
 It simplifies local SSH access for headless systems.
Date: $(date -Ru)
EOF
do_hash "MD5Sum" "md5sum"
do_hash "SHA1" "sha1sum"
do_hash "SHA256" "sha256sum"


#!/bin/bash
usage="$(basename "$0") [-h] file -- encrypt file with gpg

where:
    -h  show this help text"

if [ "$1" == "-h" ]; then
  echo "$usage"
  exit 0
fi

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "$usage" >&2
    exit 1
fi

get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

SECRETFILE=$1
SECRETABSPATH=$(get_abs_filename "$SECRETFILE")
SECRETFILEOUT="$SECRETABSPATH.gpg"
cd "$(dirname "$0")"
rm -rf /tmp/gnupg
mkdir -m 700 /tmp/gnupg
gpg --homedir /tmp/gnupg --import C3022F19-public.key
gpg -q --yes --encrypt --homedir /tmp/gnupg --trust-model always \
  --output $SECRETFILEOUT --recipient 9515E8E4 $SECRETABSPATH
rm -rf /tmp/gnupg

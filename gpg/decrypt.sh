#!/bin/bash
PASSWORD=$1
cd "$(dirname "$0")"
cd "../"
files=($(find -name "*" \( -name "*.gpg" \)))

for FILE in ${files[*]}; do
    echo "Extracting $FILE to ${FILE%.gpg}"
    gpg --passphrase $PASSWORD --batch -d -q --no-tty --yes \
      --output "${FILE%.gpg}" "$FILE"
done

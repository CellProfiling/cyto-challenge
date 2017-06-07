#!/bin/bash
#PASSWORD=$1
cd "$(dirname "$0")"
cd "../"
files=($(find -name "*" \( -name "*.gpg" \)))

for FILE in ${files[*]}; do
    echo "Extracting $FILE to ${FILE%.gpg}"
    echo $gpg_password | gpg --passphrase-fd 0 --batch --no-tty -q --yes -d \
      -o "${FILE%.gpg}" "$FILE"
done

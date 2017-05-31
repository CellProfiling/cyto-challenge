#!/bin/bash
PASSWORD=$1
for FILE in *.*.gpg; do
    echo "Extracting $FILE to ${FILE%.gpg}."
    gpg --passphrase $PASSWORD --batch -d -q --yes \
      --output "${FILE%.gpg}" "$FILE"
done

#!/bin/bash

FILE='/etc/shadow'

if [ -e "$FILE" ]; then
  echo "${FILE} exists."
else
  echo "${FILE} does not exist."
  
fi

if [ -w "$FILE" ]; then
  echo "You have permissions to edit ${FILE}"
else
  echo "You do NOT have permissions to edit ${FILE}"
fi

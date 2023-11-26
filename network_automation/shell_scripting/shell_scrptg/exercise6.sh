#!/bin/bash

read -p "Enter name of file or directory:" INPUT

if [ -f "$INPUT" ]; then
  echo "${INPUT} is a file."
elif [ -d "$INPUT" ]; then
  echo "${INPUT} is a directory."
else
  echo "${INPUT} is something else."
fi

ls -l $INPUT

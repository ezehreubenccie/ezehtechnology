#!/bin/bash

FILE=$1
if [ -f $FILE ]; then
 echo "This is a regular file."
 exit 0
elif [ -d $FILE ]; then
 echo "This is a directory."
 exit 1
else
 echo "This is another type of file."
 exit 2
fi

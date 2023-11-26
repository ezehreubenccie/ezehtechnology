#!/bin/sh

FOLDER=$1
#FILE_DEST=$2
LIST=$(ls exer*.sh)
mkdir $FOLDER
for ITEM in $LIST
do
 mv $ITEM $FOLDER/
done

#!/bin/bash

HOST=$1
ping -c 1 $HOST
RETURN_CODE=$?
if [ "$RETURN_CODE" -ne "0" ]
then
 echo "$HOST unreachable."
fi

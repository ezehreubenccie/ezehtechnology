#!/bin/bash

HOST=$1
ping -c 1 $HOST&&echo "$HOST reachable."

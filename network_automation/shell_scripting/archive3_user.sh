#!/bin/bash

# USER=$1 #The first parameter is the user

for USER in $@
do
 # echo "Executing script: $0"
 echo "Archiving user: $USER"

 # Lock the account
 passwd -l $USER

 # Create an archive of the home directory
 tar cf /archives/${USER}.tar.gz /home/${USER}
done

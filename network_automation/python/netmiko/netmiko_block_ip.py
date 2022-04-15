#!/usr/bin/env python3

#This script assumes there is a network object-group on all Cisco ASAs called 'grp..blacklist', and that the group is attached to the correct ACL/interface

#import all the modules we need
import sys
import os
import netmiko
from netmiko import ConnectHandler
print('imported modules')

#list of firewall devices to add the blacklist ip to
asa_list = ['10.1.1.1', '10.2.2.2', '10.3.3.3']

#Parameter 1 should always be the ip of the address to block (blacklist)
#check that we have enough parameters to continue (the ip addresses we need)
if len(sys.argv) < 1:
    sys.exit('ERROR: Please include parameters for the blacklist IP address')
param_1 = sys.argv[1]
print('checking params... param_1: ' + param_1)

#get the username/password information from local system environment variables
username = os.environ.get('CISCOUSERNAME', 'None')
password = os.environ.get('CISCOPASSWORD', 'None')
secret = password
print('getting access information from env variables')

#check that we have all of the environment variables we need
if (username == 'None') or (password == 'None'):
        sys.exit('ERROR: Login username/password not set in environment variables')


#start the main loop
for asa in asa_list:

    #create the ssh session using netmiko
    print('creating ssh connection to ' + asa)
    device = ConnectHandler(device_type='cisco_asa', ip=asa, username=username, password=password, secret=secret)
    print('established ssh connection to ' + asa)

    #preload our config changes into a single array
    config_commands = [
        'object network blacklist-' + param_1,
        'host ' + param_1,
        'object-group network grp..blacklist',
        'network-object object blacklist-' + param_1
    ]
    print('sending ASA command list to ' + asa)

    #send our Cisco-specific commands and dump the output to a variable
    output = device.send_config_set(config_commands)
    print('sent ASA command to ' + asa)

    #print the output
    print(output)

    #close the ssh session cleanly
    device.disconnect()
    print('closed ssh session')

print('finished on all firewall devices')

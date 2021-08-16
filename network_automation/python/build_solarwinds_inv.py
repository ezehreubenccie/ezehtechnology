#!/usr/bin/env python

from pprint import pprint


sw_inv_list = []
deviceName_list = []

# Read device names from file
with open('sw_device_names.txt') as f:
    deviceName_output = f.read()
#print(deviceName_output)

# Read device serial# from file
with open('solarwinds_inventory.txt') as f:
    sw_output = f.read()
#print(sw_output)


# Build device name list
for deviceName in deviceName_output.splitlines():
    deviceName_list.append(deviceName)
#pprint(deviceName_list)

# Print number of devices
#print('Solarwinds devices number: {}'.format(len(deviceName_list)))

# Build serial number list
for serial in sw_output.splitlines():
    sw_inv_list.append(serial)
#pprint(sw_inv_list)

# Print number of serial#
#print('Solarwinds inventory number: {}'.format(len(sw_inv_list)))

# Build dictionary from list with deviceName as key

sw_inv_dict = dict(zip(deviceName_list, sw_inv_list))
pprint(sw_inv_dict)

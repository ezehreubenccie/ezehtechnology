#!/usr/bin/env python

from pprint import pprint

sw_inv_list = []
swdeviceName_list = []
insg_inv_list = []
devicesNotInInsight = []

# Read device names from file
with open('sw_device_names.txt') as f:
    swdeviceName_output = f.read()

# Read device serial# from file
with open('solarwinds_inventory.txt') as f:
    sw_output = f.read()

# Read serial numbers from insight smartnet sheet
with open('insight_global_inventory.txt') as f:
    insg_output = f.read()

# Build device name list from solarwinds
for deviceName in swdeviceName_output.splitlines():
    swdeviceName_list.append(deviceName)

# Build serial number list from solarwinds
for serial in sw_output.splitlines():
    sw_inv_list.append(serial)

# Build serial number list from insight sheet
for serial in insg_output.splitlines():
    insg_inv_list.append(serial)

# Build dictionary/database from solarwinds list with deviceName as key
sw_inv_dict = dict(zip(sw_inv_list, swdeviceName_list))

# Convert solarwinds and insight serial#s lists to sets
sw_inv_set = set(sw_inv_list)
insg_inv_set = set(insg_inv_list)


# Compare serial#s from insight and solarwinds and extract unique serial#s
insgUnique_set = insg_inv_set.difference(sw_inv_set)
swUnique_set = sw_inv_set.difference(insg_inv_set)

# Convert unique serial sets to lists
insgUnique_list = list(insgUnique_set)
swUnique_list = list(swUnique_set)


# Reconcile unique serial#s with solarwinds database
for serial in swUnique_list:
    for key in sw_inv_dict.keys():
        if serial == key:
            device = sw_inv_dict[serial]
            devicesNotInInsight.append(device)

print('****These devices are in solarwinds but not in insight sheet.****')
pprint(devicesNotInInsight)
print()
print('****These devices are in insight sheet but not in solarwinds.****')
pprint(insgUnique_list)

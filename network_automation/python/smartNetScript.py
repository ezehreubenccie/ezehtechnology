#!/usr/bin/env python

from pprint import pprint


sw_inv_list = []
swdeviceName_list = []
insg_inv_list = []
devicesNotInInsight = []

# Read device names from file
with open('sw_device_names.txt') as f:
    swdeviceName_output = f.read()
#print(swdeviceName_output)

# Read device serial# from file
with open('solarwinds_inventory.txt') as f:
    sw_output = f.read()
#print(sw_output)

# Read serial numbers from insight smartnet sheet
with open('insight_global_inventory.txt') as f:
    insg_output = f.read()
#print(insg_output)


# Build device name list from solarwinds
for deviceName in swdeviceName_output.splitlines():
    swdeviceName_list.append(deviceName)
#pprint(swdeviceName_list)

# Print number of devices
#print('Solarwinds devices number: {}'.format(len(swdeviceName_list)))

# Build serial number list from solarwinds
for serial in sw_output.splitlines():
    sw_inv_list.append(serial)
#pprint(sw_inv_list)

# Print number of serial#s from solarwinds
#print('Solarwinds inventory number: {}'.format(len(sw_inv_list)))

# Build serial number list from insight sheet
for serial in insg_output.splitlines():
    insg_inv_list.append(serial)
#pprint(insg_inv_list)

# Print number of serial#s from insight sheet
#print('Insight global inventory number: {}'.format(len(insg_inv_list)))



# Build dictionary/database from solarwinds list with deviceName as key
sw_inv_dict = dict(zip(sw_inv_list, swdeviceName_list))
#print('****Solarwinds serial# and device name database****')
#pprint(sw_inv_dict)

# Convert solarwinds and insight serial#s lists to sets
sw_inv_set = set(sw_inv_list)
insg_inv_set = set(insg_inv_list)


# Compare serial#s from insight and solarwinds and extract unique serial#s
#print('****Insight global unique serials****')
insgUnique_set = insg_inv_set.difference(sw_inv_set)
#pprint(insgUnique_set)
#print(type(insgUnique_set))

#print('****Solarwinds unique serials****')
swUnique_set = sw_inv_set.difference(insg_inv_set)
#pprint(swUnique_set)
#print(type(swUnique_set))

# Convert unique serial sets to lists
insgUnique_list = list(insgUnique_set)
swUnique_list = list(swUnique_set)
#print('****Insight global unique serial# list****')
#pprint(insgUnique_list)
#print(type(insgUnique_list))
#print()
#print('****Solarwinds unique serial# list****')
#pprint(swUnique_list)
#print(type(swUnique_list))

#found = False
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

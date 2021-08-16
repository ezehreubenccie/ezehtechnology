#!/usr/bin/env python

from pprint import pprint

sw_inv_list = []
csco_inv_list = []
with open('solarwinds_inventory.txt') as f:
    sw_output = f.read()
#print(sw_output)

with open('cisco_my_devices_inventory.txt') as f:
    csco_output = f.read()
#print(csco_output)

for serial in sw_output.splitlines():
    sw_inv_list.append(serial)
#pprint(sw_inv_list)
print('Solarwinds inventory number: {}'.format(len(sw_inv_list)))

for serial in csco_output.splitlines():
    csco_inv_list.append(serial)
#pprint(csco_inv_list)
print('Cisco inventory number: {}'.format(len(csco_inv_list)))

# Convert lists to sets
sw_inv_set = set(sw_inv_list)
csco_inv_set = set(csco_inv_list)

print('****Cisco unique serials****')
pprint(csco_inv_set.difference(sw_inv_set))

print('****Solarwinds unique serials****')
pprint(sw_inv_set.difference(csco_inv_set))

#!/usr/bin/env python

from pprint import pprint

sw_inv_list = []
insg_inv_list = []
with open('solarwinds_inventory.txt') as f:
    sw_output = f.read()
#print(sw_output)

with open('insight_global_inventory.txt') as f:
    insg_output = f.read()
#print(insg_output)

for serial in sw_output.splitlines():
    sw_inv_list.append(serial)
#pprint(sw_inv_list)
print('Solarwinds inventory number: {}'.format(len(sw_inv_list)))

for serial in insg_output.splitlines():
    insg_inv_list.append(serial)
#pprint(insg_inv_list)
print('Insight global inventory number: {}'.format(len(insg_inv_list)))

# Convert lists to sets
sw_inv_set = set(sw_inv_list)
insg_inv_set = set(insg_inv_list)

print('****Insight global unique serials****')
pprint(insg_inv_set.difference(sw_inv_set))

print('****Solarwinds unique serials****')
pprint(sw_inv_set.difference(insg_inv_set))

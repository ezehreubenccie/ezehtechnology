#!/usr/bin/env python3

import re
from pprint import pprint

with open('show_vlan.txt') as f:
    show_vlan = f.read()

list2 = []
# Remove Unwanted lines
for line in show_vlan.splitlines():
    if ('enet' in line or '---' in line or 'VLAN' in line or 'tr' in line or
        'fdnet' in line or 'trnet' in line 'fddi' in line or 'fddi-default' in line or
        'token-ring-default' in line or 'fddinet-default' in line or 'trnet-default' in line):
        continue
    else:
        list2.append(line)
print(list2)
# Extract the vlan_id vlan_name string from list2
fields = []
pattern = re.compile(r'[0-9]+\s+\w+')
for line in list2:
    mo = pattern.search(line)
    if mo:
        fields.append(mo.group())


# Create a tuple and add to list3
list3 = []
for item in fields:
   field1 = item.split()[0]
   field2 = item.split()[1]
   list3.append((field1, field2))

pprint(list3)

#!/usr/bin/env python3

import re
from pprint import pprint

with open('show_vlan.txt') as f:
    show_vlan = f.read()

#list1 = output.splitlines()
list2 = []

# Remove unwanted lines
for line in show_vlan.splitlines():
    if 'enet' in line:
        continue
    if '---' in line:
        continue
    if 'VLAN' in line:
        continue
    if 'tr' in line:
        continue
    if 'fdnet' in line:
        continue
    if 'trnet' in line:
        continue
    if 'fddi' in line:
        continue
    if 'fddi-default' in line:
        continue
    if 'token-ring-default' in line:
        continue
    if 'fddinet-default' in line:
        continue
    if 'trnet-default' in line:
        continue
    else:
        list2.append(line)

# Extract vlan_id and vlan_name from list2
fields = []
pattern = re.compile(r'[0-9]+\s+\w+')
for line in list2:
    mo = pattern.search(line)
    if mo:
        fields.append(mo.group())



list3 = []
for item in fields:
   field1 = item.split()[0]
   field2 = item.split()[1]
   list3.append((field1, field2))

pprint(list3)

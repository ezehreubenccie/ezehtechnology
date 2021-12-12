#!/usr/bin/env python3

import re
from pprint import pprint

with open('show_vlan.txt') as f:
    output = f.read()

list1 = output.splitlines()
list2 = []

for line in list1:
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


fields = []
pattern = re.compile(r'[0-9]+\s+\w+')
for line in list2:
    mo = pattern.search(line)
    if mo:
        fields.append(mo.group())


tup1 = ()
list3 = []
for item in fields:
   field1 = item.split()[0]
   field2 = item.split()[1]
   tup1 = (field1, field2)
   list3.append(tup1)

pprint(list3)

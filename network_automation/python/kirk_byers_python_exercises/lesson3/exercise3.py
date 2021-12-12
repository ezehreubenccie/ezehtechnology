#!/usr/bin/env python3

import re

with open('show_lldp_neighbors_detail.txt') as f:
    lldp_nei = f.read()

list1 = []
pattern1 = re.compile(r'System Name:\s\w+')
pattern2 = re.compile(r'^Port id:\s\w+$')
found1, found2 = (False, False) 
for line in lldp_nei.splitlines():
    mo1 = pattern1.search(line)
    mo2 = pattern2.search(line)
    if mo1:
        found1 = True
        list1.append(line)
    if mo2:
        found2 = True
        list1.append(line)
    if found1 and found2:
        break

for item in list1:
    fields = item.split(': ')
    if 'System Name' in fields:
        sys_name = fields[1]
        print(f'Remote system name: {sys_name}')
    if 'Port id' in fields:
        port_id = fields[1]
        print(f'Remote port id: {port_id}')

#!/usr/bin/env python
from pprint import pprint

vlan_list = []
with open('show_vlan.txt') as f:
    show_vlan = f.read()

for line in show_vlan.splitlines():
    if 'VLAN' in line or '------' in line or line.startswith(' '):
        continue
    feilds = line.split()
    if feilds:
        vlan_id = feilds[0]
        vlan_name = feilds[1]
        vlan_list.append((vlan_id, vlan_name))
print()
pprint(vlan_list)
print()

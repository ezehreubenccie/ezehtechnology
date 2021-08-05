#!/usr/bin/env python
from pprint import pprint

with open('show_vlan.txt') as f:
    show_vlan = f.readlines()
vlan_id_name = []
vlan_id_name2 = []
for my_vlan in show_vlan:
    vlan_id_name.append(my_vlan.split()[0:2]) 

for item in vlan_id_name:
    if item and (item[0][0] in ['1','2','3','4','5','6','7','8','9']) and 'enet' not in item and int(item[0]) < 1002:
        vlan_id_name2.append(tuple(item))
print('****vlan id and name 2****')
pprint(vlan_id_name2)


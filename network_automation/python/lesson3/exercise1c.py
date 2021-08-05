#!/usr/bin/env python
from pprint import pprint

vlan_id_name = []
with open('show_vlan.txt') as f:
    show_vlan = f.read()

#print(show_vlan)
print('****show_vlan splitlines****')
pprint(show_vlan.splitlines())
for line in show_vlan.splitlines():
    if line and (line[0][0] in ['1','2','3','4','5','6','7','8','9']) and 'enet' not in line:
#    if 'VLAN' in line or '-----' in line or line.startswith("  ")
        continue
#    print(line.split())
    feilds = line.split()
    print('****feilds output****')
    print(feilds)
    vlan_id = feilds[0]
    print('****vlan_id****')
    pprint(vlan_id)
#    vlan_name = feilds[1]
#    vlan_id_name.append((vlan_id, vlan_name))
#print()
#pprint(vlan_id_name)
#print()
##for item in vlan_id_name:
#    if item and (item[0][0] in ['1','2','3','4','5','6','7','8','9']) and 'enet' not in item:
#        vlan_id_name2.append(tuple(item))
#print('****vlan id and name 2****')
#pprint(vlan_id_name2)
#

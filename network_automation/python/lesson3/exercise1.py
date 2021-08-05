#!/usr/bin/env python
from pprint import pprint

with open('show_vlan.txt') as f:
    show_vlan = f.readlines()
print('****show_vlan****')
pprint(show_vlan)
#vlan_id = ''
#vlan_name = ''
vlan_id_name = []
vlan_id_name2 = []
# my_list = [] 
for my_vlan in show_vlan:
#    pprint(my_vlan.split()[0:2])
    vlan_id_name.append(my_vlan.split()[0:2])
print('****vlan id and name****')
pprint(vlan_id_name) 

for item in vlan_id_name:
    if item and (item[0][0] in ['1','2','3','4','5','6','7','8','9']) and 'enet' not in item and int(item[0]) < 1002:
        print('****item****')
        pprint(item)
        print('****item[0][0]****')
        pprint(item[0][0])
#    if item[0][0]  in range(1,10):
        vlan_id_name2.append(tuple(item))
print('****vlan id and name 2****')
pprint(vlan_id_name2)
##    vlan_id, vlan_name = my_vlan.split()[0:2]
#    pprint('vlan_id: ',vlan_id) 
##     vlan_id = my_vlan[0]
#     vlan_name = my_vlan[1]
#     print(vlan_id, vlan_name)
#     my_tup = (vlan_id, vlan_name)
#     my_list = my_list.append(my_tup)

# print(my_list)

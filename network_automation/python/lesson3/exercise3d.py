#!/usr/bin/env python
from pprint import pprint

with open('cdc-core-5k-2a_show_lldp_nei_det.txt') as f:
    show_lldp = f.read()
#print(show_lldp)
#system_name, port_id = (None, None)
system_name, port_id = ([], [])
for line in show_lldp.splitlines():
#    fields = line.split()
#    print(fields)
    if 'System Name: ' in line:
        fields = line.split('System Name: ')
#        print(fields)
        if fields:
            system_name.append(fields[1])
    elif 'Port id: ' in line and 'Local' not in line:
        fields = line.split('Port id: ')
        if fields:
            port_id.append(fields[1])

#    if port_id and system_name:
#        break
#print()
#print('System Name: {}'. format(system_name))
#print('Remote Port id: {}'. format(port_id))
#print()
print('SYSTEM NAME'.center(30),'PORT ID'.center(30))
print('-' * 60)
print('{:^30}{:^30}'.format(system_name[0],port_id[0]))
print('{:^30}{:^30}'.format(system_name[1],port_id[1]))
print('{:^30}{:^30}'.format(system_name[2],port_id[2]))
print('{:^30}{:^30}'.format(system_name[3],port_id[3]))

#!/usr/bin/env python
from pprint import pprint

with open('cdc-core-5k-2a_show_lldp_nei_det.txt') as f:
    show_lldp = f.read()
#print(show_lldp)
system_name, port_id = (None, None)
for line in show_lldp.splitlines():
#    fields = line.split()
#    print(fields)
    if 'System Name: ' in line:
        fields = line.split('System Name: ')
#        print(fields)
        if fields:
            system_name = fields[1]
    elif 'Port id: ' in line and 'Local' not in line:
        fields = line.split('Port id: ')
        if fields:
            port_id = fields[1]

#    if port_id and system_name:
#        break
print()
print('System Name: {}'. format(system_name))
print('Remote Port id: {}'. format(port_id))
print()

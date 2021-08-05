#!/usr/bin/env python
from pprint import pprint

with open('cdc-core-5k-2a_show_lldp_nei_det.txt') as f:
    show_lldp_nei_det = f.readlines()
pprint(show_lldp_nei_det)

system_name = []
port_id = []
for line in show_lldp_nei_det:
    if 'System Name' in line:
        system_name.append(line.strip())
#        continue
        #found1 = True
    elif 'Port id' in line and 'Local Port id' not in line:
        port_id.append(line.strip())
#        continue
        #found2 = True

    #if found1 and found2:
        #break
print(system_name)
print(port_id)

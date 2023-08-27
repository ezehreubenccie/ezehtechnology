#!/usr/bin/env python3

import re
import regex
import pprint

with open('nxos_vlan_cfg/vlan_data.txt', 'r') as f:
    vlan_data = f.read()

# If you print the string in the python console or ipython3 console
#  you should have a clearer 
# understanding how to instruct python split the string. 
# Printing the string from the python file(.py) won't make it clearer.
print(vlan_data)


vlan_list = [regex.split("\n(?=[^\s])", vlan_data)]

pprint.pprint(vlan_list)
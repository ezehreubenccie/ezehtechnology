#!/usr/bin/env python3

import re
import regex
import pprint

with open('nxos_vlan_cfg/vlan_data.txt', 'r') as f:
    vlan_data = f.read()

vlan_list = [regex.split("\n(?=[^\s])", vlan_data)]

pprint.pprint(vlan_list)
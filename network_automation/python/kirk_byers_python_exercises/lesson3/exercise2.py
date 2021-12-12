#!/usr/bin/env python3

import re

with open('show_arp.txt') as f:
    show_arp = f.read()

# Search for default gateway IP and Mac
pattern = re.compile(r'\b10.4.234.1\b')
for line in show_arp.splitlines():
    mo = pattern.search(line)
    if mo:
        fields = line.split()
        dg_addr = fields[1]
        mac_addr = fields[3]
        print('**********Default Gateway IP/Mac**********')
        print(f'Default gateway IP/Mac: {dg_addr}/{mac_addr}')



# Search for Network tean automation server IP and Mac
pattern = re.compile(r'\b10.4.234.35\b')
for line in show_arp.splitlines():
    mo = pattern.search(line)
    if mo:
        fields = line.split()
        ip_addr = fields[1]
        mac_addr = fields[3]
        print('**********Automation Server IP/Mac**********')
        print(f'Automation Server IP/Mac: {ip_addr}/{mac_addr}')


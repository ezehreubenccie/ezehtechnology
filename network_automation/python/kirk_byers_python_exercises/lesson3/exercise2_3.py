#!/usr/bin/env python3

import re

with open('show_arp.txt') as f:
    show_arp = f.read()

# Search for default gateway IP and Mac
track1 = False
track2 = False
ip1 = re.compile(r'\b10.4.234.1\b')
ip2 = re.compile(r'\b10.4.234.35\b')
for line in show_arp.splitlines():
    mo1 = ip1.search(line)
    mo2 = ip2.search(line)
    if mo1:
        track1 = True
        fields = line.split()
        dg_addr = fields[1]
        mac_addr = fields[3]
        print(f'Default gateway IP/Mac: {dg_addr}/{mac_addr}')
    if mo2:
        track2 = True
        fields = line.split()
        ip_addr = fields[1]
        mac_addr = fields[3]
        print(f'Automation Server IP/Mac: {ip_addr}/{mac_addr}')
    if track1 and track2:
        print('Exiting.......')
        break


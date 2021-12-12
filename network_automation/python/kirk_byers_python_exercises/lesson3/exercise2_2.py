#!/usr/bin/env python3

import re

with open('show_arp.txt') as f:
    show_arp = f.read()

# Search for default gateway IP and Mac
#pattern = re.compile(r'\b10.4.234.1\b')

list1 = []
track1 = False
track2 = False
for line in show_arp.splitlines():
#    mo = pattern.search(line)
    if '10.4.234.1' in line:
        track1 = True
        list1.append(line)
    if '10.4.234.35' in line:
        track2 = True
        list1.append(line)
    if track1 and track2:
        print('Items Found!')
        break

print(list1)



# Search for Network tean automation server IP and Mac
#pattern = re.compile(r'\b10.4.234.35\b')
#for line in show_arp.splitlines():
#    mo = pattern.search(line)
#    if mo:
#        fields = line.split()
#        ip_addr = fields[1]
#        mac_addr = fields[3]
#        print('**********Automation Server IP/Mac**********')
#        print(f'Automation Server IP/Mac: {ip_addr}/{mac_addr}')
#

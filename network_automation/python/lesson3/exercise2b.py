#!/usr/bin/env python

from pprint import pprint

with open('dtx-mrt-4510-sw01_show_arp.txt') as f:
    show_arp = f.readlines()
#pprint(show_arp)
found1,found2 = (False,False)
for entry in show_arp:
    ip_addr = entry.split()[1]
    mac_addr = entry.split()[3]
    if ip_addr == '10.4.234.1':
        print('Merit HQ 4510 Switch Default gateway IP/MAC for VLAN 100 is: {}/{}'. format(ip_addr,mac_addr))
        found1 = True
    elif ip_addr == '10.4.234.35':
        print('Reuben"s Automation Server IP/MAC is: {}/{}'. format(ip_addr,mac_addr))
        found2 = True

    if found1 and found2:
        print('Exiting....')
        break

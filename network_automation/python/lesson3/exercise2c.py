#!/usr/bin/env python
from pprint import pprint

with open('dtx-mrt-4510-sw01_show_arp.txt') as f:
    show_arp = f.read()
#print(show_arp) 

found1, found2 = (False,False)
for line in show_arp.splitlines():
    fields = line.split()
    ip_addr = fields[1]
    mac_addr = fields[3]

    if ip_addr == '10.4.234.1':
        print('Merit HQ 4510 Switch Default gateway IP/Mac is: {}/{}'. format(ip_addr, mac_addr))
        found1 = True
    elif ip_addr == '10.4.234.35':
        print("Reuben's Automation Server IP/Mac is: {}/{}". format(ip_addr, mac_addr))
        found2 = True
    

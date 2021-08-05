#!/usr/bin/env python

from pprint import pprint

with open('dtx-mrt-4510-sw01_show_arp.txt') as f:
    show_arp = f.readlines()
#pprint(show_arp)
found1,found2 = (False,False)
for entry in show_arp:
    ip_addr = entry.split()[1]
    mac_addr = entry.split()[3]
    if '10.4.234.1' in entry.split():
#        ip_addr = entry.split()[1]
#        mac_addr = entry.split()[3]
        print('Default gateway IP/MAC is: {}/{}'. format(ip_addr,mac_addr))
        #print(ip_addr, mac_addr)
        #break
        found1 = True
    elif '10.4.234.35' in entry.split():
        print('Reuben"s Automation Server IP/MAC is: {}/{}'. format(ip_addr,mac_addr))
        found2 = True

    if found1 and found2:
        print('Exiting....')
        break
#    break
#    pprint('****ip_addr and mac_addr entry****')
#    pprint(entry.split()[1])
#    print('****ip_address****')
#    ip_addr = entry.split()[1]
#    pprint(ip_addr)
#    print('****mac address****')
#    mac_addr = entry.split()[3]
#    print(mac_addr)
##    print('****ip address and mac****')
#    print(ip_addr, mac_addr)

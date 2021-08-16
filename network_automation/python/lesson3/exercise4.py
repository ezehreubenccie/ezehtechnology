#!/usr/bin/env python
from pprint import pprint

with open('dtx-mrt-4510-sw01_show_arp.txt') as f:
    show_arp = f.read()


arp_table = []
for lines in show_arp.splitlines()[1:]:
#    print(lines.split())
    fields = lines.split()
    ip_addr = fields[1]
    mac_addr = fields[3]
    arp_table.append((ip_addr,mac_addr))

# Extract mac addresses and print standardized format
for ip_addr, mac_addr in arp_table:
    mac_addr = mac_addr.split('.')
    mac_addr = ''.join(mac_addr)
    mac_addr = mac_addr.upper()

    mac_addr_strd = []
    while len(mac_addr) > 0:
        entry = mac_addr[:2]
        mac_addr = mac_addr[2:]
        mac_addr_strd.append(entry)

    # Reunite MAC address using a colon
    mac_addr_strd = ':'.join(mac_addr_strd)
    pprint(mac_addr_strd)

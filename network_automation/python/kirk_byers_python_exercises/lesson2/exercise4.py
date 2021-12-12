#!/usr/bin/env python3

from pprint import pprint

with open('show_ip_int_brief.txt') as f:
    intf = f.readlines()
pprint(intf)

g0_0_2 = intf[3]
print(g0_0_2)
feilds = g0_0_2.split()
print(feilds)
gintf = feilds[0]
ip_addr = feilds[1]
print(f'Interface: {gintf}\nIP Address: {ip_addr}')
print('****Creating Tuple****')
tup1 = (gintf, ip_addr)
print(type(tup1))
print(tup1)

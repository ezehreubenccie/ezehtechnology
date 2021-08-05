#!/usr/bin/env python
from pprint import pprint

with open('show_ip_int_brief.txt') as f:
    show_intf = f.readlines()

show_intf = show_intf[1:]
mpls_intf = show_intf[2]
mpls_intf_list = mpls_intf.split()
pprint('****Extract Interface and IP****')
ip_and_intf_tup = tuple(mpls_intf_list[0:2])
pprint(ip_and_intf_tup)


#!/usr/bin/env python
from pprint import pprint

with open('show_ip_int_brief.txt') as f:
    show_ip_int_brief = f.readlines()

pprint(show_ip_int_brief)
g0_0_2_ip = show_ip_int_brief[3].strip()
pprint(g0_0_2_ip)
#show_intf = show_intf[1:]
#pprint(show_intf)
#pprint('****Obtain IP address of MPLS interface**** ')
#mpls_intf = show_intf[2]
#pprint(mpls_intf)
#pprint(type(mpls_intf))
#mpls_intf_list = mpls_intf.split()
#pprint(mpls_intf_list)
#pprint('****Extract Interface and IP****')
#ip_and_intf_tup = tuple(mpls_intf_list[0:2])
#pprint(ip_and_intf_tup)
#pprint(type(ip_and_intf_tup))

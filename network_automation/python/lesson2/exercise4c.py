#!/usr/bin/env python
from pprint import pprint

with open('show_ip_int_brief.txt') as f:
    show_ip_int_brief = f.readlines()

pprint(show_ip_int_brief)
#show_ip_int_brief = show_intf[1:]
#pprint(show_intf)
#pprint('****Obtain IP address of MPLS interface**** ')
mpls_intf = show_ip_int_brief[3]
pprint(mpls_intf)
print(type(mpls_intf))
mpls_intf_list = mpls_intf.split()
pprint(mpls_intf_list)
pprint('****Extract Interface and IP****')
intf = mpls_intf_list[0]
ip_address = mpls_intf_list[1]
ip_and_intf_tup = (intf, ip_address)
pprint(ip_and_intf_tup)
pprint(type(ip_and_intf_tup))

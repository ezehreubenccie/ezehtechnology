#!/usr/bin/env python
from pprint import pprint

with open('show_ip_bgp_sum.txt') as f:
    show_ip_bgp_sum = f.readlines()

pprint(show_ip_bgp_sum)
bgp_local_as_num = show_ip_bgp_sum[0].split()[-1]
bgp_peer_ip = show_ip_bgp_sum[-1].split()[2]
print('BGP local AS number: ',bgp_local_as_num)
print('BGP Peer IP: ',bgp_peer_ip)

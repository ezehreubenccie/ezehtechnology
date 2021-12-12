#!/usr/bin/env python3

from pprint import pprint

with open('show_ip_bgp_summ.txt') as f:
    bgp = f.readlines()
#pprint(bgp)

first_line = bgp[0]
last_line = bgp[-2:]
#print(first_line)
#print(last_line)

feilds = first_line.split()
#print(feilds)
as_numb = feilds[-1]
router_ip = feilds[3]
router_ip = router_ip[:-1]
#print(as_numb)
bgp_peer_ip = []
feilds1 = []
for item in last_line:
#    print(item)
    feilds1 = item.split()
#    print(feilds1)
    bgp_peer_ip.append(feilds1[0])

#print(bgp_peer_ip)
print(f'ROUTER IP: {router_ip}')
print('-' * 24)
print(f'AS Number: {as_numb}')
for ip in bgp_peer_ip:
    print(f'BGP Peer IP{bgp_peer_ip.index(ip) + 1}: {ip}')


#!/usr/bin/env python
from pprint import pprint

with open('show_ip_bgp_sum.txt') as f:
    bgp_summ = f.read()
#print(bgp_summ)

bgp_summ = bgp_summ.splitlines()
pprint(bgp_summ) 
first_line = bgp_summ[0]
as_number = first_line.split()[-1]

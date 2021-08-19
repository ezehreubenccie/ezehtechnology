#!/usr/bin/env python

import random

def ip_generator(base_ip='10.10.10.'):
    randOct = random.randint(1, 254)
    ip_addr = base_ip + str(randOct)
    return ip_addr

ip_address = ip_generator('10.2.254.')
print(ip_address)
ip_address = ip_generator()
print(ip_address)
ip_address = ip_generator(base_ip='10.4.234.')
print(ip_address)

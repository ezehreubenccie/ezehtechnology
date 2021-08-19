#!/usr/bin/env python


import re
from pprint import pprint

def mac_norm(mac_address):
    mo = re.search(r'^\w\w:\w\w:\w\w:\w\w:\w\w:\w\w$', mac_address)
    mo2 = re.search(r'^\w\w\w\w.\w\w\w\w.\w\w\w\w$', mac_address)
    mo3 = re.search(r'^\w:\w:\w:\w:\w:\w$', mac_address)
    if mo:
        print('Mac address already in normalized format.')
        print()
        print('You entered {}'.format(mac_address))
        print()
        print('Standardized format is {}'.format(mac_address.upper()))
        return
    elif mo2:
        print('Normalized mac address is below.')
        print()
        mac_addr = mac_address.split('.')
        mac_addr = ''.join(mac_addr)
        mac_addr = mac_addr.upper()

        mac_addr_strd = []
        while len(mac_addr) > 0:
            entry = mac_addr[:2]
            mac_addr = mac_addr[2:]
            mac_addr_strd.append(entry)

        mac_addr_strd = ':'.join(mac_addr_strd)
        print(mac_addr_strd)
    elif mo3:
        print('The zero-padded two digits is')
        print()
        mac_addr = mac_address.split(':')
        mac_addr = ''.join(mac_addr)
        mac_addr = mac_addr.upper()

        mac_addr_strd = []
        while len(mac_addr) > 0:
            entry = '0' + mac_addr[:1]
            mac_addr = mac_addr[1:]
            mac_addr_strd.append(entry)
        mac_addr_strd = ':'.join(mac_addr_strd)
        print(mac_addr_strd)
    else:
        print('Enter a mac address in the following format (xx:xx:xx:xx) or (x:x:x:x:x:x) or (xxxx.xxxx.xxxx) as function arg.')
        return
#    return mac_addr_strd

mac_norm('0ae5.e4b0.456e')
#print(mac_address)

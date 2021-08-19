#!/usr/bin/env python

def print_ip(ip_addr, username='admin', password='cisco123'):
    print('My IP address is: {}'.format(ip_addr))
    print(username)
    print(password)
    return

print_ip('10.247.0.254')


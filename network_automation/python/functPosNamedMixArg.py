#!/usr/bin/env python

# Positional arguments should come before named arguments

def print_ip(ip_addr, username, password):
    print('My IP address is: {}'.format(ip_addr))
    print(username)
    print(password)
    return

print_ip('10.247.0.1',password='admin123',username='admin')


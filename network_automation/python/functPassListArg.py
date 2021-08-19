#!/usr/bin/env python

def print_ip(ip_addr, username, password):
    print('My IP address is: {}'.format(ip_addr))
    print(username)
    print(password)
    return

my_list = ['10.249.0.1', 'admin', 'Cisco123']
print_ip(*my_list)


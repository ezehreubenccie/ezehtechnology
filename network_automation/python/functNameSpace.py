#!/usr/bin/env python

# If same variables are used, python is going to look for a variable in the local ns, if the variable is not defined in the local
# fuction, it will now look in the wider context

ip_addr2 = '192.168.148.1'
def print_ip(ip_addr, username, password):
    print('My IP address is: {}'.format(ip_addr))
    print('My IP address2 is: {}'.format(ip_addr2))
    print(username)
    print(password)
    return

print_ip('10.247.0.1','admin','admin123')


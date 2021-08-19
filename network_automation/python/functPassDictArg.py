#!/usr/bin/env python

def print_ip(ip_addr, username, password):
    print('My IP address is: {}'.format(ip_addr))
    print(username)
    print(password)
    return

my_dict = {'ip_addr':'172.16.31.1', 
           'username':'admin', 
           'password':'juniper123',
}
print_ip(**my_dict)


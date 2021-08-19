#!/usr/bin/env python

def ssh_conn(ip_addr, username, password, device_type='cisco'):
    print('IP address is: {}'.format(ip_addr))
    print('Username is: {}'.format(username))
    print('Password is: {}'.format(password))
    print('Device type is: {}'.format(device_type))
    return

ssh_conn('10.2.254.43', 'reuben3010', 'cisco234!')
print()
ssh_conn(ip_addr='10.247.0.10', password='password@1!', username='reuben.ezeh')
print()
ssh_conn('172.28.0.4', 'sshadmin', password='juniper123^&')

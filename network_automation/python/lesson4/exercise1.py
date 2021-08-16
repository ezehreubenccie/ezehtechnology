#!/usr/bin/env python

from pprint import pprint

net_device = {'ip_addr': '10.7.250.59', 'vendor': 'cisco', 'username': 'reuben', 'password': 'cisco'}
bgp_fields = {'bgp_as': '65015', 'peer_as': '2828', 'peer_ip': '10.247.0.5'}
print('****IP Address Key****')
print(net_device['ip_addr'])

print('****Set platform to ios****')
net_device['platform'] = 'ios'
pprint(net_device)

print('****Update Network device with bgp fields****')
net_device.update(bgp_fields)
pprint(net_device)


print('****Print all keys in network device dict****')
for key in net_device.keys():
    print(key)

print('****Print all keys and Values****')
print()
print('{:^15}{:^15}'.format('KEY', 'VALUE'))
print('-' * 30)
for key, value in net_device.items():

#    print('{:^20}{:^20}'.format('KEY', 'VALUE'))
#    print('-' * 40)
    print('{:^15}{:^15}'. format(key, value))
    print('-' * 30)

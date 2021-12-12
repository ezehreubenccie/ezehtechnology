#!/usr/bin/env python3

from pprint import pprint
import os

base_cmd_linux = 'ping -q -c 2'
base_cmd_windows = 'ping -n 2'
WINDOWS = False
base_cmd = base_cmd_windows if WINDOWS else base_cmd_linux
ip_list = []
for i in range(1, 255):
    ip_addr = '10.2.0.' + str(i)
#    print(ip_addr)
    ip_list.append(ip_addr)
#pprint(ip_list)
#list2 = []
for index, item in enumerate(ip_list):
    print(f'{index} ---> {item}')
#    print(type(index))
#    break
list2 = ip_list[99:102]
#print(list2)

for ip in list2:
    print(f'Pinging {ip}.......')
    return_code = os.system(f'{base_cmd} {ip}')
#    print(f'Pinging {ip}.......')
    print('-' * 60)
#    print(return_code)

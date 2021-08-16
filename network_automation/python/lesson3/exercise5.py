#!/usr/bin/env python 
from pprint import pprint
import os

WINDOWS = False

base_ip = '10.2.0.'
base_cmd_linux = 'ping -c 2'
base_cmd_windows = 'ping -n 2'

# Tenary operator
base_cmd = base_cmd_windows if WINDOWS else base_cmd_linux 

my_ip_list = []
for num in range(1, 255):
#    print(num)
    ip_addr = base_ip + str(num)
#    print(ip_addr)
#    my_list.append
    my_ip_list.append(ip_addr)
#pprint(my_ip_list)

#for index, value in enumerate(my_ip_list):
#    print('{} ---> {}'.format(index, value))


new_list = my_ip_list[2:6]
#print(new_list)

print()
print('-' * 80)
for ip in new_list:
    print('IP Addr: ', ip)
    return_code = os.system('{} {}'.format(base_cmd, ip))
    print('-' * 80)
print('-' * 80)
print()

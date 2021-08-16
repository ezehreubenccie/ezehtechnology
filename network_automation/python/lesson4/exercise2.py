#!/usr/bin/env python
from pprint import pprint

hou_base_ip = '10.1.1.'
atl_base_ip = '10.1.1.'
chi_base_ip = '10.1.1.'

hou_dc_ip_list = []
atl_dc_ip_list = []
chi_dc_ip_list = []

print('****Houston datacenter routers ip****')
print()
for num in range(1, 11):
    ip_addr = hou_base_ip + str(num)
    hou_dc_ip_list.append(ip_addr)
    if num >= 6:
        hou_dc_ip_list.append(ip_addr) 
#pprint(hou_dc_ip_list)

print('****Atlanta datacenter routers ips****')
print()
for num in range(7, 15):
    ip_addr = atl_base_ip + str(num)
    atl_dc_ip_list.append(ip_addr)
#pprint(atl_dc_ip_list)

print('****Chicago datacenter routers ips****')
print()
for num in range(8, 21):
    ip_addr = chi_base_ip + str(num)
    chi_dc_ip_list.append(ip_addr)
#pprint(chi_dc_ip_list)


print('****Convert ip lists to sets****')
print()
print('****Houston dc ip set****')
hou_dc_ip_set = set(hou_dc_ip_list)
pprint(hou_dc_ip_set)
print()
print('****Atlanta dc ip set****')
atl_dc_ip_set = set(atl_dc_ip_list)
pprint(atl_dc_ip_set)
print()
print('****Chicago dc ip set****')
chi_dc_ip_set = set(chi_dc_ip_list)
pprint(chi_dc_ip_set)
print()

print('****Find duplicated IPs in Houston and Atlanta sets****')
dup_ips_hou_atl = hou_dc_ip_set.intersection(atl_dc_ip_set)
pprint(dup_ips_hou_atl)
pprint(hou_dc_ip_set & atl_dc_ip_set)
print()

print('****Find duplicated IPs in all sets****')
print(hou_dc_ip_set & atl_dc_ip_set & chi_dc_ip_set)
print()

print('****Chicago unique IPs****')
print(chi_dc_ip_set.difference(hou_dc_ip_set).difference(atl_dc_ip_set))

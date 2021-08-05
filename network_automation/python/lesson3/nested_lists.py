#!/usr/bin/env python
some_list = ['192.168.1.1', '10.1.1.1', '10.10.20.30', '172.16.31.254']
ip_list2 = ['8.8.8.8', '8.8.4.4']

for ip in some_list:
    for ip2 in ip_list2:
        print(ip2)

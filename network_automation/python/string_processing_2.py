#!/usr/bin/env python3


mac1 = 'Internet 10.220.88.29     94 5254.abbe.5b7b ARPA FastEthernet4'
mac2 = 'Internet 10.220.88.30     94 5254.a7b1.e119 ARPA FastEthernet4'
mac3 = 'Internet 10.220.88.32     94 5254.abc7.26aa ARPA FastEthernet4'

#print(mac1.split())
#print(mac2.split())
#print(mac3.split())

feilds = mac1.split()
ip_addr1 = feilds[1]
mac_addr1 = feilds[3]

feilds = mac2.split()
ip_addr2 = feilds[1]
mac_addr2 = feilds[3]

feilds = mac3.split()
ip_addr3 = feilds[1]
mac_addr3 = feilds[3]

print('IP ADDR'.center(18), 'MAC ADDRESS'.center(18))
print('-' * 36)
print('{:^18}{:^18}'.format(ip_addr1, mac_addr1))
print('{:^18}{:^18}'.format(ip_addr2, mac_addr2))
print('{:^18}{:^18}'.format(ip_addr3, mac_addr3))

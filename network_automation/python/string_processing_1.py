#!/usr/bin/env python3


mac1 = 'Internet 10.220.88.29     94 5254.abbe.5b7b ARPA FastEthernet4'
mac2 = 'Internet 10.220.88.30     94 5254.a7b1.e119 ARPA FastEthernet4'
mac3 = 'Internet 10.220.88.32     94 5254.abc7.26aa ARPA FastEthernet4'

#print(mac1.split())
#print(mac2.split())
#print(mac3.split())

mac1 = mac1.split()
mac2 = mac2.split()
mac3 = mac3.split()

print(mac1)
print(mac2)
print(mac3)
print('IP ADDR'.center(18), 'MAC ADDRESS'.center(18))
print('-' * 36)
print('{ip_addr1:^18}{mac_addr1:^18}'.format(ip_addr1=mac1[1], mac_addr1=mac1[3]))
print('{ip_addr2:^18}{mac_addr2:^18}'.format(ip_addr2=mac2[1], mac_addr2=mac2[3]))
print('{ip_addr3:^18}{mac_addr3:^18}'.format(ip_addr3=mac3[1], mac_addr3=mac3[3]))

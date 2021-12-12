#!/usr/bin/env python3

list1 = ['10.2.0.100', '10.247.0.1', '10.10.100.10', '10.200.23.100', '1.5.20.20']
print(list1)
list1.append('5.5.5.5')
print(list1)
list1.extend(['6.6.6.6', '7.7.7.7'])
print(list1)
#list2 = ['9.9.9.9', '8.8.8.8']
list1 = list1 + ['9.9.9.9', '8.8.8.8']
print(list1)
#print(list2)

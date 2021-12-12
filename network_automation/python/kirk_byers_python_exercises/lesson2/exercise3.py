#!/usr/bin/env python3

from pprint import pprint

with open('show_arp.txt') as f:
    output = f.read()

print(output)
print(type(output))

list1 = output.splitlines()
print(list1)
list1 = list1[1:]
pprint(list1)

list1.sort()
pprint(list1)
#list1 = list1.sort()
#pprint(list1)
my_entries = list1[:3]
pprint(my_entries)
my_entries = '\n'.join(my_entries)
print(my_entries)
with open('arp_entries.txt', 'wt') as f:
    f.write(my_entries)


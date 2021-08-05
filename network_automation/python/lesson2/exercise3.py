#!/usr/bin/env python
from pprint import pprint

with open('show_arp.txt') as f:
    output = f.readlines()

pprint(output)
output = output[1:]
pprint(output)
print('****Sort list items****')
output.sort()
pprint(output)
print('****Create new list with first three items****')
fir_three = output[:3]
pprint(fir_three)
print('****Join items in new list****')
my_entries = '\n'.join(fir_three)
pprint(my_entries)
print(type(my_entries))
print('****Write new list to file****')

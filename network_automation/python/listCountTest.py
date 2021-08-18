#!/usr/bin/env python

my_list = ['Reuben', 'Jaden', 'Naomi']
count = {}

for name in my_list:
    count.setdefault(name, 0)
    count[name] = count[name] + 1
print(count)

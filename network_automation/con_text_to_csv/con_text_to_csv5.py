#!/usr/bin/env python3

import pprint


with open('NY_rule_hit_export.txt', 'r') as handle:
    lines = handle.read().splitlines()

list1 = []
#pprint.pprint(lines[2:])
for line in lines[2:]:
    print(line.split())
    

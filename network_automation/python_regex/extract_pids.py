#!/usr/bin/env python3

import re

with open('listOfProducts.txt', 'r') as handle:
    text = handle.read()

#print(text)
#print(type(text))

pattern = re.compile(r'(\d+)-\w+')

it = pattern.finditer(text)

pids = []
for match in it:
    #print(match.group(1))
    pids.append(match.group(1))

print(pids)    

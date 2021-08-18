#!/usr/bin/env python

import re

with open('show_version.txt') as f:
    output = f.read()
#print(output)


match = re.search(r'^cisco (?P<devModel>\w+/\w+) \(\w+\)[\s\w]+\s(?P<memory>\w+/\w+) bytes of memory\.$', output, flags=re.M)
print(match)
print(match.groupdict())
devModel = match.groupdict()['devModel']
print(devModel)
#if match:
#    devModel = match.group(1)
#    memory = match.group(2)
#print(devModel)
#print(memory)

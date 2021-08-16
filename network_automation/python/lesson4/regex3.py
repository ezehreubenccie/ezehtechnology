#!/usr/bin/env python
import re
from pprint import pprint

with open('show_version.txt') as f:
    output = f.read()

#print(output)

show_ver = output.splitlines()
line = show_ver[1]
#print(line)
#mo = re.search(r'^C.*$', line)
#print(mo.group())

mo = re.search(r'^C.*, Version (\S+), .*$', line)
#print(mo.group())
#print(mo.group(1))

mo = re.search(r'^Cisco IOS Software \[(?P<os_model>\S+)\], .*, Version (?P<os_version>\S+), .*$', line)
#print(mo.groupdict())
#print(mo.group(1))
#print(mo.group(2))
#ios_name = mo.group(1)
#ios_version = mo.group(2)
#print('IOS name is: {}'.format(ios_name))
#print('IOS Version is: {}'. format(ios_version))

mo = re.search(r'^Cisco (.*), Version (\S+), .*$', line)
#print(mo)
#print(mo.group())
#print(mo.group(1))
#print(mo.group(2))

mo = re.search(r'^C.*$', line)
#print(mo.group())
#print(mo.group(1))

mo = re.search(r'^Cisco IOS Software \[(\S+)\], .*, Version (\S+), .*$', line)
#print(mo)

#mo = re.search(r'^Cisco.*$', line)
#print(mo)

mo = re.search(r'^Cisco (.*?), ', line)
#print(mo)
#print(mo.group(0))
#print(mo.group(1))
#
#mo = re.search(r'^Cisco .*?, ', line)
#print(mo)
#print(mo.group(0))
##print(mo.group(1))

mo = re.search(r'^.*?,', line)
#print(mo)
#print(mo.group(0))
#print(mo.group(1))

mo = re.search('Processor board ID (.*)$', output, flags=re.M)
#print(mo)
#print(mo.group(1))

mo = re.search(r'^Cisco.*', output, flags=re.DOTALL)
#print(mo)
#print(mo.group(0))

mo = re.split(r'^-------.*$', output, flags=re.M)
#pprint(mo)
#print(len(mo))
print(mo[0])
print(mo[1])
#print(mo.group())

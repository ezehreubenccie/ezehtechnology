#!/usr/bin/env python

import re

with open('show_version.txt') as f:
    output = f.read()
#print(output)

# Extract OS Version

showVer = output.splitlines()
line = showVer[0]
#print(line)

mo = re.search(r'^C.*, Version (\S+)', line)
#print(mo)
#print(mo.group(1))
#print('****OS Version****')
version = mo.group(1)
#print(version)

# Extract Serial number
mo = re.search('Processor board ID (.*)$', output, flags=re.M)
#print('****serial number****')
serial = mo.group(1)
#print(serial)

# Extract config register
mo = re.search('Configuration register is (\S+)$', output, flags=re.M)
#print('****Config Register****')
confReg = mo.group(1)


print('OS Version: {}'.format(version))
print('Serial Number: {}'.format(serial))
print('Config Register: {}'.format(confReg))

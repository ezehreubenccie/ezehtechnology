#!/usr/bin/env python

import re

with open('show_version.txt') as f:
    output = f.read()

showVer = output.splitlines()
line = showVer[0]

# Extract OS Version
mo = re.search(r'^C.*, Version (\S+)', line)
version = mo.group(1)

# Extract Serial number
mo = re.search('^Processor board ID (.*)$', output, flags=re.M)
serial = mo.group(1)

# Extract config register
mo = re.search('^Configuration register is (\S+)$', output, flags=re.M)
confReg = mo.group(1)

print('OS Version: {}'.format(version))
print('Serial Number: {}'.format(serial))
print('Config Register: {}'.format(confReg))

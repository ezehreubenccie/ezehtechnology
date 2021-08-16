#!/usr/bin/env python
import re

#line = '10.220.100.1'
#ip_addr = line
#mo = re.search(r'', ip_addr)
#print(mo)

#line = '10.220.100.1'
#ip_addr = line
#mo = re.search(r'.', ip_addr)
#print(mo.group(0))

#line = '1      '
#ip_addr = line
#mo = re.search(r'.*', ip_addr)
#print(mo)

#line = '1      '
#ip_addr = line
#mo = re.search(r'.+', ip_addr)
#print(mo)

#line = ''
#ip_addr = line
#mo = re.search(r'.', ip_addr)
#print(mo)

#line = ''
#ip_addr = line
#mo = re.search(r'.*', ip_addr)
#print(mo)
#
#line = ''
#ip_addr = line
#mo = re.search(r'.+', ip_addr)
#print(mo)
#
#line = '10.220.100.1'
#ip_addr = line
#mo = re.search(r'.*', ip_addr)
#print(mo)
#
#
#line = '10.220.100.1'
#ip_addr = line
#mo = re.search(r'.+', ip_addr)
#print(mo)
#
#line = '10.220.100.1'
#ip_addr = line
##print(ip_addr)
#mo = re.search(r'^.*$', ip_addr)
#print(mo)
#
#line = '10.220.100.145'
#ip_addr = line
#mo = re.search(r'\d+$', ip_addr)
#print(mo)
#
#line = '10.220.100.147'
#ip_addr = line
#mo = re.search(r'\d$', ip_addr)
#print(mo)
#
#line = '     10.220.100.147     '
#ip_addr = line
#mo = re.search(r'^\s+\d', ip_addr)
#print(mo)
#
#line = '     10.220.100.147     '
#ip_addr = line
#mo = re.search(r'^\s+\d+', ip_addr)
#print(mo)
#
#line = '     10.220.100.147     '
#ip_addr = line
#mo = re.search(r'^\s+\S+', ip_addr)
#print(mo)


#line = '     1.220.100.147     '
#ip_addr = line
#mo = re.search(r'\s+[\d\.]', ip_addr)
#print(mo)
#
#
#line = '     1.220.100.147     '
#ip_addr = line
#mo = re.search(r'\s+[\d\.]*', ip_addr)
#print(mo)


line = '     1.220.100.147     '
ip_addr = line
mo = re.search(r'\s+(\S+)', ip_addr)
print(mo)
print(mo.group(0))
print(mo.group(1))
print(mo.groups())

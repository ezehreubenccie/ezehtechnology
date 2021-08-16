#!/usr/bin/env python
import re

my_str = 'The quick brown fox jumps over the lazy dog'
mo = re.search(r'fox', my_str) 
print(mo)

my_str = 'To be or not to be'
mo = re.search(r'be', my_str)
print(mo)

my_str = 'this is outside (this is inside)'
mo = re.search('(this is inside)', my_str)
print(mo)

my_str = '10.220.100.1'
mo = re.search(r'\d\d\.', my_str)
print(mo)

my_str = '10.220.100.1'
mo = re.search(r'[\d].', my_str)
print(mo)

my_str = '10.220.100.1'
mo = re.search(r'[\d]\.', my_str)
print(mo)

#!/usr/bin/env python
from pprint import pprint

with open('show_version.txt') as f:
    show_version = f.readlines()
print(show_version)
print(type(show_version))

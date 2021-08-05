#!/usr/bin/env python
from pprint import pprint

with open('show_version.txt') as f:
    show_version = f.read()
print(show_version)
print(type(show_version))

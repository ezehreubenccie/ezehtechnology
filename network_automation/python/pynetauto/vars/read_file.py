#!/usr/bin/env python3

from yaml import safe_load


with open('dtx-lbjlab-5506x-asa01.yml', 'r') as handle:
    output = safe_load(handle)
    print(output)

#!/usr/bin/env python3


from yaml import safe_load

with open('hosts.yml', 'r') as handle:
    host_root = safe_load(handle)
    print(host_root)

print(host_root['host_list'])

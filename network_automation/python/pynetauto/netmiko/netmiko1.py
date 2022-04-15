#!/usr/bin/env python3


from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader

def main():
    with open('hosts.yml', 'r') as handle:
        host_root = safe_load(handle)

    platform_map = {'ios': 'cisco_ios', 'iosxr': 'cisco_xr'}

    for host in host_root['host_list']:
        platform = platform_map[host['platform']]


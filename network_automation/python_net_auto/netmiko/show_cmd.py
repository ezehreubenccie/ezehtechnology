#!/usr/bin/env python3

from netmiko import Netmiko
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader
from getpass import getpass


def main():

    with open('hosts/show_cmd.yml', 'r') as handle:
        host_root = safe_load(handle)


    platform_map = {'ios': 'cisco_ios'}

    for host in host_root['host_list']:
        platform = platform_map[host['platform']]
    
        with open('show_cmd.yml', 'r') as handle:
            command = host['cmd']

        conn = Netmiko(
            host=host['name'],
            username=)









if __name__ == "__main__":
    main()

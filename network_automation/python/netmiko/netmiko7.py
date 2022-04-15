#!/usr/bin/env python3


from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import getpass

def get_og(file):
    with open(file, 'r') as handle:
        host_root = safe_load(handle)
    print(host_root)
    platform_map = {'asa': 'cisco_asa'}
    
    username = 'SA_Solarwinds'
    password = getpass.getpass('Enter ssh password:')
    enable = getpass.getpass('Enter enable password:')
    for host in host_root['host_list']:
        platform = platform_map[host['platform']] 

        conn = ConnectHandler(
            host=host['name'], 
            username=username,  
            password=password,
            secret=enable,  
            device_type=platform,
            session_log='netmiko7.log'  
        )

        print(f'Logged into {conn.find_prompt()} successfully')

        result = conn.send_command('sh run object-group id BLOCKED_HOSTS')

#        print(result)

        conn.disconnect()

        print(f"Writing {host['name']} facts to file")
        with open(f'{host["name"]}_blocked_hosts_og.txt', 'w') as handle:
            handle.write(result)
    return f'{host["name"]}_blocked_hosts_og.txt'

if __name__=='__main__':
    hosts = 'hosts3.yml'
    get_og(hosts)

#!/usr/bin/env python3


from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import getpass
from datetime import datetime

def blk_ip(file):
    with open(file, 'r') as handle:
        host_root = safe_load(handle)
    print(host_root)
    platform_map = {'asa': 'cisco_asa'}
    
    username = 'SA_Solarwinds'
    password = getpass.getpass('Enter ssh password:')
    enable = getpass.getpass('Enter enable password:')
    for host in host_root['host_list']:
        platform = platform_map[host['platform']] 

        with open(f'vars/ips_to_block/mal_ip.yml', 'r') as handle:
            blocked = safe_load(handle)

        j2_env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, autoescape=True)
        template = j2_env.get_template(f'templates/add_lines_to_objg/{platform}.j2')

        config = template.render(data=blocked)


        conn = ConnectHandler(
            host=host['name'], 
            username=username,  
            password=password,
            secret=enable,  
            device_type=platform,
            session_log='add_lines_to_blocked_hosts_acl.log'  
        )

        print(f'Logged into {conn.find_prompt()} successfully')
#        object_group = 'USAP-Server-Subnets'
#        result = conn.send_command(f'sh run object-group id {object_group}')

#        print(result)

        conn.disconnect()

#        print(f"Writing {host['name']} network object group to file")
#        with open(f'{host["name"]}_{object_group}_og.txt', 'w') as handle:
#            handle.write(result)
#    return f'{host["name"]}_{object_group}_og.txt'

if __name__=='__main__':
    hosts = 'hosts_lab.yml'
    blik_ip(hosts)

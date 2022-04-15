#!/usr/bin/env python3


from yaml import safe_load
from netmiko import Netmiko, file_transfer
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler

def main():
    with open('hosts.yml', 'r') as handle:
        host_root = safe_load(handle)
    print(host_root)
    platform_map = {'ios': 'cisco_ios', 'asa': 'cisco_asa'}

    enable = 'cisco'
    file = 'test.txt'
    for host in host_root['host_list']:
        platform = platform_map[host['platform']] 

        print(f"Connecting to {host['name']}")
#        if platform == 'cisco_xe':
        conn = ConnectHandler(
            host=host['name'], 
            username='reuben',  
            password='cisco',
#            secret=enable,  
            device_type=platform,
            session_log='netmiko3.log'  
        )
        
        print(f'uploading {file}')
        result = file_transfer(conn, source_file=file, dest_file=file, file_system=host.get('file_system'))
        print(f'Logged into {conn.find_prompt()} successfully')

#        result = conn.send_config_set(config.split('\n'))

        print(f'Details: {result}\n')

        conn.disconnect()
if __name__=='__main__':
    main()

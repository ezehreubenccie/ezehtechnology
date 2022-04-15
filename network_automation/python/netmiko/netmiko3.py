#!/usr/bin/env python3


from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler

def main():
    with open('hosts.yml', 'r') as handle:
        host_root = safe_load(handle)
    print(host_root)
    platform_map = {'ios': 'cisco_ios', 'asa': 'cisco_asa'}

    enable = 'cisco'
    for host in host_root['host_list']:
        platform = platform_map[host['platform']] 

        with open(f'vars/{host["name"]}.yml', 'r') as handle:
            interfaces = safe_load(handle)

        j2_env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, autoescape=True)
        template = j2_env.get_template(f'templates/{platform}.j2')

        config = template.render(data=interfaces)
#        if platform == 'cisco_xe':
        conn = ConnectHandler(
            host=host['name'], 
            username='reuben',  
            password='cisco',
#            secret=enable,  
            device_type=platform,
            session_log='netmiko3.log'  
        )

        print(f'Logged into {conn.find_prompt()} successfully')

        result = conn.send_config_set(config.split('\n'))

        print(result)

        conn.disconnect()
if __name__=='__main__':
    main()

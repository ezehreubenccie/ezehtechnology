#!/usr/bin/env python3


from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler

def main():
    with open('hosts2.yml', 'r') as handle:
        host_root = safe_load(handle)
    print(host_root)
    platform_map = {'asa': 'cisco_asa'}

    enable = 'cisco'
    for host in host_root['host_list']:
        platform = platform_map[host['platform']] 

#        with open(f'vars/{host["name"]}.yml', 'r') as handle:
#            interfaces = safe_load(handle)

#        j2_env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, autoescape=True)
#        template = j2_env.get_template(f'templates/{platform}.j2')

#        config = template.render(data=interfaces)
#        if platform == 'cisco_xe':
        conn = ConnectHandler(
            host=host['name'], 
            username='reuben',  
            password='cisco',
#            secret=enable,  
            device_type=platform,
            session_log='netmiko4.log'  
        )

        print(f'Logged into {conn.find_prompt()} successfully')

        result = conn.send_command('sh run object-group id BLOCKED_HOSTS')

#        print(result)

        conn.disconnect()

        print(f"Writing {host['name']} facts to file")
        with open(f'{host["name"]}_blocked_hosts_og.txt', 'w') as handle:
            handle.write(result)
if __name__=='__main__':
    main()

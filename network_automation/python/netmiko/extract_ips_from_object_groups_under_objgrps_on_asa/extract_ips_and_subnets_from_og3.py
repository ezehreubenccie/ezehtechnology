#!/usr/bin/env python3


from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import pprint
import getpass
import re

obj_net_grp_list = []
obj_net_grp = []
pattern1 = re.compile(r'network-object\s\d\d.\d.\d.\d\s')
pattern2 = re.compile(r'network-object\sobject')
pattern3 = re.compile(r'^\d\d.\d.\d.\d\s')
pattern4 = re.compile(r'\d\d')
#def get_og(file):
with open('hosts3.yml', 'r') as handle:
    host_root = safe_load(handle)
    print(host_root)
    platform_map = {'asa': 'cisco_asa'}

with open('object_ids.txt', 'r') as objs:
    objects = objs.read() 
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
            session_log='netmiko8.log'  
        )
        
        print(f'Logged into {conn.find_prompt()} successfully')
#        print(objects.splitlines())
        for object in objects.splitlines():
            if pattern1.search(object):
                field1 = object.split()[1]
                field2 = object.split()[2]
#                result = conn.send_command(f'sh run object id {field2}')
                obj_net_grp_list.append(f'{field1} {field2}')

            if pattern2.search(object):
                field2 = object.split()[2]
                result = conn.send_command(f'sh run object id {field2}')

#                print(result)
                obj_net_grp_list.append(result)
            if 'group-object' in object:
                field1 = object.split()[1]
                result = conn.send_command(f'sh run object-group id {field1}')
                obj_net_grp_list.append(result)
#            else:
#                field1 = object.split()[1]
#                obj_net_grp_list.append(field1)
        pprint.pprint(obj_net_grp_list)
        print(len(obj_net_grp_list))
#        print(' ' + 'subnet' + ' ' + '10.2.0.0 255.255.0.0')
        for entry in obj_net_grp_list:
#            print(f'{field1} {field2}')
            if pattern3.search(entry):
                fields = entry.split()
                field1 = fields[0]
                field2 = fields[1]
                print(f' {field1} {field2}')
                obj_net_grp.append(f' {field1} {field2}')
#            print(len(entry.split('\n')))
            elif len(entry.split('\n')) == int(3):
                fields = entry.split('\n')
                field1 = fields[1]
                field2 = fields[2]
                print(f'{field1}')
                print(f'{field2}')
                obj_net_grp.append(f' {field1}\n{field2}')
            else:
                fields = entry.split('\n')
                field1 = fields[1]
                print(field1)
                obj_net_grp.append(field1)
##
        pprint.pprint(obj_net_grp)
        conn.disconnect()
#        print(obj_net_grp)
#        print(len(obj_net_grp))
#        print(f"Writing {host['name']} facts to file")
#        with open(f'{host["name"]}_usap_serv_sub_hosts_og.txt', 'w') as handle:
#            handle.write(result)
#    return f'{host["name"]}_usap_serv_sub_hosts_og.txt'
#
#if __name__=='__main__':
#    hosts = 'hosts3.yml'
#    get_og(hosts)

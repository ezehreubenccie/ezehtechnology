#!/usr/bin/env python3


from conn_to_asa_and_read_og import get_og
import pprint
import re

def main():
    hosts = 'hosts3.yml'
    file = get_og(hosts)
    ip_obj_list = []
    print('file is:')
    print(file)
    with open(file, 'r') as handle:
        output = handle.read()
    print('output is:')
    print(output)
    print(output.splitlines())
    for subnet in output.splitlines()[1:]:
        print(subnet)
        ip_obj_list.append(subnet)

    file = 'object_ids.txt'
    print(f'Write object Ids  to {file}')
    print(f'ip_obj_list is {ip_obj_list}')
    with open(file, 'w') as f:
        for ip in ip_obj_list:
            f.write(ip)
            f.write('\n')

if __name__=='__main__':
    main()

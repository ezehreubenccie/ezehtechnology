#!/usr/bin/env python3


from netmiko8 import get_og
import pprint
import re

def main():
    hosts = 'hosts3.yml'
    file = get_og(hosts)
    ip_obj_list = []
    print(file)
    with open(file, 'r') as handle:
        output = handle.read()
#    print(output.splitlines())
#    output = output.splitlines()[1:-1]
#    print(output)
#    pattern1 = re.compile(r'network-object\s(object|host)')

    for subnet in output.splitlines()[1:-1]:
        print(subnet)
        ip_obj_list.append(subnet)
#        mo = pattern1.search(subnet)
#        print(mo)
#        if 'network-object host' in subnet or 'network-object object' in subnet:
#            field0 = subnet.split()[0]
#            field1 = subnet.split()[1]
#            field2 = subnet.split()[2]
#            ip_addr_list.append(field2)
#        print(field2)
#        print(subnet)
#        if 'group-object' in subnet:
#            field1 = subnet.split()[1]
#            ip_addr_list.append(subnet)
#        else:
#            field1 = subnet.split()[1]
#            field2 = subnet.split()[2]
#            ip_addr_list.append(field1 + ' ' + field2)
#    pprint.pprint(ip_addr_list)

    file = 'object_ids.txt'
    print(f'Write object Ids  to {file}')
    with open(file, 'w') as f:
        for ip in ip_obj_list:
            f.write(ip)
            f.write('\n')

if __name__=='__main__':
    main()

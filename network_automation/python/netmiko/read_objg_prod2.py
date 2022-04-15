#!/usr/bin/env python3


from netmiko7 import get_og
import pprint
import re

def main():
    hosts = 'hosts3.yml'
    file = get_og(hosts)
    ip_addr_list = []
    print(file)
    with open(file, 'r') as handle:
        output = handle.read()
#    print(output.splitlines())
#    output = output.splitlines()[1:-1]
#    print(output)
#    pattern1 = re.compile(r'network-object\s(object|host)')

    for subnet in output.splitlines()[1:-1]:
        print(subnet)
#        mo = pattern1.search(subnet)
#        print(mo)
        if 'network-object host' in subnet or 'network-object object' in subnet:
            field0 = subnet.split()[0]
            field1 = subnet.split()[1]
            field2 = subnet.split()[2]
            ip_addr_list.append(field2)
#        print(field2)
#        print(subnet)
        else:
            field1 = subnet.split()[1]
            field2 = subnet.split()[2]
            ip_addr_list.append(field1 + ' ' + field2)
    pprint.pprint(ip_addr_list)
    file = 'local_ip_usap_addresses.txt'
    print(f'Write IPs to text to {file}')
    with open(file, 'w') as f:
        for ip in ip_addr_list:
            f.write(ip)
            f.write('\n')
if __name__=='__main__':
    main()

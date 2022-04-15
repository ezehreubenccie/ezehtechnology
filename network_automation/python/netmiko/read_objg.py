#!/usr/bin/env python3


from netmiko6 import get_og

def main():
    hosts = 'hosts2.yml'
    file = get_og(hosts)
#    print(file)
    with open(file, 'r') as handle:
        output = handle.read()
#    print(output.splitlines())
##    output = output.splitlines()[1:-1]
#    print(output)
    for subnet in output.splitlines()[1:-1]:
        field0 = subnet.split()[0]
        field1 = subnet.split()[1]
        field2 = subnet.split()[2]
        print(field2)
#        print(subnet)

if __name__=='__main__':
    main()

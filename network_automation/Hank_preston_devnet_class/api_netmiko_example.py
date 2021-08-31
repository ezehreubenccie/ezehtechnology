#!/usr/bin/env python

from netmiko import ConnectHandler
from pprint import pprint


router = {'device_type': 'cisco_ios',
          'host': 'lbjlabrouter01',
          'port': 22,
          'user': 'reuben',
          'pass': 'cisco'}

net_connect = ConnectHandler(ip=router['host'],
                             port=router['port'],
                             username=router['user'],
                             password=router['pass'],
                             device_type=router['device_type'])

interface_cli = net_connect.send_command('show run int G0/0/0')
pprint(interface_cli)

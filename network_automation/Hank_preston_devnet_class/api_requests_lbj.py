#!/usr/bin/env python

import requests
from pprint import pprint

router = {'ip': 'dtx-lbj-4331-rtr01',
          'port': '443',
          'user': 'usapadmin',
          'pass': 'T3nb5li1kp#Ds!@'}

headers = {'Accept': 'application/yang-data+json'}

u = 'https://{}:{}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=0%2F0%2F2'

u = u.format(router['ip'], router['port'])

r = requests.get(u, headers=headers, auth=(router['user'], router['pass']), verify=False)

pprint(r.text)
api_data = r.json()
pprint(api_data)
#interface_name = api_data['Cisco-IOS-XE-native:GigabitEthernet']['name']
#print(interface_name)

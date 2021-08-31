#!/usr/bin/env python

from ncclient import manager
from pprint import pprint
import xmltodict


router = {'ip': 'lbjlabrouter01',
          'port': 830,
          'user': 'reuben',
          'pass': 'cisco'}

netconf_filter = '''
<filter>
  <interfaces xmlns='urn:ietf:params:xml:ns:yang:ietf-interfaces'>
    <interface>
      <name>GigabitEthernet0/0/0</name>
    </interface>
  </interfaces>
</filter>'''

m = manager.connect(host=router['ip'],
                    port=router['port'],
                    username=router['user'],
                    password=router['pass'],
                    device_params={'name':'iosxe'},
                    hostkey_verify=False)

#print(m)
interface_netconf = m.get_config('running', netconf_filter)
#pprint(interface_netconf.xml)
interface_python = xmltodict.parse(interface_netconf.xml)['rpc-reply']['data']
pprint(interface_python)
#pprint(interface_python['interfaces']['interface']['name']['#text'])

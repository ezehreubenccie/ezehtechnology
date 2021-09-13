#!/usr/bin/env python

from device_info import ios_xe
from ncclient import manager
import xml.dom.minidom
from pprint import pprint

# NETCONF filter to use
with open('filter-ietf-interfaces.xml') as f:
    netconf_filter = f.read()

if __name__== "__main__":
    with manager.connect(host=ios_xe["address"], 
                         username=ios_xe["username"],
                         password=ios_xe["password"],
                         hostkey_verify=False) as m:
 
        netconf_reply = m.get_config("running", netconf_filter)
        pprint(netconf_reply.xml)
#        print(type(netconf_reply.xml))
        interfaces = xml.dom.minidom.parseString(netconf_reply.xml)
        print(interfaces)
#        print(type(interfaces))
        interfaces = interfaces.getElementsByTagName("interfaces")
#        print(interfaces)
        print(interfaces[0].toprettyxml())

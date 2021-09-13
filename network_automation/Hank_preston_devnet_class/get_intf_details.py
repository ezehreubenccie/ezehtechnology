#!/usr/bin/env python

from device_info import ios_xe
from ncclient import manager
import xmltodict
from pprint import pprint

# NETCONF filter to use
with open('filter-ietf-interfaces_2.xml') as f:
    netconf_filter = f.read()

#print(netconf_filter)
if __name__== "__main__":
    with manager.connect(host=ios_xe["address"], 
                         username=ios_xe["username"],
                         password=ios_xe["password"],
                         hostkey_verify=False) as m:
       
        # Get Configuration and State Info for Interface
        netconf_reply = m.get(netconf_filter)
#        print(netconf_reply)

        # Process the XML and store useful dictionaries
        intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
#        pprint(intf_details)
        intf_config = intf_details["interfaces"]["interface"]
#        pprint(intf_config)
        intf_info = intf_details["interfaces-state"]["interface"]

        print("")
        print("Interface Details:")
        print("  Name: {}".format(intf_config["name"]["#text"]))
        print("  Description: {}".format(intf_config["description"]))
        print("  Type: {}".format(intf_config["type"]["#text"]))
        print("  Mac Address: {}".format(intf_info["phys-address"]))
        print("  Packets Input: {}".format(intf_info["statistics"]["in-unicast-pkts"]))
        print("  Packets Output: {}".format(intf_info["statistics"]["out-unicast-pkts"]))


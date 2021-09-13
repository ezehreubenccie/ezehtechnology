#!/usr/bin/env python


__author__ = "Reuben Ezeh"
__Title__ = "Senior Network Engineer"
__email__ = "ezehreubenccie@gmail.com"


from device_info import ios_xe
from ncclient import manager


# NETCONF Config Template to use
with open("config-temp-ietf-interfaces.xml") as f:
    netconf_template = f.read()

if __name__ == "__main__":
    # Build the XML Configuration to send
    netconf_payload = netconf_template.format(intf_name="GigabitEthernet0/0/0",
                                              intf_desc="Configured by Reuben using NETCONF",
                                              ip_address="10.2.2.2",
                                              subnet_mask="255.255.255.0"
                                              )

    print("Configuration Payload:")
    print("----------------------")
    print(netconf_payload)

    with manager.connect(host=ios_xe["address"],
                         username=ios_xe["username"],
                         password=ios_xe["password"],
                         hostkey_verify=False) as m:

        # Send NETCONF <edit-config>
        netconf_reply = m.edit_config(netconf_payload, target="running")

        # Print the NETCONF Reply
        print(netconf_reply)

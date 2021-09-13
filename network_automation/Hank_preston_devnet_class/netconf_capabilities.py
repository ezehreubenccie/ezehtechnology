#!/usr/bin/env python

from ncclient import manager
from device_info import ios_xe

if __name__ == "__main__":

    with manager.connect(host=ios_xe["address"],
                         username=ios_xe["username"],
                         password=ios_xe["password"],
                         hostkey_verify=False) as m:

        print("Here are the NETCONF Capabilities")
        for capabilities in m.server_capabilities:
            print(capabilities)


#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Demonstrate SCP file transfer using Netmiko
"""


import sys
from yaml import safe_load
from netmiko import Netmiko, file_transfer



def main(argv):
    """
    Execution starts here
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Netmiko uses "cisco_nxos" instead of "nxos" and
    # "cisco_ios" instead of "ios", so use a mapping dict to convert
    platform_map = {"nxos": "cisco_nxos", "ios": "cisco_ios", "asa": "cisco_asa", "iosxe": "cisco_iosxe"}

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["host_list"]:
        # Use the map to get the proper Netmiko platform
        platform = platform_map[host["platform"]]

        # Initialize the SSH connection
        print(f"Connecting to {host['name']}")
        conn = Netmiko(
            host=host["name"],
            username="",
            password="",
            device_type=platform,
        )

        # Upload the file specified. The dict.get(key) function tries
        # to retrieve the value at the specified key and returns None
        # if it does not exist, very useful in network automation!
        print(f"  Uploading {argv[1]}")
        result = file_transfer(
            conn,
            source_file=argv[1],
            dest_file=argv[1],
            file_system=host.get("file_system"),
        )

        # Print the resulting details
        print(f"  Details: {result}\n")
        conn.disconnect()


if __name__ == "__main__":
    main(sys.argv)

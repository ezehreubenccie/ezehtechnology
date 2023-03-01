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
    # breakpoint()
    # Read the hosts file into structured data, may raise YAML Error
    with open("hosts/labasafirewalls/labasafirewalls.yml", "r") as handle:
        host_root = safe_load(handle)

    # Netmiko uses 'cisco_asa' instead of 'asa'
    platform_map = {"asa": "cisco_asa"}

    # Iterate over the list of hosts (list of dictionaries)
    host = host_root["host_list"][0]

    # Use the map to get proper Netmiko platform
    platform = platform_map[host["platform"]]

    with open("vars/labasafirewalls.yml", "r") as handle:
        creds = safe_load(handle)
        creds = creds['labasafirewalls']
    print(creds)
    # Create netmiko SSH connection handler to access the device
    print(f"connecting to {host['name']}")
    conn = Netmiko(
        host=host["name"],
        username=creds["username"],
        password=creds["password"],
        secret=creds["secret"],
        device_type=platform,
    )

    # Upload the file specified. The dict.get(key) function tries
    # to retrieve the value at the specified key and returns None
    # if it does not exist. Very useful in Network automation!
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

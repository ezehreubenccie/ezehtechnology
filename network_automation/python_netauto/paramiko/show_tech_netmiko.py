#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Demonstrate using SSH via netmiko to configure network devices.
"""

from yaml import safe_load
from netmiko import Netmiko
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import time

date1 = datetime.today()


def main():
    """
    Execution starts here.
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Netmiko uses "cisco_nxos" instead of "nxos" and
    # "cisco_ios" instead of "ios", so use a mapping dict to convert
    platform_map = {"nxos": "cisco_nxos", "ios": "cisco_ios"}

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["host_list"]:
        # Use the map to get the proper Netmiko platform
        platform = platform_map[host["platform"]]


        # Create netmiko SSH connection handler to access the device
        conn = Netmiko(
            host=host["name"],
            username="reuben",
            password="cisco",
            device_type=platform,
        )

        command = "show tech-support"
        print(f"Logged into {conn.find_prompt()} successfully")

        # Send the configuration string to the device. Netmiko
        # takes a list of strings, not a giant \n-delimited string,
        # so use the .split() function
       # print(vlan_cfg_chg)
       # time.sleep(5.0)
        print("Collecting show tech info!")
        with open(
            f"changes/{host['name']}_{date1.month}_{date1.day}_{date1.year}_{date1.hour}_{date1.minute}_{date1.second}.txt",
            "w",
        ) as handle:
            handle.write("\n")
            handle.write(command)
        result = conn.send_command(command, read_timeout=180)

        # Netmiko automatically collects the results; you can ignore
        # or process them further
        with open(
            f"changes/{host['name']}_{date1.month}_{date1.day}_{date1.year}_{date1.hour}_{date1.minute}_{date1.second}.txt",
            "a",
        ) as handle:
            handle.write("\n")
            handle.write(result)

        conn.disconnect()


if __name__ == "__main__":
    main()

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
    platform_map = {"nxos": "cisco_nxos"}

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["host_list"]:
        # Use the map to get the proper Netmiko platform
        platform = platform_map[host["platform"]]

        # Load the host-specific vlans declarative state
        with open(f"vars/{host['name']}_vlans.yml", "r") as handle:
            vlans = safe_load(handle)

        # Setup the jinja2 templating environment and render the template
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template(f"templates/netmiko/{platform}_vlans.j2")
        vlan_cfg_chg = template.render(data=vlans)

        # Create netmiko SSH connection handler to access the device
        conn = Netmiko(
            host=host["name"],
            username="reuben",
            password="cisco",
            device_type=platform,
        )

        print(f"Logged into {conn.find_prompt()} successfully")

        # Send the configuration string to the device. Netmiko
        # takes a list of strings, not a giant \n-delimited string,
        # so use the .split() function
        print(vlan_cfg_chg)
        time.sleep(5.0)
        print("Copying changes to be applied to file")
        with open(
            f"changes/{host['name']}_{date1.month}_{date1.day}_{date1.year}_{date1.hour}_{date1.minute}_{date1.second}.txt",
            "w",
        ) as handle:
            handle.write("changes to be applied.\n")
            handle.write(vlan_cfg_chg)
        result = conn.send_config_set(vlan_cfg_chg.split("\n"))

        # Netmiko automatically collects the results; you can ignore
        # or process them further
        with open(
            f"changes/{host['name']}_{date1.month}_{date1.day}_{date1.year}_{date1.hour}_{date1.minute}_{date1.second}.txt",
            "w",
        ) as handle:
            handle.write("changes implemented!\n")
            handle.write(result)

        conn.disconnect()


if __name__ == "__main__":
    main()

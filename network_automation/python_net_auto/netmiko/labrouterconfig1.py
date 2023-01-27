#!/usr/bin/env python3


"""
Author: Reuben Ezeh
purpose: Test
"""

from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader


def main():
    """
    Execution starts here.
    """
    
    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts/hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Netmiko uses "cisco_ios" instead of "ios"
    platform_map = {"ios": "cisco_ios"}

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["host_list"]:

        # Use the map to get proper Netmiko platform
        platform = platform_map[host["platform"]]
        # Load the host-specific vars/configs
        with open(f"vars/{host['name']}.yml", "r") as handle:
            intf = safe_load(handle)

        # Setup the jinja2 templating environment and render the template
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template(f"jinja/labrouters/{platform}.j2")


        new_config = template.render(data=intf)

#        # Create netmiko SSH connection handler to access the device
        conn = Netmiko(
            host=host["name"],
            username="reuben",
            password="cisco",
            device_type=platform,
        )

        
        print(f"logged into {conn.find_prompt()} successfully")
        
        # Send configuration string to the device. Netmiko
        # takes a list of strings, not a giant \n-delimited string,
        # so use the split() function

        result = conn.send_config_set(new_config.split("\n"))

        # Netmiko automatically collects the results; you can ignore them
        # or process them further
        print(result)

        conn.disconnect()


if __name__ == "__main__":
    main()

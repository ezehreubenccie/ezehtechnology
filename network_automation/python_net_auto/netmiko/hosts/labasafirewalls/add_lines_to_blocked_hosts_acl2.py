#!/usr/bin/env python

"""
Author: Reuben Ezeh
Purpose: Block malicious IP using python script as an alternative to solarwinds.
"""

from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader


def main():
    """
    Execution starts here
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    platform = "cisco_asa"

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["host_list"]:
        # load the variables for the template file
        with open("vars/mal_ip.yml", "r") as handle:
            mal_ip = safe_load(handle)

        # Setup the jinja2 templating environment and render the template
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template("templates/block_ip_config.j2")

        config = template.render(data=mal_ip)

        # Create netmiko SSH connection handler to access the device
        conn = Netmiko(
            host=host["name"],
            username="reuben",
            password="cisco",
            secret="cisco",
            device_type=platform,
        )

        print(f"Logged into {conn.find_prompt()} successfully")

        # Send the configuration string to the device, Netmiko
        # takes a list of strings, not a giant \n-delimiter string,
        # so use the .split() function
        result = conn.send_config_set(config.split("\n"))

        # Netmiko automatically collects the results; you can ignore them
        # or process them further
        print(result)

        conn.disconnect()


if __name__ == "__main__":
    main()

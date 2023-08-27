#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Demonstrate using NAPALM via SSH to interact with multiple
nxos devices to collect structured data
"""

from napalm import get_network_driver
from jinja2 import Environment, FileSystemLoader
from yaml import safe_load
from parse_nxos_vlans_6 import parse_vlan_nxos, vlan_diff


def main():
    """
    Execution starts here.
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Iterate over the list of hosts from the YAML file
    for host in host_root["host_list"]:
        # Determine and create the network driver object based on platform
        print(f"Getting {host['platform']} driver")
        driver = get_network_driver(host["platform"])
        conn = driver(hostname=host["name"], username="reuben", password="cisco")

        # Open the connection and get the model ID
        print("Opening connection and gathering facts")
        conn.open()
        facts = conn.get_facts()
        # print(facts)
        print(f"{host['name']} model type: {facts['model']}")

        # Run the proper show command and perform parsing
        output = conn.cli([host["vlan_cmd"]])
        # print(output)
        vlan_data = parse_vlan_nxos(output[host["vlan_cmd"]])

#        print(vlan_data)
        # Read the YAML file into structured data, may raise YAMLError
        with open(f"vars/{host['name']}_vlans.yml", "r") as handle:
            vlans = safe_load(handle)

        # Find the differnce in VLANs between intended and actual config
        vlan_updates = vlan_diff(vlans, vlan_data)

        print(vlan_updates)

        # Template the configuration changes based on the VLAN updates
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template(f"templates/sett/{host['platform']}_vlans.j2")
        vlan_cfg_chg = template.render(data=vlan_updates)

        # Use NAPALM built-in merging to compare and merge VLAN updates
        # Note that dynamically removing configuration is still a challenge
        # unless NAPLAM is explicitly told ...
        conn.load_merge_candidate(config=vlan_cfg_chg)
        diff = conn.compare_config()
        # print(diff)
        if diff:
            print(diff)
            print("Commiting configuration changes")
            conn.commit_config()
        else:
            print("no diff; config up to date")

        # ALl done; close the connection
        conn.close()
        print("OK!\n")


if __name__ == "__main__":
    main()

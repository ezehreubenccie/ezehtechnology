#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Demonstrate using nornir to introduce orchestration and
concurrency, as well as inventory management
"""

import logging
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_napalm.plugins.tasks import (
    # napalm_cli,
    napalm_get,
    napalm_configure,
)
from nornir_utils.plugins.tasks.text import template_file
from nornir_utils.plugins.functions import print_result
from parse_nxos_vlans_6 import vlan_diff, parse_vlan_nxos


def manage_vlan(task):
    """
    Grouped task does 4 things:
    1. Gather facts with NAPALM
    2. Gather VLAN configuration with with Netmiko
    3. Locally render VLAN config template
    4. Configure VLAN updates with NAPALM
    """

    # TASK 1: Gather facts using NAPALM to get model ID
    task1_result = task.run(task=napalm_get, getters=["get_facts"])
    model = task1_result[0].result["get_facts"]["model"]
    print(f"{task.host.name}: connected as model type {model}")

    # TASK 2: Collect the VLAN running configuration using netmiko
    task2_result = task.run(
        task=netmiko_send_command, command_string=task.host["vlan_cmd"]
    )
    cmd_output = task2_result[0].result

    # ALTERNATIVE IMPLEMENTATION: Can use napalm_cli just as easily,
    # but using netmiko and NAPALM together highlights Nornir's flexibility
    # task2_result = task.run(task=napalm_cli, commands=[task.host["vrf_cmd"]])
    # cmd_output = task2_result[0].result[task.host["vrf_cmd"]]

    # Determine the parser and perfrom parsing
    vlan_data = parse_vlan_nxos(cmd_output)
    vlan_updates = vlan_diff(task.host["vlans"], vlan_data)

    # TASK 3: Create the template of config to add
    task3_result = task.run(
        task=template_file,
        template=f"{task.host.platform}_vlans.j2",
        path="templates/",
        data=vlan_updates,
    )
    vlan_chg_cfg = task3_result[0].result

    # TASK 4: Configure the devices using NAPALM and print any updates
    task4_result = task.run(task=napalm_configure, configuration=vlan_chg_cfg)
    if task4_result[0].diff:
        print(f"{task.host.name}: diff below\n{task4_result[0].diff}")
    else:
        print(f"{task.host.name}: no diff; config up to date")


def main():
    """
    Execution begins here.
    """

    # Initialize nornir, nothing new yet.
    nornir = InitNornir()

    # We can run arbitrary Python code, so let's just print the
    # hostnames loaded through the inventory, which are dict keys.
    print("Nornir initialized with inventory hosts:")
    for host in nornir.inventory.hosts.keys():
        print(host)

    # Invoke the grouped task.
    result = nornir.run(task=manage_vlan)

    # Use Nornir-supplied function to pretty-print the result
    # to see a recap of all actions taken. Standard Python logging
    # levels are supported to set output verbosity.
    print_result(result, severity_level=logging.WARNING)


if __name__ == "__main__":
    main()

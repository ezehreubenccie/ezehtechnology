#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Demonstrate using SSH via paramiko to configure network devices.
"""

import time
import paramiko
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader


def send_cmd(conn, command):
    """
    Given an open connection and a command, issue the command and wait
    1 second for the command to be processed.
    """
    output = conn.send(command + "\n")
    time.sleep(10.0)
    return output


def get_output(conn):
    """
    Given an open connection, read all the data from the buffer and
    decode the byte string as UTF-8.
    """
    return conn.recv(65535).decode("utf-8")


def main():
    """
    Execution starts here
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["host_list"]:
        # load the host-specific VLAN declarative state
        with open(f"vars/{host['name']}_vlans.yml", "r") as handle:
            vlans = safe_load(handle)

        # Setup the jinja2 templating environment and render the template
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template(f"templates/paramiko/{host['platform']}_vlans.j2")
        vlan_cfg_chg = template.render(data=vlans)

        # Create paramiko SSH client to connect to the device
        conn_params = paramiko.SSHClient()
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        conn_params.connect(
            hostname=host["name"],
            port=22,
            username="reuben",
            password="cisco",
            look_for_keys=False,
            allow_agent=False,
        )

        # Start an interactive shell and collect the prompt
        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f"logged into {get_output(conn).strip()} successfully")

        # Send the configuration string to the device
        print(vlan_cfg_chg)
        send_cmd(conn, vlan_cfg_chg)
        print(f"Updated {host['name']} VLAN configuration")
        conn.close()


if __name__ == "__main__":
    main()

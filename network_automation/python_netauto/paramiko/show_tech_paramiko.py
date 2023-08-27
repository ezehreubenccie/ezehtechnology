#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Demonstrate using SSH via paramiko to configure network devices.
"""

import time
from datetime import datetime
import paramiko
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader

date1 = datetime.today()

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
        
        command = "show tech-support"
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
        print(command)
        time.sleep(5.0)
        print("Collecting show tech-support!")
        with open(f"changes/show_tech_{host['name']}_{date1.month}_{date1.day}_{date1.year}_{date1.hour}_{date1.minute}_{date1.second}.txt", "w") as handle:
            
            handle.write(command)
        send_cmd(conn, command)
        output = get_output(conn)
        time.sleep(600.0)
        print(output)
        with open(
            f"changes/show_tech_{host['name']}_{date1.month}_{date1.day}_{date1.year}_{date1.hour}_{date1.minute}_{date1.second}.txt",
            "a",
        ) as handle:
            handle.write("\n")
            handle.write(output)
        print(f"Collected {host['name']} show tech-support information")
        conn.close()


if __name__ == "__main__":
    main()

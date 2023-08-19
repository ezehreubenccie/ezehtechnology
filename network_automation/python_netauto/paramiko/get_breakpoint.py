#!/usr/bin/env python

"""
Author: Reuben Ezeh
Purpose: Demonstrate using SSH via paramiko to get information from
the network and print it to the screen
"""

import time
import paramiko


def send_cmd(conn, command):
    """
    Given an open connection and a command, issue the command and wait
    1 second for the command to be processed.
    """
    conn.send(command + "\n")
    time.sleep(10.0)


def get_output(conn):
    """
    Given an open connection, read all the data from the buffer and
    decode the byte string as UTF-8.
    """
    return conn.recv(65535).decode("utf-8")


def main():
    """
    Execution starts here.
    """

    # Define host inventory in line. Remember our platform types:
    # nxos1 is a Cisco NXOS nxos9000
    # nxos2 is a Cisco NXOS nxos9000
    # r1 is a Cisco CSR1000v
    host_dict = {
        "nxos1": "show running-config | grep vlan",
        "nxos2": "show running-config | grep vlan",
        "r1": "show running-config | sec interface"
    }

    # for each host in the inventory dict, extract key and value
    for hostname, device_cmd in host_dict.items():
        # Paramiko can be SSH client or server; use client here
        conn_params = paramiko.SSHClient()

        # We don't need paramiko to refuse connections due to missing SSH keys
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn_params.connect(
            hostname=hostname,
            port=22,
            username="reuben",
            password="cisco",
            look_for_keys=False,
            allow_agent=False,
        )

        # Get and interactive shell and wait a bit for the prompt to appear
        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f"Logged into {get_output(conn).strip()} successfully")

        # Iterate over the list of commands, sending each one in series
        # The final command in the list is the OS-specific commands
        commands = [
            "terminal length 0",
            "show version | in Saft",
            device_cmd,
        ]
        concat_output = ""
        for command in commands:
            # It helps to have a custom function to abstract sending
            # commands and reading output from the device
            breakpoint()
            send_cmd(conn, command)
            concat_output += get_output(conn)
            #print(get_output(conn))

        # Close session when we are done
        conn.close()

        # Open a new text file per host and write the output
        print(f"Writing {hostname} facts to file")
        with open(f"{hostname}_facts.txt", "w") as handle:
            handle.write(concat_output)

if __name__ == "__main__":
    main()


#!/usr/bin/env python3


import time
import paramiko
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader


def send_cmd(conn, command):
    """
    Given an open connection and a command, issue the command and wait
    1 second for the command to be processed.
    """
    conn.send(command + "\n")
    time.sleep(1.0)


def get_output(conn):
    """
    Given  an open connection, read all the data from the buffer and decode
    the byte string as UTF-8.
    """
    return conn.recv(65535).decode("utf-8")


def main():

    with open("hosts.yml", "r") as handle:
        net_devices = safe_load(handle)
        print(net_devices)

    for host in net_devices["host_list"]:

        with open(f"vars/{host['name']}.yml", "r") as handle:
            ints = safe_load(handle)
            print(ints)
            print(ints["creds"][0])

        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )

        template = j2_env.get_template(f"templates/{host['platform']}.j2")

        config = template.render(data=ints)
        conn_params = paramiko.SSHClient()

        # Ignore any untrusted keys. Not recommended in production env
        conn_params.set_missing_host_key_policy(
            paramiko.AutoAddPolicy
        )  # so that paramiko doesnt reject the connection because of missing keys
        conn_params.connect(
            hostname=host["name"],
            port=22,
            username=ints["creds"][0]["username"],
            password=ints["creds"][0]["password"],
            look_for_keys=False,
            allow_agent=False,  # Don't use any local ssh agents
        )

        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f"Logged into {get_output(conn).strip()} successfully")

        print(config)
        enable_secret = ints["creds"][0]["enable"]
        commands = ["enable", enable_secret]
        send_cmd(conn, commands[0])
        send_cmd(conn, commands[1])
        send_cmd(conn, config)

        print(f"Configuration sent to {host['name']}")
        conn.close()


if __name__ == "__main__":
    main()

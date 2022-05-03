#!/usr/bin/env python3


import time
import paramiko


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
    host_dict = {
        "labasa1": "show run | grep access-l",
    }

    for hostname, cmd in host_dict.items():
        conn_params = paramiko.SSHClient()

        # Ignore any untrusted keys. Not recommended in production env
        conn_params.set_missing_host_key_policy(
            paramiko.AutoAddPolicy
        )  # so that paramiko doesnt reject the connection because of missing keys
        conn_params.connect(
            hostname=hostname,
            username="reuben",
            password="cisco",
            look_for_keys=False,
            allow_agent=False,  # Don't use any local ssh agents
        )

        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f"Logged into {get_output(conn).strip()} successfully")

        commands = ["enable", "cisco", "terminal pager 0", "show version | GREP SOFTWARE", cmd]
        concat_output = ''

        for command in commands:
#            breakpoint()
            send_cmd(conn, command)
            concat_output += get_output(conn)
            #print(get_output(conn))

        conn.close()  # Close session when we are done
        print(f'Writing {hostname} output to file')
        with open(f'{hostname}_output.txt', 'w') as handle:
            handle.write(concat_output)

if __name__=='__main__':
    main()

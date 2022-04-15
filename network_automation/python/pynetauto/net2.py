#!/usr/bin/env python3

import time, paramiko


def send_cmd(conn, command):
    conn.send(command + '\n')
    time.sleep(1.0)

def get_output(conn):
    return conn.recv(65535).decode('utf-8')

def main(): 
    host_dict = {'labasa1': 'show run nat'}
    enable = 'cisco'
    for hostname, cmd in host_dict.items():
        conn_params = paramiko.SSHClient()
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn_params.connect(hostname=hostname,
                            port=22,
                            username='reuben',
                            password='cisco',
                            enable=enable,
                            look_for_keys=False,
                            allow_agent=False,
        )

        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f'Logged into {get_output(conn).strip()} successfully')

        commands = ['term pager 0', 'show version | inc Software', cmd]

        for command in commands:
            send_cmd(conn, command)
            print(get_output(conn))
        conn.close()

if __name__=='__main__':
    main() 


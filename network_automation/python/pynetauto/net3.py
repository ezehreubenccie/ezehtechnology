#!/usr/bin/env python3

import time, paramiko


def send_cmd(conn, command):
    conn.send(command + '\n')
    time.sleep(1.0)

def get_output(conn):
    return conn.recv(65535).decode('utf-8')

def main(): 
    host_dict = {'lbjlabrouter02': 'show ip int brie', 'lbjlabrouter01': 'show run vrf'}

    for hostname, cmd in host_dict.items():
        conn_params = paramiko.SSHClient()
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn_params.connect(hostname=hostname,
                            port=22,
                            username='reuben',
                            password='cisco',
                            look_for_keys=False,
                            allow_agent=False,
        )

        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f'Logged into {get_output(conn).strip()} successfully')

        commands = ['term length 0', 'show version | inc Software,', cmd]
        concat_output = ''
        for command in commands:
            send_cmd(conn, command)
            concat_output += get_output(conn)
            #print(get_output(conn))
        conn.close()
        
        print(f'Writing {hostname} facts to file')
        with open(f'{hostname}_facts.txt', 'w') as handle:
            handle.write(concat_output)

if __name__=='__main__':
    main() 


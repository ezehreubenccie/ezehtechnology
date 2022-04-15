#!/usr/bin/env python3

from netmiko import ConnectHandler
from getpass import getpass
import time


time.sleep(4)

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="lbjlabrouter01",
    username="reuben",
    password=getpass(),
    session_log='lbjlabrouter1.log'
)
print(net_connect.find_prompt())
output = net_connect.send_command('show ip int brief')
print(output)
net_connect.disconnect()

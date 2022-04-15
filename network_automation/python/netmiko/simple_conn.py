#!/usr/bin/env python3

from netmiko import ConnectHandler
from getpass import getpass

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="lbjlabrouter01",
    username="reuben",
    password=getpass(),
)
print(net_connect.find_prompt())

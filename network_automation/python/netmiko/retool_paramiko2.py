#!/usr/bin/env python3


from netmiko import Netmiko
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader


def main():

    with open("hosts.yml", "r") as handle:
        net_devices = safe_load(handle)
        print(net_devices)

    # Netmiko uses platform of cisco_ios, cisco_asa, instead if ios and asa
    # so use a mapping dict to convert

    platform_map = {"asa": "cisco_asa"}

    for host in net_devices["host_list"]:

        platform = platform_map[host["platform"]]
#        print(platform)
        with open(f"vars/{host['name']}.yml", "r") as handle:
            ints = safe_load(handle)
#            print(ints)
#            print(ints["creds"][0])

        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )

        template = j2_env.get_template(
            f"templates/{host['name']}/{platform}.j2"
        )

        config = template.render(data=ints)
        username = ints["creds"][0]["username"]
        password = ints["creds"][0]["password"]
        enable_secret = ints["creds"][0]["enable"]
        conn = Netmiko(
            host=host["name"],
            port=22,
            username=username,
            password=password,
            secret=enable_secret,
            session_log="retool_paramiko2.log",
            device_type=platform,
        )

        print(f"Logged into {conn.find_prompt()} successfully")
        print(f"The configuration below will be sent to {host['name']}")
        print(config)

        result = conn.send_config_set(config.split("\n"))
        print(result)

#        print(f"Configuration sent to {host['name']}")
        conn.disconnect()


if __name__ == "__main__":
    main()

def asa_devices_to_upgrade():
    with open('asa_5506x_devices.txt', 'r') as f:
        file_content = f.read().splitlines()

    devices = list()

    for item in file_content:
        tmp = item.split(',')
        devices.append(tmp)


    for asa in devices:
        asa_firewall = {'device_type': 'cisco_asa',
                  'ip': asa[3],
                  'port': '22',
                  'username': asa[0],
                  'password': asa[1],
                  'secret': asa[2],
                  'verbose': 'True'
                  }
        return asa_firewall

#dict1 = asa_devices_to_upgrade()
#print(dict1)
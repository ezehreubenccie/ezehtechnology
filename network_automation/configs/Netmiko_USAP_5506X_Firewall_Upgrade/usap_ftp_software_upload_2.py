from netmiko import ConnectHandler
import sys
from getpass import getpass
import time
from datetime import datetime
start_time = datetime.now()
print(">>>> {}".format(start_time))
start = time.time()
#host = input('Enter ip address: ')
ftp_user = 'reuben'
ftp_pass = 'cisco'
ftp_ip = '10.7.250.54'
target_software = 'asa964-41-lfbff-k8.SPA'
#device = {'device_type': 'cisco_asa',
#          'host': host,
#          'username':'reuben',
#          'password':'cisco',
#          'port': '22',
#          'secret': 'cisco',
#          'verbose': True}
def usap_ftp_software_upload(**device):
    global ftp_user
    global ftp_pass
    global ftp_ip
    global target_software
    net_connect = ConnectHandler(**device)
    prompt = net_connect.find_prompt()
    hostname = prompt[0:-1]

    check = f'show disk0: | grep {target_software}'
    check_output = net_connect.send_command(check)
    if target_software not in check_output:
        cmd = f'copy ftp://{ftp_user}:{ftp_pass}@{ftp_ip}/{target_software}  ' f'disk0:/{target_software}'
        # expect_string = (r'Source filename', r'Destination filename')
        output = net_connect.send_command(cmd, expect_string=r'Address or name of remote host')
        # output = net_connect.send_command_expect(cmd, 'Source filename', 'Destination filename')
        # if 'Source filename' in output:
        #    output += net_connect.send_command('\n')
        # if 'Destination filename' in output:
        #    output += net_connect.send_command('\n')
        output += net_connect.send_command('\n', expect_string=r'Source username')
        output += net_connect.send_command('\n', expect_string=r'Source password')
        output += net_connect.send_command('\n', expect_string=r'Source filename')
        output += net_connect.send_command('\n', expect_string=r'Destination filename')
        # output += net_connect.send_command('\n')
        # print(output)
        # if 'Do you want to overwrite?' in output:
        #    output += net_connect.send_command('n', expect_string=r'#', delay_factor=2)
        #    print('\n*There is a file already existing with this name.\n')
        #    sys.exit()

        output += net_connect.send_command('\n', expect_string=r'#', delay_factor=2)
        # if 'Do you want to overwrite' in output:
        #    output += net_connect.send_command('n')
        # print(output)
        ## output = net_connect.send_command('show int ip brie')
        print(output)
        print('#' * 80)
        print(f'\n*upload of target software to {hostname} completed successfully....\n')
        net_connect.disconnect()
        # end_time = datetime.now()
        end = time.time()
        print("\n>>>> {}".format(datetime.now() - start_time))
        print(f'Total execution time is {end - start} seconds')
    else:
        print(f"\n*Hooray!! Target Software {target_software} is already in {hostname}'s flash: :) :) :)\n")
        print('#' * 80)


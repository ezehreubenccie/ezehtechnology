from netmiko import ConnectHandler
import time
from datetime import datetime



start_time = datetime.now()
print(">>>> {}".format(start_time))
start = time.time()
ftp_user = 'reuben'
ftp_pass = 'cisco'
ftp_ip = '10.7.250.54'
target_software = 'asa964-41-lfbff-k8.SPA'


def usap_ftp_software_upload(**device):
    global ftp_user
    global ftp_pass
    global ftp_ip
    global target_software
    net_connect = ConnectHandler(**device)
    prompt = net_connect.find_prompt()
    hostname = prompt[0:-1]
    print(f'\n*upload of target software to {hostname} starting now....\n')
    cmd = f'copy ftp://{ftp_user}:{ftp_pass}@{ftp_ip}/{target_software}  ' f'disk0:/{target_software}'
    output = net_connect.send_command(cmd, expect_string=r'Address or name of remote host')
    output += net_connect.send_command('\n', expect_string=r'Source username')
    output += net_connect.send_command('\n', expect_string=r'Source password')
    output += net_connect.send_command('\n', expect_string=r'Source filename')
    output += net_connect.send_command('\n', expect_string=r'Destination filename')
    output += net_connect.send_command('\n', expect_string=r'#', delay_factor=2)


    print(output)
    print('#' * 80)
    print(f'\n*upload of target software to {hostname} completed successfully....\n')
    net_connect.disconnect()
    end = time.time()
    print("\n>>>> {}".format(datetime.now() - start_time))
    print(f'Total execution time is {end - start} seconds')



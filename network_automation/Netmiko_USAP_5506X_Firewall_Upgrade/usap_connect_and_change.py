from netmiko import ConnectHandler
from datetime import datetime
import sys
import time

start_time = datetime.now()
print(">>>> {}".format(start_time))
start = time.time()
old_file = ''
old_dest_file = ''
source_file = 'asa964-41-lfbff-k8.SPA'
dest_file = 'asa964-41-lfbff-k8.SPA'
device = dict()
file_system = 'disk0:'
direction = 'put'


def connect_and_change(**device):
    global source_file
    global dest_file
    global direction
    global file_system
    global old_file
    global old_dest_file
    connection = ConnectHandler(**device)
    connection.enable()

    print('\n*STEP 2 - Remove Old Software Version from boot variable.\n')
    output_ = connection.send_command('show run boot')
    print(output_.splitlines())
    output_list = output_.splitlines()
    if source_file not in output_list[0]:
        print('removing old boot file.............')
        confs = ['no ' + output_list[0], "write mem"]
        confs_1 = ['no ' + output_list[1], "write mem"]
        output1 = connection.send_config_set(confs)
        output1_2 = connection.send_config_set(confs_1)

        print(f'\n*{output1}\n')
        print(f'\n*{output1_2}\n')
        print('\nsuccessfully removed old software version from boot variable...')
    else:
        print('asa software already on latest version\n')
        print('exiting now.........')
        sys.exit()

    print('\n* STEP 3 - Set boot variable')
    old_dest_file = output_list[0].split()[2]
    set_boot_system = 'boot system {}/{}'.format(file_system, dest_file)
    set_boot_system_2 = 'boot system {}'.format(old_dest_file)
    output = connection.send_config_set([set_boot_system])
    output_2 = connection.send_config_set([set_boot_system_2])
    print(output)
    print(output_2)


    print('\n* Step 4 - Verify Boot System.\n')
    boot_system = connection.send_command("show boot")
    print(boot_system)


    print('\n* STEP 5 - Save Configuration and Reload Cisco ASA\n')
    commands = ['write mem', 'reload', 'y']
    output = connection.send_config_set(commands)

    print(output, '\n')

    print('#' * 80)
    end = time.time()
    print("\n>>>> {}".format(datetime.now() - start_time))
    print(f'Total execution time: {end - start} seconds')

    connection.disconnect()
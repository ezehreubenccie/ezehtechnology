from netmiko import ConnectHandler
from netmiko import file_transfer
from datetime import datetime
import threading
import sys

import time
start_time = datetime.now()
print(">>>> {}".format(start_time))
start = time.time()

old_file = 'asa984-15-lfbff-k8.SPA'
old_dest_file = 'asa984-15-lfbff-k8.SPA'
source_file = 'asa984-22-lfbff-k8.SPA'
dest_file = 'asa984-22-lfbff-k8.SPA'
file_system = 'disk0:'
direction = 'put'


print('\n* Step1: Upload Software to ASA ')
#global source_file
#global dest_file
#global direction
#global file_system
#global old_file
#global old_dest_file

with open('asadevices.txt', 'r') as f:
    file_content = f.read().splitlines()

devices = list()


for item in file_content:
    tmp = item.split(',')
    devices.append(tmp)

for asa in devices:
    device = {'device_type': 'cisco_asa',
              'ip': asa[3],
              'port': '22',
              'username': asa[0],
              'password': asa[1],
              'secret': asa[2],
              'verbose': 'True',
              'file_system': 'disk0:'
              }
    file_system = device.pop('file_system')
    connection = ConnectHandler(**device)
    connection.enable()

    prompt = connection.find_prompt()
    hostname = prompt[0:-1]
    #print(hostname)

    transfer_output = file_transfer(connection, source_file=source_file, dest_file=dest_file, file_system='disk0:',
                                    direction=direction, overwrite_file=True)

    #if (transfer_output['file_exists'] == True) and (transfer_output['file_transferred'] == True) and (transfer_output['file_verified'] == True):
    #    print(f'Transfer of file to {hostname} was successful')
    #else:
    #    print(f'Transfer of file to {hostname} was unsuccessful. The reason is {transfer_output}')
    #    sys.exit()
    print(transfer_output)
    ppause = input("Hit enter to continue: ")
    #answer = input('Do you want to proceed with Step2:?(Yes/No)\n')
    #if answer.lower() == 'yes' or answer.lower() == 'y':
    #    print('\n* Executing Step2: Now......')
    #else:
    #    print(f'You answer was {answer}. Exiting Program now.........')
    #    sys.exit()
    #print(f'Transfer of file to {hostname} was successful')
    #print(transfer_output)
    print('\n*STEP 2 - Remove Old Software Version from boot variable.\n')
    output_ = connection.send_command('show run boot')
    if  source_file not in output_:
        print('removing old boot file.............')
        confs = ['no ' + output_, "write mem"]
        output_2 = connection.send_config_set(confs)
        print(output_2)
        print('\nsuccessfully removed old software version from boot variable...')
    else:
        print('asa software already on latest version\n')
        print('exiting now.........')
        sys.exit()

    print('\nSTEP 3 - Set boot variable')
    set_boot_system = 'boot system {}/{}'.format(file_system, dest_file)
    set_boot_system_2 = 'boot system {}/{}'.format(file_system, old_dest_file)
    output = connection.send_config_set([set_boot_system])
    output_2 = connection.send_config_set([set_boot_system_2])
    print(output)
    print(output_2)
    #print(f'\n*Primary boot variable is : {output}')
    #print(f'\n*Backup boot variable is : {output_2}')
    #time.sleep(10)
    #check = input('Please check the output above. Are the boot Variables set correctly?(Yes/No)\n')
    #if check.lower() == 'yes' or check.lower() == 'y':
    #    print(f'\nYour answer is {check}. Proceeding with STEP 4')


    #print('\nBackup Boot variable Is Set!')

    print('\n* Step 4 - Verify Boot System.\n')
    boot_system = connection.send_command("show boot")
    print(boot_system)
    #check = input('Please check the output above. Are the boot Variables set correctly?(Yes/No)\n')
    #if check.lower() == 'yes' or check.lower() == 'y':
    #    print(f'\nYour answer is {check}. Proceeding with STEP 4')
    #else:
    #    print('\nSetting boot variable back to old software image.\n')
    #    set_boot_system_3 = 'boot system {}/{}'.format(file_system, old_dest_file)

    print('\nSTEP 5 - Save Configuration and Reload Cisco ASA\n')
    commands = ['write mem', 'reload', 'y']
    output = connection.send_config_set(commands)
    # output_1= tera_term.send_command('reload')
    # output_2= tera_term.send_command('y')
    print(output, '\n')
    # print(output_1, '\n')
    # print(output_2, '\n')

    end = time.time()
    print("\n>>>> {}".format(datetime.now() - start_time))
    print(f'Total execution time: {end - start} seconds')

    print('#' * 30)

    connection.disconnect()

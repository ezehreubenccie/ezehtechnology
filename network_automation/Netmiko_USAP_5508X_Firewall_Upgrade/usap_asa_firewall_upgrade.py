import sys

from usap_asa_devices_to_upgrade import asa_devices_to_upgrade
from usap_ftp_software_upload_2 import usap_ftp_software_upload
from usap_connect_and_change import connect_and_change
from create_threads import create_threads


asa_firewall = asa_devices_to_upgrade()
#print(type(asa_firewall))
try:
    #print('Please Check and ensure target software is not present in devices before running')
    answer = input('upload target software to devices? (yes/no): ')
    if answer.lower() == 'yes' or answer.lower() == 'y':
        create_threads(asa_firewall, usap_ftp_software_upload(**asa_firewall))
    else:
        print(f'your answer is {answer}. Exiting the program.....')
        sys.exit()

except KeyboardInterrupt:
    print('\n\n* Program aborted by user. Exiting....\n')
    sys.exit()

try:
    print('Target Software uploaded to devices successfully!')
    upgrade_answer = input('Do you want to upgrade devices now?(yes/no): ')
    if upgrade_answer.lower() == 'yes' or upgrade_answer.lower() == 'y':
        create_threads(asa_firewall, connect_and_change(**asa_firewall))
    else:
        print(f'your answer is {upgrade_answer}. Exiting the program.....')
        sys.exit()

except KeyboardInterrupt:
    print('\n\n* Program aborted by user. Exiting....\n')
    sys.exit()






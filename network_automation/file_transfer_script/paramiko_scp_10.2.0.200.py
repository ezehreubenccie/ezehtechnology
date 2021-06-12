import myparamiko
import getpass
from scp import SCPClient


username = input('Username:')
password = getpass.getpass()
tera_term = myparamiko.connect('10.2.0.200', 22, username, password)

scp = SCPClient(tera_term.get_transport())
#copy a single file to a remote server
#scp.put('/home/reuben3010/network_automation/get_boot_system_and_asdm_image_for_fpr_1120_firewalls.yml', '/root/network_automation/get_boot_system_and_asdm_image_for_fpr_1120_firewalls.yml')

#copy a directory to a remote server
#scp.put('directory1', recursive=True, remote_path='/home/reuben3010/Network_Automation_Scripts')

#copy a file from a remote server
#scp.get('/root/network_automation/gather_fpr_1120_firewall_asdm_software_facts_2.yml', '/home/reuben3010/network_automation/gather_fpr_1120_firewall_asdm_software_facts_2.yml')
#scp.get('/home/reuben3010/Network_Automation_Scripts/commands_file', 'commands_file.txt')
#scp.get('/etc/passwd', 'passwd.txt')
#scp.get('/etc/ansible/seattle_firewall.yml', '/etc/ansible/seattle_firewall.yml')
scp.get('/Volume/home/admin/pigtail-all-1623256701.log', '/home/reuben3010/fmc_files/pigtail-all-1623256701.log')

#copy a file from a remote server to a local directory
#scp.get('/etc/passwd', 'c:\\')
scp.close()

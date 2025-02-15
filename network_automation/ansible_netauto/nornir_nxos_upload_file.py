from nornir import InitNornir
# from nornir.plugins.tasks.networking import napalm_get, netmiko_send_command
# from nornir.plugins.functions.text import print_result
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_netmiko.tasks import netmiko_send_command
import json
import time

import logging
from netmiko import ConnectHandler

logging.basicConfig(filename="netmiko_debug.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

import os
from getpass import getpass

scp_password = os.getenv("SCP_PASS") 


def gather_nexus_facts(task: Task):
    """Gather Nexus Switch Hardware facts"""
    result = task.run(task=napalm_get, getters=["facts"])
    # result = nr.run(task=netmiko_send_command, command_string="show version")

    return Result(host=task.host, result=result.result)


def check_flash_space(task: Task, sw_image: str):
    """Check if the software image exists in flash"""
    cmd = f"dir bootflash: | include {sw_image}"
    result = task.run(task=netmiko_send_command, command_string=cmd)
    return Result(host=task.host, result=result.result)


def get_free_space(task: Task):
    """Get free space on the switch"""
    cmd = "dir"
    result = task.run(task=netmiko_send_command, command_string=cmd)
    return Result(host=task.host, result=result.result)


# def copy_software_image(
#     task: Task, scp_server: str, scp_user: str, file_path: str, sw_image: str, vrf: str
# ):
#     """Copy software image to Nexus switch"""
#     cmds = [
#         "clear ssh hosts",
#         f"copy scp://{scp_user}@{scp_server}/{file_path}/{sw_image} bootflash: vrf {vrf} use-kstack",
#     ]
#     for cmd in cmds:
#         result = task.run(task=netmiko_send_command, command_string=cmd,expect_string=r"#",read_timeout=80)
#     return Result(host=task.host, result=result.result)

###THIS WORKED######   
# def copy_software_image(task, scp_server, scp_user, file_path, sw_image, vrf, scp_pass):
#     """Copy software image to Nexus switch using SCP with proper prompt handling."""
    
#     net_connect = task.host.get_connection("netmiko", task.nornir.config)

#     cmds = [
#         "clear ssh hosts",
#         f"copy scp://{scp_user}@{scp_server}/{file_path}/{sw_image} bootflash: vrf {vrf} use-kstack"
#     ]

#     for cmd in cmds:
#         result = net_connect.send_command_timing(cmd, delay_factor=5)

#         # Handle interactive prompts dynamically
#         if "Are you sure you want to continue connecting" in result:
#             result += net_connect.send_command_timing("yes", delay_factor=5)
#         # if "Password:" in result:
#         #     result += net_connect.send_command_timing("your_scp_password", delay_factor=5)
#         if "bytes copied" in result:
#             break  # Exit if the file copy succeeds
#         if "password:" in result.lower():
#             result += net_connect.send_command_timing(scp_pass, delay_factor=5)

#         print(f"DEBUG: SCP Copy Output for {task.host}: {result}")

#     # Wait 5 minutes before checking the file
#     print("Waiting 5 minutes to ensure SCP completes before validating...")
#     time.sleep(300)

#     return Result(host=task.host, result="Software copy started successfully.")



######THIS IS THE ONE THAT DEFINATELY WORKED BUT TO MUCH OUTPUT########
# def copy_software_image(task, scp_server, scp_user, file_path, sw_image, vrf, scp_pass):
#     """Copy software image to Nexus switch using SCP with proper progress monitoring."""
    
#     net_connect = task.host.get_connection("netmiko", task.nornir.config)

#     cmd = f"copy scp://{scp_user}@{scp_server}/{file_path}/{sw_image} bootflash: vrf {vrf} use-kstack"

#     # Start the SCP copy
#     result = net_connect.send_command_timing(cmd, delay_factor=5)

#     # Handle authentication and host verification
#     if "Are you sure you want to continue connecting" in result:
#         result += net_connect.send_command_timing("yes", delay_factor=5)
#     if "password:" in result.lower():
#         result += net_connect.send_command_timing(scp_pass, delay_factor=5)

#     print(f"DEBUG: SCP Transfer Started for {task.host}")

#     # Monitor SCP progress
#     retries = 0
#     while retries < 60:  # Wait up to 30 minutes (60 retries, 30 sec each)
#         result = net_connect.read_channel()
#         print(f"DEBUG: SCP Progress Output: {result.strip()}")

#         if "#" in result:  # File transfer complete if CLI prompt appears
#             print("✅ SCP Transfer Completed!")
#             return Result(host=task.host, result="Software copy completed successfully.")

#         time.sleep(30)  # Wait 30 seconds before checking again
#         retries += 1

#     return Result(host=task.host, failed=True, result="❌ SCP transfer did not complete in expected time.")


from tqdm import tqdm
import re
import time

def copy_software_image(task, scp_server, scp_user, file_path, sw_image, vrf, scp_pass):
    """Copy software image to Nexus switch using SCP with a progress bar."""
    
    net_connect = task.host.get_connection("netmiko", task.nornir.config)

    cmd = f"copy scp://{scp_user}@{scp_server}/{file_path}/{sw_image} bootflash: vrf {vrf} use-kstack"

    # Start the SCP copy
    result = net_connect.send_command_timing(cmd, delay_factor=5)

    # Handle authentication and host verification
    if "Are you sure you want to continue connecting" in result:
        result += net_connect.send_command_timing("yes", delay_factor=5)
    if "password:" in result.lower():
        result += net_connect.send_command_timing(scp_pass, delay_factor=5)

    print(f"📦 SCP Transfer Started for {task.host}...")

    # Initialize progress bar
    progress_bar = tqdm(total=100, desc=f"{task.host} - SCP Progress", position=0, leave=True)

    # Monitor SCP progress
    retries = 0
    completed = False
    while retries < 60:  # Wait up to 30 minutes (60 retries, 30 sec each)
        result = net_connect.read_channel()

        # Extract percentage from SCP output using regex
        match = re.search(r'(\d+)%', result)
        if match:
            percent_complete = int(match.group(1))
            progress_bar.n = percent_complete
            progress_bar.refresh()

        if "#" in result:  # File transfer complete if CLI prompt appears
            completed = True
            break

        time.sleep(30)  # Wait 30 seconds before checking again
        retries += 1

    progress_bar.close()

    if completed:
        print("✅ SCP Transfer Completed!")
        return Result(host=task.host, result="Software copy completed successfully.")
    else:
        return Result(host=task.host, failed=True, result="❌ SCP transfer did not complete in expected time.")





# def validate_copy(task: Task, sw_image: str, actual_sw_image_size: int):
#     """Validate if software image was copied correctly"""
#     cmd = f"dir bootflash:{sw_image} | json"
#     result = task.run(task=netmiko_send_command, command_string=cmd)
#     output = json.loads(result.result)
#     file_size = output["TABLE_dir"]["ROW_dir"]["fsize"]
#     if int(file_size) >= actual_sw_image_size:
#         return Result(host=task.host, result="Software image copied successfully")
#     else:
#         return Result(host=task.host, result="Copy failed, incorrect file size")

# def validate_copy(task, sw_image):
#     """Validate if software image was copied correctly."""
#     net_connect = task.host.get_connection("netmiko", task.nornir.config)

#     cmd = f"dir bootflash:{sw_image} | json"
    
#     # Send command with relaxed timing
#     result = net_connect.send_command_timing(
#         cmd, 
#         delay_factor=5,  # Increase wait time for slow responses
#         read_timeout=60  # Ensure it waits long enough
#     )

#     # Debugging: Print response
#     print(f"DEBUG: Validate Copy Output for {task.host}: {result}")

#     if "No such file or directory" in result:
#         return Result(host=task.host, failed=True, result=f"{sw_image} not found in bootflash.")

#     return Result(host=task.host, result="Software image verified successfully.")

def validate_copy(task: Task, sw_image: str, actual_sw_image_size: int, max_retries=20, delay_between_checks=60):
    """Validate if software image was copied correctly after waiting for transfer to complete."""

    cmd = f"dir bootflash:{sw_image} | json"
    retries = 0

    while retries < max_retries:
        result = task.run(task=netmiko_send_command, command_string=cmd)

        try:
            output = json.loads(result.result)
            file_size = output["TABLE_dir"]["ROW_dir"]["fsize"]

            if int(file_size) >= actual_sw_image_size:
                return Result(host=task.host, result=f"✅ Software image copied successfully. Size: {file_size} bytes")

            print(f"⚠️ Copy in progress: {file_size} bytes copied so far. Waiting before retrying...")

        except (json.JSONDecodeError, KeyError):
            print(f"⚠️ File not found yet. Retrying in {delay_between_checks} seconds...")

        time.sleep(delay_between_checks)  # Wait before retrying
        retries += 1

    return Result(host=task.host, failed=True, result=f"❌ {sw_image} not found in bootflash after {max_retries} retries.")



if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")

    # Variables
    sw_image = "nxos.9.3.14.bin"
    scp_server = "10.1.101.130"
    scp_user = "rezeh"
    file_path = "home/rezeh/VENV/python_netauto/paramiko"
    vrf = "management"
    actual_sw_image_size = 2005689856  # Bytes

    # Execute tasks
    results = nr.run(task=gather_nexus_facts)
    print_result(results)

    flash_results = nr.run(task=check_flash_space, sw_image=sw_image)
    print_result(flash_results)

    space_results = nr.run(task=get_free_space)
    print_result(space_results)

    copy_results = nr.run(
        task=copy_software_image,
        scp_server=scp_server,
        scp_user=scp_user,
        file_path=file_path,
        sw_image=sw_image,
        scp_pass=scp_password,
        vrf=vrf
    )
    print_result(copy_results)

    validate_results = nr.run(
        task=validate_copy, sw_image=sw_image, actual_sw_image_size=actual_sw_image_size
    )
    print_result(validate_results)

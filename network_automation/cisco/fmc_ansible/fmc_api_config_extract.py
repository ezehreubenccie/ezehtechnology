#!/usr/bin/env python3

import requests
import json

# Suppress SSL warnings for self-signed certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Replace with your FMC details
FMC_HOST = "wa-fmc2500"
USERNAME = "apiuser"
PASSWORD = "Xs0PC8VPMoxkuooXVreb"

# API endpoints
FMC_LOGIN_URL = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
FMC_DEVICE_URL = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{{domain_uuid}}/devices/devicerecords"

# Function to obtain the FMC auth token
def get_auth_token():
    headers = {"Content-Type": "application/json"}
    response = requests.post(FMC_LOGIN_URL, auth=(USERNAME, PASSWORD), headers=headers, verify=False)

    if response.status_code == 204:
        auth_token = response.headers.get("X-auth-access-token")
        domain_uuid = response.headers.get("DOMAIN_UUID")
        return auth_token, domain_uuid
    else:
        print(f"Failed to authenticate with FMC: {response.text}")
        exit()

# Function to retrieve device configurations
# def get_device_configurations(auth_token, domain_uuid):
#     headers = {
#         "Content-Type": "application/json",
#         "X-auth-access-token": auth_token
#     }

#     device_url = FMC_DEVICE_URL.format(domain_uuid=domain_uuid)
#     response = requests.get(device_url, headers=headers, verify=False)

#     if response.status_code == 200:
#         devices = response.json()["items"]
#         print(f"Retrieved {len(devices)} devices.")
#         return devices
#     else:
#         print(f"Failed to retrieve devices: {response.text}")
#         exit()

# # Function to save configuration details to a file
# def save_to_file(filename, data):
#     with open(filename, "w") as file:
#         json.dump(data, file, indent=4)
#     print(f"Configuration saved to {filename}")

# Main logic
def main():
    print("Authenticating with FMC...")
    auth_token, domain_uuid = get_auth_token()
    print(f"token: {auth_token}")
    print(f"domain_uuid: {domain_uuid}")

    # print("Fetching device configurations...")
    # devices = get_device_configurations(auth_token, domain_uuid)

    # Save detailed configurations to a file
    # save_to_file("device_configurations.json", devices)

    # print("Process completed.")

if __name__ == "__main__":
    main()

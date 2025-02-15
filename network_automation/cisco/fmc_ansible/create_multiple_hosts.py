#!/usr/bin/env python3

import requests
import json
import os

FMC_HOST = os.getenv("FMC_HOST")
USERNAME = os.getenv("FMC_USERNAME")
PASSWORD = os.getenv("FMC_PASSWORD")

HOSTS = [
    {"name": "test-dc02", "ip": "10.1.1.2"},
    {"name": "test-dc03", "ip": "10.1.1.3"},
    {"name": "test-dc04", "ip": "10.1.1.4"},
]

# API endpoints
FMC_LOGIN_URL = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
FMC_DEVICE_URL = (
    f"https://{FMC_HOST}/api/fmc_config/v1/domain/{{domain_uuid}}/devices/devicerecords"
)

# Define Headers
HEADERS = {"Content-Type": "application/json"}

# Suppress SSL warnings for self-signed certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Get Authentication Token
def get_auth_token():
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        FMC_LOGIN_URL, auth=(USERNAME, PASSWORD), headers=headers, verify=False
    )

    if response.status_code == 204:
        auth_token = response.headers.get("X-auth-access-token")
        domain_uuid = response.headers.get("DOMAIN_UUID")
        return auth_token, domain_uuid
    else:
        print(f"Failed to authenticate with FMC: {response.text}")
        exit()


# Create Network Objects
def create_host_objects(token, domain_uuid):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts"

    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    # Data for the new Host Object
    for host in HOSTS:
        data = {
            "name": host["name"],
            "value": host["ip"],
            "description": f"Host object for {host['name']}",
            "type": "Host",
            "overridable": False,
        }

    

        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

        if response.status_code in [200, 201]:
            print(f"✅ Successfully created {host['name']} ({host['ip']})")
        else:
            print(f"❌ Failed to create {host['name']} ({host['ip']}): {response.text}")



# Main logic
def main():
    print("Authenticating with FMC...")
    auth_token, domain_uuid = get_auth_token()
    print(f"token: {auth_token}")
    print(f"domain_uuid: {domain_uuid}")

    if auth_token and domain_uuid:
        create_host_objects(auth_token, domain_uuid)
    else:
        print("❌ Could not retrieve authentication token.")


if __name__ == "__main__":
    main()


# Main Execution
# if __name__ == "__main__":
#     token, domain_uuid = get_auth_token()
#     print(f"token: {token}")
#     print(f"domain_uuid: {domain_uuid}")
# if token and domain_uuid:
#     create_network_object(token, domain_uuid)
# else:
#     print("❌ Could not retrieve authentication token.")

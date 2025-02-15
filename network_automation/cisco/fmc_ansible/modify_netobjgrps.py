#!/usr/bin/env python3

import requests
import json
import os

# FMC Credentials and Host
FMC_HOST = os.getenv("FMC_HOST")
USERNAME = os.getenv("FMC_USERNAME")
PASSWORD = os.getenv("FMC_PASSWORD")
# HOSTNAME = "utd-dc03.utd.com"
HOSTNAME = "test-dc01"

# Object groups to modify
# OBJECT_GROUPS = [
#     "UTD-dns-server",
#     "DM_INLINE_NETWORK_12",
#     "Waltham-LDAP-Servers",
#     "WalthamDNSServers",
#     "Waltham_AD_Servers",
#     "Waltham_Domain_Controllers",
#     "DM_INLINE_NETWORK_50-FTD_MIG"
# ]

OBJECT_GROUPS = [
    "test_1"
    # "UTD-dns-server",
    # "DM_INLINE_NETWORK_12",
    # "Waltham-LDAP-Servers",
    # "WalthamDNSServers",
    # "Waltham_AD_Servers",
    # "Waltham_Domain_Controllers",
    # "DM_INLINE_NETWORK_50-FTD_MIG"
]

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Authenticate to FMC and get token
def get_auth_token():
    url = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    response = requests.post(url, auth=(FMC_USER, FMC_PASS), verify=False)
    if response.status_code == 204:
        return response.headers["X-auth-access-token"], response.headers["DOMAIN_UUID"]
    else:
        print("Failed to get token:", response.text)
        exit()

# Get network object ID of the host
def get_network_object_id(hostname, token, domain_uuid):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkaddresses"
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        for obj in data.get("items", []):
            if obj.get("name") == hostname:
                return obj["id"]
    print(f"Host {hostname} not found in FMC. Create it manually or add creation logic.")
    exit()

# Get object group details
def get_object_group(group_name, token, domain_uuid):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        for obj_group in data.get("items", []):
            if obj_group.get("name") == group_name:
                return obj_group
    print(f"Object group {group_name} not found in FMC.")
    return None

# Update object group with new host
def add_host_to_group(group_name, network_obj_id, token, domain_uuid):
    group = get_object_group(group_name, token, domain_uuid)
    if not group:
        return

    group_id = group["id"]
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups/{group_id}"
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    # Append new object to the existing group
    group["objects"].append({"id": network_obj_id, "type": "Network"})

    response = requests.put(url, headers=headers, json=group, verify=False)
    if response.status_code == 200:
        print(f"Successfully added {HOSTNAME} to {group_name}")
    else:
        print(f"Failed to update {group_name}: {response.text}")

# Main execution
if __name__ == "__main__":
    token, domain_uuid = get_auth_token()
    network_obj_id = get_network_object_id(HOSTNAME, token, domain_uuid)

    for group in OBJECT_GROUPS:
        add_host_to_group(group, network_obj_id, token, domain_uuid)

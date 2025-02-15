#!/usr/bin/env python3

import requests
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Get FMC credentials from environment variables
FMC_HOST = os.getenv("FMC_HOST")
USERNAME = os.getenv("FMC_USERNAME")
PASSWORD = os.getenv("FMC_PASSWORD")

# Host objects with assigned groups
HOSTS = [
    {"name": "test-dc02", "ip": "10.1.1.2", "group": "test_2"},
    {"name": "test-dc03", "ip": "10.1.1.3", "group": "test_3"},
    {"name": "test-dc04", "ip": "10.1.1.4", "group": "test_4"},
    {"name": "test-dc05", "ip": "10.1.1.5", "group": "test_4"},
    {"name": "test-dc06", "ip": "10.1.1.6", "group": "test_5"},
    {"name": "test-dc07", "ip": "10.1.1.7", "group": "test_6"},
]

# API Endpoints
FMC_LOGIN_URL = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"


# Get Authentication Token
def get_auth_token():
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        FMC_LOGIN_URL, auth=(USERNAME, PASSWORD), headers=headers, verify=False
    )

    if response.status_code == 204:
        return response.headers.get("X-auth-access-token"), response.headers.get(
            "DOMAIN_UUID"
        )

    print(f"❌ Failed to authenticate with FMC: {response.text}")
    exit()


# Retrieve existing host objects and return a dictionary {name: id}
def get_existing_host_ids(token, domain_uuid):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts?limit=1000"
    headers = {"X-auth-access-token": token}

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        host_ids = {
            host["name"]: host["id"] for host in response.json().get("items", [])
        }
        print(f"🔹 Retrieved {len(host_ids)} existing host objects from FMC.")
        return host_ids
    else:
        print(f"❌ Failed to retrieve existing hosts: {response.text}")
        return {}


# Create hosts if they don't exist
def create_host_objects(token, domain_uuid, host_ids):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts"
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    for host in HOSTS:
        if host["name"] in host_ids:
            print(f"✅ Host {host['name']} already exists. Skipping.")
            continue  # Skip if host exists

        data = {
            "name": host["name"],
            "value": host["ip"],
            "description": f"Host object for {host['name']}",
            "type": "Host",
        }
        response = requests.post(
            url, headers=headers, data=json.dumps(data), verify=False
        )

        if response.status_code in [200, 201]:
            host_id = response.json().get("id")
            host_ids[host["name"]] = host_id  # Store new host ID
            print(f"✅ Successfully created {host['name']} ({host['ip']})")
        else:
            print(f"❌ Failed to create {host['name']} ({host['ip']}): {response.text}")


# Check if a network group exists
def check_group_exists(token, domain_uuid, group_name):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups?filter=nameOrValue:{group_name}"
    headers = {"X-auth-access-token": token}
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        existing_groups = response.json().get("items", [])
        for group in existing_groups:
            if group["name"] == group_name:
                return group["id"]
    return None


# Create network groups with at least one member
def create_object_groups(token, domain_uuid, host_ids):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    groups = {host["group"] for host in HOSTS}

    for group_name in groups:
        group_id = check_group_exists(token, domain_uuid, group_name)
        if group_id:
            print(f"✅ Object group {group_name} already exists. Skipping.")
            continue

        first_host = next((host for host in HOSTS if host["group"] == group_name), None)
        if not first_host or first_host["name"] not in host_ids:
            print(f"❌ No valid hosts found for group {group_name}, skipping creation.")
            continue

        data = {
            "name": group_name,
            "description": f"Object group for {group_name}",
            "type": "NetworkGroup",
            "objects": [{"type": "Host", "id": host_ids[first_host["name"]]}],
        }

        response = requests.post(
            url, headers=headers, data=json.dumps(data), verify=False
        )

        if response.status_code in [200, 201]:
            print(f"✅ Successfully created object group {group_name}")
        else:
            print(f"❌ Failed to create object group {group_name}: {response.text}")


# Add hosts to their respective groups
def add_hosts_to_groups(token, domain_uuid, host_ids):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    groups = {host["group"] for host in HOSTS}

    for group_name in groups:
        group_id = check_group_exists(token, domain_uuid, group_name)
        if not group_id:
            print(f"❌ Object group {group_name} does not exist. Skipping.")
            continue

        hosts_to_add = [
            {"type": "Host", "id": host_ids[host["name"]]}
            for host in HOSTS
            if host["group"] == group_name and host["name"] in host_ids
        ]

        group_url = f"{url}/{group_id}"
        response = requests.put(
            group_url,
            headers=headers,
            data=json.dumps({"objects": hosts_to_add}),
            verify=False,
        )

        if response.status_code in [200, 201]:
            print(
                f"✅ Updated group {group_name} with members: {', '.join(host['name'] for host in HOSTS if host['group'] == group_name)}"
            )
        else:
            print(f"❌ Failed to update group {group_name}: {response.text}")


# Main Execution
if __name__ == "__main__":
    print("🔹 Authenticating with FMC...")
    token, domain_uuid = get_auth_token()

    print("🔹 Fetching existing hosts...")
    host_ids = get_existing_host_ids(token, domain_uuid)

    create_host_objects(token, domain_uuid, host_ids)
    create_object_groups(token, domain_uuid, host_ids)
    add_hosts_to_groups(token, domain_uuid, host_ids)

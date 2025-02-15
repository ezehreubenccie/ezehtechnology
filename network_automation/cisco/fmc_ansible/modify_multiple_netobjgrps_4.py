#!/usr/bin/env python3

import requests
import json
import os
import csv
import sys

# Load FMC credentials from environment variables
FMC_IP = os.getenv("FMC_HOST")
USERNAME = os.getenv("FMC_USERNAME")
PASSWORD = os.getenv("FMC_PASSWORD")


# CSV file path (modify if needed)
CSV_FILE = "hosts.csv"

# API endpoints
FMC_LOGIN_URL = f"https://{FMC_IP}/api/fmc_platform/v1/auth/generatetoken"
FMC_DEVICE_URL = (
    f"https://{FMC_IP}/api/fmc_config/v1/domain/{{domain_uuid}}/devices/devicerecords"
)


# Suppress SSL warnings for self-signed certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Get Authentication Token
# def get_auth_token():
#     url = f"https://{FMC_IP}/api/fmc_platform/v1/auth/generatetoken"
#     response = requests.post(
#         url,
#         auth=(USERNAME, PASSWORD),
#         headers={"Content-Type": "application/json"},
#         verify=False,
#     )

#     if response.status_code == 204:
#         return response.headers.get("X-auth-access-token"), response.headers.get(
#             "DOMAIN-UUID"
#         )
#     print(f"❌ Failed to get auth token: {response.text}")
#     return None, None

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



# Load hosts from CSV file
def load_hosts_from_csv(csv_file):
    hosts = []
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if "name" in row and "ip" in row and "group" in row:
                    hosts.append(
                        {
                            "name": row["name"].strip(),
                            "ip": row["ip"].strip(),
                            "group": row["group"].strip(),
                        }
                    )
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        sys.exit(1)
    return hosts


# Check if a host object exists
def check_host_exists(token, domain_uuid, host_name):
    url = f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts?filter=nameOrValue:{host_name}"
    headers = {"X-auth-access-token": token}

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        existing_hosts = response.json().get("items", [])
        return any(host["name"] == host_name for host in existing_hosts)
    return False


# Create host objects if they don’t exist
def create_host_objects(token, domain_uuid, hosts):
    url = f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts"
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    for host in hosts:
        if check_host_exists(token, domain_uuid, host["name"]):
            print(f"✅ Host {host['name']} already exists. Skipping.")
            continue

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
            print(f"✅ Successfully created {host['name']} ({host['ip']})")
        else:
            print(f"❌ Failed to create {host['name']} ({host['ip']}): {response.text}")


# Check if a network group exists
def check_group_exists(token, domain_uuid, group_name):
    url = f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups?filter=nameOrValue:{group_name}"
    headers = {"X-auth-access-token": token}

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        existing_groups = response.json().get("items", [])
        for group in existing_groups:
            if group["name"] == group_name:
                return group["id"]
    return None


# Create object groups with at least one member
def create_object_groups(token, domain_uuid, hosts):
    url = (
        f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    )
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    groups = {host["group"] for host in hosts}

    for group_name in groups:
        group_id = check_group_exists(token, domain_uuid, group_name)

        if group_id:
            print(f"✅ Object group {group_name} already exists. Skipping.")
            continue

        first_host = next((host for host in hosts if host["group"] == group_name), None)
        if not first_host:
            print(f"❌ No hosts found for group {group_name}, skipping creation.")
            continue

        data = {
            "name": group_name,
            "description": f"Object group for {group_name}",
            "type": "NetworkGroup",
            "objects": [{"type": "Host", "name": first_host["name"]}],
        }

        response = requests.post(
            url, headers=headers, data=json.dumps(data), verify=False
        )

        if response.status_code in [200, 201]:
            print(
                f"✅ Created object group {group_name} with {first_host['name']} as initial member"
            )
        else:
            print(f"❌ Failed to create object group {group_name}: {response.text}")


# Add remaining hosts to their respective groups
def add_hosts_to_groups(token, domain_uuid, hosts):
    url = (
        f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    )
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    group_ids = {
        group_name: check_group_exists(token, domain_uuid, group_name)
        for group_name in {host["group"] for host in hosts}
    }

    for group_name, group_id in group_ids.items():
        if not group_id:
            print(f"❌ Object group {group_name} does not exist. Skipping.")
            continue

        hosts_to_add = [
            {"type": "Host", "name": host["name"]}
            for host in hosts
            if host["group"] == group_name
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
                f"✅ Updated group {group_name} with members: {', '.join(host['name'] for host in hosts if host['group'] == group_name)}"
            )
        else:
            print(f"❌ Failed to update group {group_name}: {response.text}")


# Main Execution
if __name__ == "__main__":
    token, domain_uuid = get_auth_token()
    if not token or not domain_uuid:
        print("❌ Could not retrieve authentication token.")
        sys.exit(1)

    hosts = load_hosts_from_csv(CSV_FILE)
    create_host_objects(token, domain_uuid, hosts)
    create_object_groups(token, domain_uuid, hosts)
    add_hosts_to_groups(token, domain_uuid, hosts)

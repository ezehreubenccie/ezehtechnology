#!/usr/bin/env python3

import requests
import json
import os
import csv
import sys

FMC_HOST = os.getenv("FMC_HOST")
USERNAME = os.getenv("FMC_USERNAME")
PASSWORD = os.getenv("FMC_PASSWORD")

# CSV file path (modify if needed)
CSV_FILE = "hosts.csv"

# Host objects with assigned groups
# HOSTS = [
#     {"name": "test-dc02", "ip": "10.1.1.2", "group": "test_2"},
#     {"name": "test-dc03", "ip": "10.1.1.3", "group": "test_3"},
#     {"name": "test-dc04", "ip": "10.1.1.4", "group": "test_4"},
#     {"name": "test-dc05", "ip": "10.1.1.5", "group": "test_4"},
#     {"name": "test-dc06", "ip": "10.1.1.6", "group": "test_5"},
# ]

# List of unique object groups
#GROUPS = set(host["group"] for host in HOSTS)

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


# Load hosts from CSV file
def load_hosts_from_csv(csv_file):
    hosts = []
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if "name" in row and "ip" in row and "group" in row:
                    hosts.append({"name": row["name"].strip(), "ip": row["ip"].strip(), "group": row["group"].strip()})
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        sys.exit(1)
    return hosts


# Check if a host object already exists
def check_host_exists(token, domain_uuid, host_name):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts?filter=nameOrValue:{host_name}"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        existing_hosts = response.json().get("items", [])
        for host in existing_hosts:
            if host["name"] == host_name:
                return True  # Host already exists
    return False  # Host does not exist


# Create Network Objects in FMC if they don't already exist
def create_host_objects(token, domain_uuid, hosts):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts"

    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    # Data for the new Host Object
    for host in hosts:
        if check_host_exists(token, domain_uuid, host["name"]):
            print(
                f"✅ Host {host['name']} ({host['ip']}) already exists. Skipping creation."
            )
            continue  # Skip creation if the host already exists

        data = {
            "name": host["name"],
            "value": host["ip"],
            "description": f"Host object for {host['name']}",
            "type": "Host",
            "overridable": False,
        }

        response = requests.post(
            url, headers=headers, data=json.dumps(data), verify=False
        )

        if response.status_code in [200, 201]:
            print(f"✅ Successfully created {host['name']} ({host['ip']})")
        else:
            print(f"❌ Failed to create {host['name']} ({host['ip']}): {response.text}")


# Check if an object group exists
def check_group_exists(token, domain_uuid, group_name):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups?filter=nameOrValue:{group_name}"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        existing_groups = response.json().get("items", [])
        for group in existing_groups:
            if group["name"] == group_name:
                return group["id"]  # Return the existing group's ID
    return None  # Group does not exist


# Create object groups if they don’t exist
def create_object_groups(token, domain_uuid, hosts):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    groups = {host["group"] for host in hosts}

    for group_name in groups:
        group_id = check_group_exists(token, domain_uuid, group_name)

        if group_id:
            print(f"✅ Object group {group_name} already exists. Skipping creation.")
            continue  # Skip if group already exists

        data = {
            "name": group_name,
            "description": f"Object group for {group_name}",
            "type": "NetworkGroup",
            "overridable": False,
            "objects": [],  # Initially empty, we'll add members later
        }

        response = requests.post(
            url, headers=headers, data=json.dumps(data), verify=False
        )

        if response.status_code in [200, 201]:
            print(f"✅ Successfully created object group {group_name}")
        else:
            print(f"❌ Failed to create object group {group_name}: {response.text}")


# Add host objects to their respective groups
def add_hosts_to_groups(token, domain_uuid, hosts):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    # Fetch existing object groups
    group_ids = {
        group_name: check_group_exists(token, domain_uuid, group_name)
        for group_name in GROUPS
    }

    for group_name, group_id in group_ids.items():
        if not group_id:
            print(f"❌ Object group {group_name} does not exist. Skipping.")
            continue

        # Fetch the current members of the group
        group_url = f"{url}/{group_id}"
        group_response = requests.get(group_url, headers=headers, verify=False)

        if group_response.status_code != 200:
            print(f"❌ Failed to fetch object group {group_name}: {group_response.text}")
            continue

        existing_group_data = group_response.json()
        existing_members = {
            obj["name"] for obj in existing_group_data.get("objects", [])
        }

        # Find hosts that belong to this group
        hosts_to_add = [
            host
            for host in HOSTS
            if host["group"] == group_name and host["name"] not in existing_members
        ]

        if not hosts_to_add:
            print(f"✅ No new hosts to add to group {group_name}.")
            continue

        # Prepare new member data
        new_members = [{"type": "Host", "name": host["name"]} for host in hosts_to_add]
        existing_group_data["objects"].extend(new_members)

        # Update the group with new members
        update_response = requests.put(
            group_url,
            headers=headers,
            data=json.dumps(existing_group_data),
            verify=False,
        )

        if update_response.status_code in [200, 201]:
            print(
                f"✅ Added {', '.join(host['name'] for host in hosts_to_add)} to group {group_name}"
            )
        else:
            print(
                f"❌ Failed to add hosts to group {group_name}: {update_response.text}"
            )


# Main logic
def main():
    if not all([FMC_HOST, USERNAME, PASSWORD]):
        print(
            "❌ Missing environment variables. Please set FMC_IP, FMC_USERNAME, and FMC_PASSWORD."
        )
    else:
        print("Authenticating with FMC...")
        auth_token, domain_uuid = get_auth_token()
        print(f"token: {auth_token}")
        print(f"domain_uuid: {domain_uuid}")

        if auth_token and domain_uuid:
            hosts = load_hosts_from_csv(CSV_FILE)
            create_host_objects(auth_token, domain_uuid, hosts)
            create_object_groups(auth_token, domain_uuid, hosts)
            add_hosts_to_groups(auth_token, domain_uuid, hosts)
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

#!/usr/bin/env python3

import requests
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pprint import pprint

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
    {"name": "test-dc07", "ip": "10.1.1.7", "group": "test_4"},
]

# List of unique object groups
GROUPS = set(host["group"] for host in HOSTS)

# API endpoints
FMC_LOGIN_URL = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
FMC_DEVICE_URL = (
    f"https://{FMC_HOST}/api/fmc_config/v1/domain/{{domain_uuid}}/devices/devicerecords"
)

# Define Headers
HEADERS = {"Content-Type": "application/json"}

# Suppress SSL warnings for self-signed certificates
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# matching_objects = []
# offset = 0
# limit = 3000
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


def find_network_object_id(token, domain_uuid, object_name):
    """Find the ID of a network object (Host or Network) by name."""
    object_types = ["hosts"]  # Both Host and Network objects
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}
    matching_objects = []
    offset = 0
    limit = 3000
    # print(object_name)

    for obj_type in object_types:
        while True:
            url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/{obj_type}?offset={offset}&limit={limit}"
            response = requests.get(url, headers=headers, verify=False)
    
            if response.status_code == 200:
                objects = response.json().get("items", [])
                # pprint(object_name)
                # print(len(objects))

                if not objects:
                    break  # Stop when no more objects are found

                for obj in objects:
                    # pprint(obj["name"])
                    if obj["name"] == object_name:
                        matching_objects.append({"id": obj["id"], "type": obj["type"]})
                offset += limit  # Increment offset for pagination
            else:
                print(f"❌ Failed to retrieve network objects: {response.text}")
                break

    return matching_objects
                
                        # return obj["id"], obj["type"]  # Return the ID and type of object
        # return None, None

# Create Network Objects in FMC if they don't already exist
def create_host_objects(token, domain_uuid):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts"

    headers = {"Content-Type": "application/json", "X-auth-access-token": token}
    
    object_ids = []
    # Data for the new Host Object
    for host in HOSTS:
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

def find_network_object_group_id(token, domain_uuid, group_name):
    """Find the ID of a network object group by name."""
    url = f"{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        groups = response.json().get("items", [])
        for group in groups:
            if group["name"] == group_name:
                return group["id"]  # Return the group ID
    return None

# Create object groups with at least one member
def create_object_groups(token, domain_uuid):
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    for group_name in GROUPS:
        group_id = check_group_exists(token, domain_uuid, group_name)

        # If group exists, skip creation
        if group_id:
            print(f"✅ Object group {group_name} already exists. Skipping creation.")
            continue

        # Find the first host in this group
        first_host = next((host for host in HOSTS if host["group"] == group_name), None)
        print(first_host)

        if not first_host:
            print(f"❌ No hosts found for group {group_name}, skipping creation.")
            continue

        data = {
            "name": group_name,
            "description": f"Object group for {group_name}",
            "type": "NetworkGroup",
            "overridable": False,
            "objects": [{"type": "Host", "name": first_host["name"]}],
        }

        response = requests.post(
            url, headers=headers, data=json.dumps(data), verify=False
        )

        if response.status_code in [200, 201]:
            print(
                f"✅ Successfully created object group {group_name} with {first_host['name']} as initial member"
            )
        else:
            print(f"❌ Failed to create object group {group_name}: {response.text}")



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
            # group_name = "test_3"
            object_name = "test-dc03"
            # create_host_objects(auth_token, domain_uuid)
            # string1 = check_group_exists(auth_token, domain_uuid, group_name)
            # find_network_object_id(auth_token, domain_uuid, object_name)
            matching_objects = find_network_object_id(auth_token, domain_uuid, object_name)
            
            if matching_objects:
                print(f"✅ Found {len(matching_objects)} matching objects:")
                pprint(matching_objects)
            else:
                print(f"❌ No matching objects found for {object_name}")
            # print(string1)
            # print(id)
            # print(type)



if __name__ == "__main__":
    main()
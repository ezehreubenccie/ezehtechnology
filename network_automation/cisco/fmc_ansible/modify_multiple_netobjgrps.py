import requests
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Get FMC credentials from environment variables
FMC_IP = os.getenv("FMC_HOST")
USERNAME = os.getenv("FMC_USERNAME")
PASSWORD = os.getenv("FMC_PASSWORD")

# Host objects with assigned groups
HOSTS = [
    {"name": "test2-dc02", "ip": "10.1.1.2", "group": "test_2"},
    {"name": "test3-dc03", "ip": "10.1.1.3", "group": "test_3"},
    {"name": "test4-dc04", "ip": "10.1.1.4", "group": "test_4"},
    {"name": "test4-dc05", "ip": "10.1.1.5", "group": "test_4"}
]

# List of unique object groups
GROUPS = set(host["group"] for host in HOSTS)

# Suppress SSL warnings for self-signed certificates
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



# Get Authentication Token
def get_auth_token():
    url = f"https://{FMC_IP}/api/fmc_platform/v1/auth/generatetoken"
    response = requests.post(url, auth=(USERNAME, PASSWORD), headers={"Content-Type": "application/json"}, verify=False)

    if response.status_code == 204:
        token = response.headers.get("X-auth-access-token")
        domain_uuid = response.headers.get("DOMAIN-UUID")
        return token, domain_uuid
    else:
        print(f"❌ Failed to get auth token: {response.text}")
        return None, None


# Check if a host object exists
def check_host_exists(token, domain_uuid, host_name):
    url = f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts?filter=nameOrValue:{host_name}"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code == 200:
        existing_hosts = response.json().get("items", [])
        for host in existing_hosts:
            if host["name"] == host_name:
                return True  # Host already exists
    return False  # Host does not exist


# Create a host object if it doesn’t exist
def create_host_objects(token, domain_uuid):
    url = f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/hosts"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    for host in HOSTS:
        if check_host_exists(token, domain_uuid, host["name"]):
            print(f"✅ Host {host['name']} ({host['ip']}) already exists. Skipping creation.")
            continue

        data = {
            "name": host["name"],
            "value": host["ip"],
            "description": f"Host object for {host['name']}",
            "type": "Host",
            "overridable": False
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

        if response.status_code in [200, 201]:
            print(f"✅ Successfully created {host['name']} ({host['ip']})")
        else:
            print(f"❌ Failed to create {host['name']} ({host['ip']}): {response.text}")


# Check if an object group exists
def check_group_exists(token, domain_uuid, group_name):
    url = f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups?filter=nameOrValue:{group_name}"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        existing_groups = response.json().get("items", [])
        for group in existing_groups:
            if group["name"] == group_name:
                return group["id"]  # Return the existing group's ID
    return None  # Group does not exist


# Create object groups if they don’t exist
def create_object_groups(token, domain_uuid):
    url = f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    for group_name in GROUPS:
        group_id = check_group_exists(token, domain_uuid, group_name)

        if group_id:
            print(f"✅ Object group {group_name} already exists. Skipping creation.")
            continue  # Skip if group already exists

        data = {
            "name": group_name,
            "description": f"Object group for {group_name}",
            "type": "NetworkGroup",
            "overridable": False,
            "objects": []  # Initially empty, we'll add members later
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

        if response.status_code in [200, 201]:
            print(f"✅ Successfully created object group {group_name}")
        else:
            print(f"❌ Failed to create object group {group_name}: {response.text}")


# Add host objects to their respective groups
def add_hosts_to_groups(token, domain_uuid):
    url = f"https://{FMC_IP}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    # Fetch existing object groups
    group_ids = {group_name: check_group_exists(token, domain_uuid, group_name) for group_name in GROUPS}

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
        existing_members = {obj["name"] for obj in existing_group_data.get("objects", [])}

        # Find hosts that belong to this group
        hosts_to_add = [host for host in HOSTS if host["group"] == group_name and host["name"] not in existing_members]

        if not hosts_to_add:
            print(f"✅ No new hosts to add to group {group_name}.")
            continue

        # Prepare new member data
        new_members = [{"type": "Host", "name": host["name"]} for host in hosts_to_add]
        existing_group_data["objects"].extend(new_members)

        # Update the group with new members
        update_response = requests.put(group_url, headers=headers, data=json.dumps(existing_group_data), verify=False)

        if update_response.status_code in [200, 201]:
            print(f"✅ Added {', '.join(host['name'] for host in hosts_to_add)} to group {group_name}")
        else:
            print(f"❌ Failed to add hosts to group {group_name}: {update_response.text}")


# Main Execution
if __name__ == "__main__":
    if not all([FMC_IP, USERNAME, PASSWORD]):
        print("❌ Missing environment variables. Please set FMC_IP, FMC_USERNAME, and FMC_PASSWORD.")
    else:
        token, domain_uuid = get_auth_token()
        if token and domain_uuid:
            create_host_objects(token, domain_uuid)
            create_object_groups(token, domain_uuid)
            add_hosts_to_groups(token, domain_uuid)
        else:
            print("❌ Could not retrieve authentication token.")

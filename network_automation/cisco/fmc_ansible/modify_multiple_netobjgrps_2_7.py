#!/usr/bin/env python3

import requests
import json
import os

# FMC Details
FMC_HOST = f'https://{os.getenv("FMC_HOST")}'
USERNAME = os.getenv("FMC_USERNAME")
PASSWORD = os.getenv("FMC_PASSWORD")

# Disable SSL Warnings (Not recommended for production)
requests.packages.urllib3.disable_warnings()


def get_auth_token():
    """Retrieve authentication token from FMC."""
    auth_url = f"{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    response = requests.post(auth_url, auth=(USERNAME, PASSWORD), verify=False)

    if response.status_code == 204:
        return response.headers["X-auth-access-token"], response.headers["DOMAIN_UUID"]
    else:
        raise Exception("Failed to obtain auth token")


def create_network_objects(token, domain_uuid, objects):
    """Create multiple network objects and return their IDs."""
    url = f"{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkaddresses"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}
    object_ids = []

    for obj in objects:
        data = {"name": obj["name"], "value": obj["ip"], "type": "Network"}
        response = requests.post(url, headers=headers, json=data, verify=False)
        if response.status_code in [200, 201]:
            object_ids.append(response.json()["id"])
        else:
            print(f"Failed to create object {obj['name']}: {response.text}")

    return object_ids


def create_network_object_group(token, domain_uuid, group_name, object_ids):
    """Create a network object group with multiple objects."""
    url = f"{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkgroups"
    headers = {"Content-Type": "application/json", "X-auth-access-token": token}

    data = {
        "name": group_name,
        "objects": [{"id": obj_id, "type": "Network"} for obj_id in object_ids],
        "type": "NetworkGroup",
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code in [200, 201]:
        print(f"Network Group '{group_name}' created successfully!")
    else:
        raise Exception(f"Failed to create network group: {response.text}")


if __name__ == "__main__":
    try:
        token, domain_uuid = get_auth_token()

        # Define multiple objects
        network_objects = [
            {"name": "test-dc011", "ip": "10.1.1.11"},
            {"name": "test-dc012", "ip": "10.1.1.12"},
            {"name": "test-dc013", "ip": "10.1.1.13"},
        ]

        object_ids = create_network_objects(token, domain_uuid, network_objects)
        create_network_object_group(token, domain_uuid, "test_2", object_ids)

    except Exception as e:
        print(f"Error: {e}")

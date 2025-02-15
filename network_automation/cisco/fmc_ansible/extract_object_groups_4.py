import requests
import json


# Configuration variables
FMC_HOST = "wa-fmc2500"
DOMAIN_UUID = "e276abec-e0f2-11e3-8169-6d9ed49b625f"
USERNAME = "apiuser"
PASSWORD = "Xs0PC8VPMoxkuooXVreb"
TARGET_IPS = {"10.1.101.100", "10.2.101.100", "192.168.0.12"}  # Set of target IPs

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

def get_auth_token():
    """
    Authenticate with FMC and retrieve the access token.
    """
    url = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
    if response.status_code == 204:
        return response.headers["X-auth-access-token"]
    else:
        raise Exception(f"Failed to authenticate. Status code: {response.status_code}, Response: {response.text}")
    
def fetch_all_network_groups(token):
    """
    Fetch all network groups using the FMC API, handling pagination.
    """
    all_network_groups = []
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{DOMAIN_UUID}/object/networkgroups?limit=25"
    headers = {
        "Content-Type": "application/json",
        "X-auth-access-token": token
    }

    while url:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch network groups. Status code: {response.status_code}, Response: {response.text}")

        data = response.json()
        all_network_groups.extend(data.get("items", []))
        # Get the next URL from the paging section
        url = data.get("paging", {}).get("next", [None])[0]

    return all_network_groups

def fetch_group_details(token, group_id):
    """
    Fetch detailed information about a specific network group.
    """
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{DOMAIN_UUID}/object/networkgroups/{group_id}"
    headers = {
        "Content-Type": "application/json",
        "X-auth-access-token": token
    }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch details for group {group_id}. Status code: {response.status_code}, Response: {response.text}")
    return response.json()

def filter_network_groups_by_ips(network_groups, token, target_ips):
    """
    Filter network groups to find those containing the specified IPs.
    """
    matched_groups = []
    for group in network_groups:
        # Fetch detailed information about the group
        group_details = fetch_group_details(token, group["id"])
        group_objects = group_details.get("objects", [])
        group_ips = {obj.get("value") for obj in group_objects if obj.get("type") == "Host"}
        # Check if any target IP is in the group
        if target_ips.intersection(group_ips):
            matched_groups.append(group_details)
    return matched_groups

def main():
    """
    Main function to authenticate, fetch, and filter network groups.
    """
    try:
        print("Authenticating with FMC...")
        token = get_auth_token()
        print("Fetching all network groups...")
        network_groups = fetch_all_network_groups(token)
        print(f"Fetched {len(network_groups)} network groups.")

        print(f"Filtering network groups for IPs: {', '.join(TARGET_IPS)}")
        matched_groups = filter_network_groups_by_ips(network_groups, token, TARGET_IPS)
        print(f"Found {len(matched_groups)} matching network groups.")

        # Print the results in a readable format
        print(json.dumps(matched_groups, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
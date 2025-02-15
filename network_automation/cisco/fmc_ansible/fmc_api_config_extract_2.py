import requests
import json

# Suppress SSL warnings for self-signed certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Replace with your FMC details
FMC_HOST = "<FMC_IP_OR_HOSTNAME>"
USERNAME = "<USERNAME>"
PASSWORD = "<PASSWORD>"

# API endpoints
FMC_LOGIN_URL = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
FMC_DEVICE_URL = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{{domain_uuid}}/devices/devicerecords"
FMC_ACCESS_RULES_URL = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{{domain_uuid}}/policy/accesspolicies/{{policy_id}}/accessrules"
FMC_NAT_POLICIES_URL = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{{domain_uuid}}/policy/natpolicies"
FMC_VPN_SETTINGS_URL = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{{domain_uuid}}/devices/vpnconfig"

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
def get_device_configurations(auth_token, domain_uuid):
    headers = {
        "Content-Type": "application/json",
        "X-auth-access-token": auth_token
    }

    device_url = FMC_DEVICE_URL.format(domain_uuid=domain_uuid)
    response = requests.get(device_url, headers=headers, verify=False)

    if response.status_code == 200:
        devices = response.json()["items"]
        print(f"Retrieved {len(devices)} devices.")
        return devices
    else:
        print(f"Failed to retrieve devices: {response.text}")
        exit()

# Function to retrieve access rules
def get_access_rules(auth_token, domain_uuid, policy_id):
    headers = {
        "Content-Type": "application/json",
        "X-auth-access-token": auth_token
    }

    access_rules_url = FMC_ACCESS_RULES_URL.format(domain_uuid=domain_uuid, policy_id=policy_id)
    response = requests.get(access_rules_url, headers=headers, verify=False)

    if response.status_code == 200:
        access_rules = response.json()["items"]
        print(f"Retrieved {len(access_rules)} access rules.")
        return access_rules
    else:
        print(f"Failed to retrieve access rules: {response.text}")
        exit()

# Function to retrieve NAT policies
def get_nat_policies(auth_token, domain_uuid):
    headers = {
        "Content-Type": "application/json",
        "X-auth-access-token": auth_token
    }

    response = requests.get(FMC_NAT_POLICIES_URL.format(domain_uuid=domain_uuid), headers=headers, verify=False)

    if response.status_code == 200:
        nat_policies = response.json()["items"]
        print(f"Retrieved {len(nat_policies)} NAT policies.")
        return nat_policies
    else:
        print(f"Failed to retrieve NAT policies: {response.text}")
        exit()

# Function to retrieve VPN settings
def get_vpn_settings(auth_token, domain_uuid):
    headers = {
        "Content-Type": "application/json",
        "X-auth-access-token": auth_token
    }

    response = requests.get(FMC_VPN_SETTINGS_URL.format(domain_uuid=domain_uuid), headers=headers, verify=False)

    if response.status_code == 200:
        vpn_settings = response.json()
        print("Retrieved VPN settings.")
        return vpn_settings
    else:
        print(f"Failed to retrieve VPN settings: {response.text}")
        exit()

# Function to save configuration details to a file
def save_to_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Configuration saved to {filename}")

# Main logic
def main():
    print("Authenticating with FMC...")
    auth_token, domain_uuid = get_auth_token()

    print("Fetching device configurations...")
    devices = get_device_configurations(auth_token, domain_uuid)
    save_to_file("device_configurations.json", devices)

    print("Fetching access rules for a policy...")
    # Replace with a specific policy_id for your environment
    policy_id = "<ACCESS_POLICY_ID>"
    access_rules = get_access_rules(auth_token, domain_uuid, policy_id)
    save_to_file("access_rules.json", access_rules)

    print("Fetching NAT policies...")
    nat_policies = get_nat_policies(auth_token, domain_uuid)
    save_to_file("nat_policies.json", nat_policies)

    print("Fetching VPN settings...")
    vpn_settings = get_vpn_settings(auth_token, domain_uuid)
    save_to_file("vpn_settings.json", vpn_settings)

    print("Process completed.")

if __name__ == "__main__":
    main()

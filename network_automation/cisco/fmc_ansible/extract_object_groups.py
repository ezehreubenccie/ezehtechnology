import requests
import json

# Configuration variables
FMC_HOST = "wa-fmc2500"
DOMAIN_UUID = "e276abec-e0f2-11e3-8169-6d9ed49b625f"
USERNAME = "apiuser"
PASSWORD = "Xs0PC8VPMoxkuooXVreb"

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
    


def main():
    """
    Main function to authenticate and fetch all network groups.
    """
    try:
        print("Authenticating with FMC...")
        token = get_auth_token()
        # print(token)
        print("Fetching all network groups...")
        network_groups = fetch_all_network_groups(token)
        print(f"Fetched {len(network_groups)} network groups.")
        # Print the results in a readable format
        print(json.dumps(network_groups, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

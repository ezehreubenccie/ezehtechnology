#!/usr/bin/env python3

import json
import sys
import csv
import time
from getpass import getpass
from argparse import ArgumentParser
from pprint import pprint

# External Packages
import requests

# Disable insecure connection warnings on destinations with untrusted certificates
requests.packages.urllib3.disable_warnings()

# Global variables to hold existing FMC object data
object_data = {
    'ikeV1PolicyObjects': [],
    'ikeV2PolicyObjects': [],
    'networkObjects': [],
    'ftdEndpoints': {}
}

def verbose_output(func_name, response):
    """
    Function to print out the full HTTP response data from API calls, when verbose option is chosen.
    params: func_name (str), response (Requests response object)
    """
    pprint(
        f"{func_name} Response:\nStatus Code: {response.status_code}\nHeaders: {response.headers}\nPayload: {response.text}\n'"
    )

    return


def auth(args):
    """
    Authenticate to the FMC server and obtain a token.
    params: ArgParse namespace object
    returns: token (str), refresh_token (str), domain_uuid (str)
    """
    # If user didn't specify a password, prompt them interactively.
    # Passwords with special characters can be problematic as CLI arguments.
    if not args.password:
        password = getpass("Please enter the FMC password: ", stream=None)
    else:
        password = args.password

    url = f"https://{args.fmc_server}/api/fmc_platform/v1/auth/generatetoken"
    headers = {"Content-Type": "application/json"}

    if args.cert_path:
        response = requests.post(
            url,
            headers=headers,
            auth=requests.auth.HTTPBasicAuth(args.username, password),
            verify=args.cert_path,
        )
    else:
        response = requests.post(
            url,
            headers=headers,
            auth=requests.auth.HTTPBasicAuth(args.username, password),
            verify=False,
        )

    if args.verbose:
        verbose_output("auth()", response)
        # print(type(response))

    if (
        response.status_code in [200, 204]
        and response.headers["X-auth-access-token"] != ""
    ):
        token = response.headers["X-auth-access-token"]
        refresh_token = response.headers["X-auth-refresh-token"]
        domain_uuid = response.headers["DOMAIN_UUID"]
        return token, refresh_token, domain_uuid
    else:
        print("Error encountered during authentication:\n")
        # Use verbose_output() to print out response details
        verbose_output("auth()", response)
        sys.exit(1)

def get_ike_object(args, token, domain_uuid):
    """
    Function to obtain data about IKE Policy Objects in FMC.  Updates global variable with results.
    params: ArgParse namespace object, token (str), domain_uuid (str)
    """
    global object_data
    offset = 0
    limit = 600

    urlIkeV1 = f'https://{args.fmc_server}/api/fmc_config/v1/domain/{domain_uuid}/object/ikev1policies'
    urlIkeV2 = f'https://{args.fmc_server}/api/fmc_config/v1/domain/{domain_uuid}/object/ikev2policies'

    headers = {
        'Content-Type': 'application/json',
        'X-auth-access-token': token
    }
    if args.cert_path:
        responseV1 = requests.get(urlIkeV1, headers=headers, verify=args.cert_path)
        responseV2 = requests.get(urlIkeV2, headers=headers, verify=args.cert_path)
    else:
        responseV1 = requests.get(urlIkeV1, headers=headers, verify=False)
        responseV2 = requests.get(urlIkeV2, headers=headers, verify=False)
    
    # if args.verbose:
    #     verbose_output('get_ike_object()', responseV1)
    #     verbose_output('get_ike_object()', responseV2)
    
    if responseV1.status_code in [200]:
        object_data['ikeV1PolicyObjects'] = responseV1.json()['items']
        # print("\n\nIKEV1 Policy Objects\n")
        # pprint(object_data['ikeV1PolicyObjects'])
    else:
        print(f'!!!!!!!!!!\nError encountered when obtaining details about IKE Policy Objects."\n!!!!!!!!!!\n')
        verbose_output('get_ike_object()', responseV1)
    
    if responseV2.status_code in [200]:
        object_data['ikeV2PolicyObjects'] = responseV2.json()['items']
        # print("\n\nIKEV2 Policy Objects\n")
        # pprint(object_data['ikeV2PolicyObjects'])
    else:
        print(f'!!!!!!!!!!\nError encountered when obtaining details about IKE Policy Objects."\n!!!!!!!!!!\n')
        verbose_output('get_ike_object()', responseV2)

def get_network_objects(args, token, domain_uuid):
    """
    Function to obtain data about Network Objects in FMC.  Updates global variable with results.
    params: ArgParse namespace object, token (str), domain_uuid (str)
    """
    global object_data
    offset = 0
    limit = 600

    # url = f'https://{args.fmc_server}/api/fmc_config/v1/domain/{domain_uuid}/object/networks'
    url = f'https://{args.fmc_server}/api/fmc_config/v1/domain/{domain_uuid}/object/networks?offset={offset}&limit={limit}'

    headers = {
        'Content-Type': 'application/json',
        'X-auth-access-token': token
    }
    if args.cert_path:
        response = requests.get(url, headers=headers, verify=args.cert_path)
    else:
        response = requests.get(url, headers=headers, verify=False)
    
    if args.verbose:
        verbose_output('get_network_objects()', response)
    
    if response.status_code in [200]:
        object_data['networkObjects'] = response.json()['items']
        print("\n\nNetwork Objects\n\n")
        pprint(object_data['networkObjects'])
        print(len(object_data['networkObjects']))

    else:
        print(f'!!!!!!!!!!\nError encountered when obtaining details about Network Objects."\n!!!!!!!!!!\n')
        verbose_output('get_network_objects()', response)


def get_device_details(args, token, domain_uuid, input_data):
    """
    Function to obtain details of Devices in FMC.
    params: ArgParse namespace object, token (str), domain_uuid (str), input_data (list)
    """
    global object_data

    url = f'https://{args.fmc_server}/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords'

    headers = {
        'Content-Type': 'application/json',
        'X-auth-access-token': token
    }

    for item in input_data:
        # Check if data was already collected on this device and pass
        if object_data['ftdEndpoints'].get(item['device_name']):
            pass
        # If data not already collected, move ahead and collect
        else:
            object_data['ftdEndpoints'][item["device_name"]] = {}
            # Filter results to just this device name in FMC
            params = {
                'filter': f'name:{item["device_name"]}'
            }
            if args.cert_path:
                response = requests.get(url, headers=headers, params=params, verify=args.cert_path)
            else:
                response = requests.get(url, headers=headers, params=params, verify=False)
            
            if args.verbose:
                verbose_output('get_device_details()', response)
            
            if response.status_code in [200]:
                for device in response.json()['items']:
                    if item['device_name'] == device['name']:
                        object_data['ftdEndpoints'][item['device_name']] = device
                        # Call helper function to gather interface details next
                        object_data['ftdEndpoints'][item['device_name']]['interfaces'] = get_device_interfaces(args, token, domain_uuid, device['id'])
                    else:
                        # If device is not found in the response payload, then take this action.
                        print(f'!!!!!!!!!!\nDevice Name {item["device_name"]}specified in input data was not found."\n!!!!!!!!!!\n')
                        verbose_output('get_device_details()', response)
            else:
                print(f'!!!!!!!!!!\nError encountered when obtaining details about device {item["device_name"]}."\n!!!!!!!!!!\n')
                verbose_output('get_device_details()', response)


def get_device_interfaces(args, token, domain_uuid, device_uuid):
    """
    Helper function to obtain interface details of a device in FMC.
    params: ArgParse namespace object, token (str), domain_uuid (str), device_uuid (str)
    returns: interfaces (list)
    """
    url = f'https://{args.fmc_server}/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords/{device_uuid}/ftdallinterfaces'

    headers = {
        'Content-Type': 'application/json',
        'X-auth-access-token': token
    }
    # Request full details to be returned, not just summary (only way to get the "ifname" key in response data, which contains interface's "Logical Name")
    params = {
        "expanded": True
    }

    if args.cert_path:
        response = requests.get(url, headers=headers, params=params, verify=args.cert_path)
    else:
        response = requests.get(url, headers=headers, params=params, verify=False)
    
    if args.verbose:
        verbose_output('get_device_interfaces()', response)

    if response.status_code in [200]:
        return response.json()['items']
    else:
        print(f'!!!!!!!!!!\nError encountered when obtaining interface details about device with UUID: {device_uuid}."\n!!!!!!!!!!\n')
        verbose_output('get_device_details()', response)
        return []





def main(args):
    """
    Main function to control workflow in this script.
    params: args (ArgParse Namespace object)
    """

    # Check input file extension and parse input data
    # extension = args.input_file.split('.')[1].lower()
    # if extension == 'csv':
    #     input_data = csv_to_json(args)
    # elif extension in ['yml', 'yaml']:
    #     input_data = yaml_to_json(args)
    # else:
    #     print(f'Input file extension "{extension}" is not supported.')
    #     sys.exit(1)

    # Authenticate to FMC and obtain token
    token, refresh_token, domain_uuid = auth(args)

    # Get IKE Policy Object information
    get_ike_object(args, token, domain_uuid)

    # # Get Network Object information
    get_network_objects(args, token, domain_uuid)

    # # Get details about FTD Device
    get_device_details(args, token, domain_uuid, input_data)

    # If user chose "collect_data" option, only perform GET requests and then write output to file.
    # if args.collect_data:
    #     # Nested JSON does not flatten into CSV very well, so write to text file.
    #     filename = write_to_text(object_data, 'object_data')
    #     print(f'\n**********\nResults saved to output file {filename}\n**********')
    # else:
    #     # Create the S2S VPN Policy object and all supporting configurations
    #     result = create_s2s_policy(args, token, domain_uuid, input_data)
    #     # Write results to an appropriate filetype, based on input file.
    #     if extension == 'csv':
    #         filename = write_to_csv(result)
    #     elif extension in ['yml', 'yaml']:
    #         filename = write_to_yaml(result)
    #     print(f'\n**********\nResults saved to output file {filename}\n**********')


# If this script is executed directly from the Python interpreter (not imported into another script), collect CLI arguments and then call main() function.
if __name__ == "__main__":
    parser = ArgumentParser(description="Select your options:")
    parser.add_argument(
        "--username", "-u", type=str, required=True, help="FMC Username"
    )
    parser.add_argument(
        "--password", "-p", type=str, required=False, help="FMC Password"
    )
    parser.add_argument(
        "--fmc_server", "-s", type=str, required=True, help="FMC Server IP"
    )
    parser.add_argument(
        "--cert_path",
        "-c",
        type=str,
        required=False,
        help="Path to FMC cert, if you choose to verify it.",
    )
    parser.add_argument(
        "--input_file",
        "-f",
        type=str,
        required=False,
        help="Filename of the configuration input file.  Accepts CSV and YAML formats.",
    )
    parser.add_argument(
        "--collect_data",
        action="store_true",
        help="Only make GET API calls to collect object data from FMC, then save results to output files.",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print verbose output"
    )
    args = parser.parse_args()

    main(args)

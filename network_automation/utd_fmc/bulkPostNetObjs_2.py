#!/usr/bin/python3
"""
File: bulkPostNetObjs.py
Inputs:
    Username
    Password
    FMC IP Address
    CSV file with network objects for a bulk import
Outputs: 
    none

To use this file as a standalone script, the username, password, & FMC IP
will need to be passed in as command-line arguments.

Author: suddesai@cisco.com
H/T: namiagar@cisco.com for assistance in troubleshooting this script

---
MIT License

Copyright (c) 2021 Sudhir H. Desai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# include the necessary modules
import argparse
import json
import requests
import textwrap
import requestToken as token
from pprint import pprint


# if we're using this as a stand-alone script, run the following
if __name__ == "__main__":
    # first set up the command line arguments and parse them
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("username", type=str, help ="API username")
    parser.add_argument("password", type=str, help="password of API user")
    parser.add_argument("ip_address", type=str, help="IP of FMC")
    parser.description = textwrap.dedent('''\
...         input file formatting – one name per line
...         --------------------------------
...         name,value,description,overridable,type
    ''')
    parser.add_argument("csvInput", type=str,
        help="provide the csv of network objects \
            to add.")
    args = parser.parse_args()

    # set needed variables to generate a token
    u = args.username
    p = args.password
    ip = args.ip_address
    path = "/api/fmc_platform/v1/auth/generatetoken"
    header = {} # don't need to instantiate this, but doing so for clarity
    payload = [] # don't need to instantiate this, but doing so for clarity

    # call the token generating function and populate our header
    header = token.get_token(ip, path, u, p)
    print('This is my header')
    print(header)
    # we need to update our path to account for the domain UUID as follows
    path = f"/api/fmc_config/v1/domain/{header['DOMAIN_UUID']}/object/networks?bulk=true"

    # and process the file into the payload
    with open(args.csvInput) as file:
        for netObjs in file:
            netObj = netObjs.strip().split(',')
            try: # try block in case something unexpected occurs
                netObject = f'{{"name": "{netObj[0]}","value": "{netObj[1]}","overridable": {netObj[2]},"description": "{netObj[3]}","type": "{netObj[4]}"}}'
                payload.append(json.loads(netObject))

            except Exception as err:
                raise SystemExit(err)
                
    header_f = {"accept": "application/json", "Content-Type": "application/json", "X-auth-access-token": header['X-auth-access-token']}

    print("This is my payload...")
    print(json.dumps(payload, indent=4))
    # now to POST our list of network objects
    try:
        r = requests.post(f"https://{ip}/{path}", headers=header_f, data=json.dumps(payload), verify=False)
        
        print("This is the request body..")
        pprint(r.request.body)
        pprint("Headers: " + str(r.headers) + "\n")
        pprint("Text: " + str(r.text) + "\n")
        pprint("Status Code: " + str(r.status_code))

    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

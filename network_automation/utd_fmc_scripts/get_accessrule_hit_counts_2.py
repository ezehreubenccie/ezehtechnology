#!/usr/bin/env python3

import requests
from cisco_fmc import CiscoFMC
import pprint
import json

protocol = 'https'
hostname = 'wa-fmc2500'
domain_id = 'e276abec-e0f2-11e3-8169-6d9ed49b625f'
accesspolicy_id = '40CE2481-5D56-0ed3-0000-081604388814'
device_id = '1b37e462-f66c-11de-9aca-a60da3d3d96a'
offset = 0
limit = 600



url = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/policy/accesspolicies/{accesspolicy_id}/operational/hitcounts?offset={offset}&limit={limit}&filter=deviceId:{device_id}&expanded=True"

fmc = CiscoFMC.build_from_env_vars()

payload = {}
headers = {
  'X-auth-access-token': fmc.headers["X-auth-access-token"]
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

#print(type(response.text))
response_dict = json.loads(response.text)
print(type(response_dict))
#pprint.pprint(response.text)
pprint.pprint(response_dict)

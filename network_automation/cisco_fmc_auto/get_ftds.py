#!/usr/bin/env python3

import requests
import json
import os

class CiscoFMC:
    '''
    Python client SDK for Cisco FMC.
    '''

    def __init__(
        self,
        username,
        password,
        host='cdcfmc01',
        verify=False,
    ):
        '''
        Constructor for the class
        '''

        # Store all input parameters and assemble base URL
        self.username = username
        self.password = password
        self.verify = verify
        self.base_url = f'https://{host}/api'

        # if we aren't verifying SSL certificates, disable obnoxious warnings
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # Create a stateful HTTPS session to improve performance
        self.sess = requests.session()
url = "https://cdcfmc01/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords"

payload={}
headers = {
  'X-auth-access-token': 'f53d4be2-1c78-4366-8537-ccedc1988220',
  'X-auth-refresh-token': 'f4c85def-2548-4922-872f-bce136a3d5fb'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

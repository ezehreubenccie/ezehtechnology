#!/usr/bin/env python3




import requests

url = "https://cdcfmc01/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords"

payload={}
headers = {
  'X-auth-access-token': 'f53d4be2-1c78-4366-8537-ccedc1988220',
  'X-auth-refresh-token': 'f4c85def-2548-4922-872f-bce136a3d5fb'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

#!/usr/bin/env python3

import requests
from cisco_fmc import CiscoFMC
import pprint
import json

protocol = "https"
hostname = "wa-fmc2500"
domain_id = "e276abec-e0f2-11e3-8169-6d9ed49b625f"
#accesspolicy_id = "40CE2481-5D56-0ed3-0000-081604388814"
#device_id = "1b37e462-f66c-11de-9aca-a60da3d3d96a"
offset = 0
limit = 600


#url = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/policy/accesspolicies/{accesspolicy_id}/operational/hitcounts?offset={offset}&limit={limit}&filter=deviceId:{device_id}&expanded=True"
url = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/object/networkgroups?offset={offset}&limit={limit}"

fmc = CiscoFMC.build_from_env_vars()

payload = {}
headers = {"X-auth-access-token": fmc.headers["X-auth-access-token"]}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

#print(type(response.text))
response_dict = json.loads(response.text)
print(type(response_dict))
#pprint.pprint(response.text)
pprint.pprint(response_dict)

# print(type(response_dict["items"]))

# print(len(response_dict["items"]))

""" NY_rule_hits = open("NY1_rule_hit_export.csv", "w")
NY_rule_hits.write("RuleName,RuleID,Hit Count,First Hit Time(EST),Last Hit Time(EST)\n")
for item in response_dict["items"]:
    rulename = item["rule"]["name"]
    ruleid = item["metadata"]["deviceRuleId"]
    hitcount = item["hitCount"]
    firsthit = item["firstHitTimeStamp"]
    lasthit = item["lastHitTimeStamp"]

    line = rulename + "," + ruleid + "," + str(hitcount) + "," + firsthit + "," + lasthit
    NY_rule_hits.write(f"{line}\n")

NY_rule_hits.close() """

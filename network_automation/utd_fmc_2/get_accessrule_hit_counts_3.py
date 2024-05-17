#!/usr/bin/env python3

import requests
from cisco_fmc import CiscoFMC
import pprint
import json

protocol = "https"
hostname = "wa-fmc2500"
domain_id = "e276abec-e0f2-11e3-8169-6d9ed49b625f"
accesspolicy_id = "40CE2481-5D56-0ed3-0000-292057859955"
device_id = "a6eddfc4-0bd5-11ee-9960-a6db2169469d"
offset = 0
limit = 600


url = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/policy/accesspolicies/{accesspolicy_id}/operational/hitcounts?offset={offset}&limit={limit}&filter=deviceId:{device_id}&expanded=True"

fmc = CiscoFMC.build_from_env_vars()

payload = {}
headers = {"X-auth-access-token": fmc.headers["X-auth-access-token"]}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

# print(type(response.text))
response_dict = json.loads(response.text)
# print(type(response_dict))
# pprint.pprint(response.text)
# pprint.pprint(response_dict)

# print(type(response_dict["items"]))

# print(len(response_dict["items"]))

Waltham_INET_rule_hits = open("Waltham_INET_rule_hit_export.csv", "w")
Waltham_INET_rule_hits.write("RuleName,RuleID,Hit Count,First Hit Time(EST),Last Hit Time(EST)\n")
for item in response_dict["items"]:
    rulename = item["rule"]["name"]
    ruleid = item["metadata"]["deviceRuleId"]
    hitcount = item["hitCount"]
    firsthit = item["firstHitTimeStamp"]
    lasthit = item["lastHitTimeStamp"]

    line = rulename + "," + ruleid + "," + str(hitcount) + "," + firsthit + "," + lasthit
    Waltham_INET_rule_hits.write(f"{line}\n")

Waltham_INET_rule_hits.close()

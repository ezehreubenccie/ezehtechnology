#!/usr/bin/env python3

import requests
from cisco_fmc import CiscoFMC
import pprint
import json

# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry


def retry_request(url, total=4, status_forcelist=[429, 500, 502, 503, 504], **kwargs):
    # Make number of requests required
    for i in range(total):
        try:
            # response = requests.get(url, **kwargs)
            response = requests.request("GET", url)
            if response.status_code in status_forcelist:
                # Retry request
                continue
            return response
        except requests.exceptions.ConnectionError:
            pass
    return None


if __name__ == "__main__":
    protocol = "https"
    hostname = "wa-fmc2500"
    domain_id = "e276abec-e0f2-11e3-8169-6d9ed49b625f"
    # accesspolicy_id = "40CE2481-5D56-0ed3-0000-081604388814"
    # device_id = "1b37e462-f66c-11de-9aca-a60da3d3d96a"
    offset = 0
    limit = 600

    # url = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/policy/accesspolicies/{accesspolicy_id}/operational/hitcounts?offset={offset}&limit={limit}&filter=deviceId:{device_id}&expanded=True"
    # url = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/object/networkgroups?offset={offset}&limit={limit}"
    url = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/object/networkgroups?offset={offset}&limit={limit}"

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

    # NY_rule_hits = open("NY1_rule_hit_export.csv", "w")
    # NY_rule_hits.write("RuleName,RuleID,Hit Count,First Hit Time(EST),Last Hit Time(EST)\n")
    netgrp_id_list = []
    netgrp_name_list = []
    for item in response_dict["items"]:
        netgrp_id = item["id"]
        netgrp_name = item["name"]

        netgrp_id_list.append(netgrp_id)
        netgrp_name_list.append(netgrp_name)

    # pprint.pprint(netgrp_name_list)
    # print(f"There are {len(netgrp_name_list)} object groups.")
    # pprint.pprint(netgrp_id_list)
    # print(f"There are {len(netgrp_id_list)} object groups ids.")
    status_code = []
    ObjGrps = open("obj_grp_ips.csv", "w")
    ObjGrps.write("Name,IP Addresses\n")
    for id in netgrp_id_list[0:12]:
        url_for_objgrp_lit = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/object/networkgroups/{id}"
        # print(url_for_objgrp_lit)
        response_lit = requests.request(
        "GET", url_for_objgrp_lit, headers=headers, data=payload, verify=False
        )
        # response_lit = retry_request(
        #     url_for_objgrp_lit, headers=headers, data=payload, verify=False
        # )
        # print(response_lit)
        response_lit_dict = json.loads(response_lit.text)
        pprint.pprint(response_lit_dict)
        name = response_lit_dict["name"]
        # ip_addresses = response_lit_dict["literals"]
        print(name)
    #     print(ip_addresses)
    #     ips = []
    #     for ip in ip_addresses:
    #         ips.append(ip["value"])
    #     print(ips)
    #     ipsj = " ".join(ips)
    #     line = f"{name},{ipsj}"
    #     ObjGrps.write(f"{line}\n")
    # ObjGrps.close()

        

    # print(dir(response_lit))
    # print(response_lit.status_code)
    # status_code.append(response_lit.status_code)
    # pprint.pprint(status_code)

    # ruleid = item["metadata"]["deviceRuleId"]
    # hitcount = item["hitCount"]
    # firsthit = item["firstHitTimeStamp"]
    # lasthit = item["lastHitTimeStamp"]

    # line = rulename + "," + ruleid + "," + str(hitcount) + "," + firsthit + "," + lasthit
    # NY_rule_hits.write(f"{line}\n")

    # NY_rule_hits.close()

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
    netgrp_id_list_100 = netgrp_id_list[602:702]
    # pprint.pprint(netgrp_id_list_100)
    # print(f"There are {len(netgrp_id_list)} object groups ids.")
    status_code = []
    # ips = []
    ObjGrps = open("obj_grp_ips_5.csv", "w")
    ObjGrps.write("Name,IP Addresses\n")
    for id in netgrp_id_list_100:
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
        name = response_lit_dict["name"]
        # pprint.pprint(response_lit_dict)
        # pprint.pprint(response_lit_dict["objects"])
        # ips = []
        if "literals" in response_lit_dict:
            # pprint.pprint(response_lit_dict['literals'])
            # ips.append(response_lit_dict['literals'])
            # pprint.pprint(ips[0][0])
            # print(type(ips[0]))
            ip_addresses = response_lit_dict["literals"]
        #     print(ip_addresses[0][1]["value"])
            for ip in ip_addresses:
                # ips = []
                print(f'{name},{ip["value"]}')
            # pprint.pprint(ips)
            # ipsj = " ".join(ips)
            # line = f"{name},{ipsj}"
            # print(line)
            # ObjGrps.write(f"{line}\n")
        # if "objects" in response_lit_dict:
        #     for obj in response_lit_dict["objects"]:
        #         if "Host" == response_lit_dict["objects"][0]["type"]:
        #             urlobj = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/object/hosts/{obj['id']}"
        #             response_obj = requests.request(
        #                 "GET", urlobj, headers=headers, data=payload, verify=False
        #             )
        #             response_obj_dict = json.loads(response_obj.text)
        #             # pprint.pprint(response_obj_dict)
        #             name = response_obj_dict["name"]
        #             ip = response_obj_dict["value"]
        #             print(f"{name},{ip}")
        # #             line_host = f"{name},{ip}"
        # #             ObjGrps.write(f"{line_host}\n")

        #         if "Range" == response_lit_dict["objects"][0]["type"]:
        #             urlobjrg = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/object/ranges/{obj['id']}"
        #             response_obj_rg = requests.request(
        #                 "GET", urlobjrg, headers=headers, data=payload, verify=False
        #             )
        #             response_obj_dict_rg = json.loads(response_obj_rg.text)
        #             # pprint.pprint(response_obj_dict)
        #             name = response_obj_dict_rg["name"]
        #             ip = response_obj_dict_rg["value"]
        #             print(f"{name},{ip}")
        #             # line_range = f"{name},{ip}"
        #             # ObjGrps.write(f"{line_range}\n")

        #         if "Network" == response_lit_dict["objects"][0]["type"]:
        #             urlobjnet = f"{protocol}://{hostname}/api/fmc_config/v1/domain/{domain_id}/object/networks/{obj['id']}"
        #             response_obj_net = requests.request(
        #                 "GET", urlobjnet, headers=headers, data=payload, verify=False
        #             )
        #             response_obj_dict_net = json.loads(response_obj_net.text)
        #             # pprint.pprint(response_obj_dict)
        #             name = response_obj_dict_net["name"]
        #             ip = response_obj_dict_net["value"]
        #             print(f"{name},{ip}")
        #             line_network = f"{name},{ip}"
        #             ObjGrps.write(f"{line_network}\n")
    # ObjGrps.close()
    # name = response_lit_dict["name"]
    # ip_addresses = response_lit_dict["literals"]
    # print(name)
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

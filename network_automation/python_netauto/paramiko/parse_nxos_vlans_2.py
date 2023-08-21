#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Develop VLAN configuration parsers for NXOS.
These are focused on vlans and not general-purpose VLAN fields
"""

import re
import pprint
import regex


def parse_vlan_nxos(text):
    """
    Parses blocks of VLAN text into indexable dictionary entries. This
    typically feeds into the vlan_diff function to be tested against the
    intended config
    """
    # print(text)
    lines = regex.split(r"\n(?=[^\s])", text)
    # pprint.pprint(lines)
    lines = lines[2:]
    return_dict = {}
    for line in lines:
        name_regex = re.compile(r"\d{1,3}\s+(?P<vlan_name>\S+)")
        name_match = name_regex.search(line)
        # print(name_match)
        sub_dict = {}
        vlan_dict = {name_match.group("vlan_name"): sub_dict}
        # pprint.pprint(vlan_dict)

        # Parse assigned ports
        port_regex = re.compile(r"(?P<assn_ports>Eth\d{1,3}\/\d{1,3})")
        port_matches = port_regex.findall(line)
        sub_dict.update({"assg_ports": port_matches})
        # print(sub_dict)

        # Parse vlan status
        status_regex = re.compile(r"(?P<status>active|suspended|act\/lshut)")
        status_matches = status_regex.search(line)
        sub_dict.update({"status": status_matches.group("status")})
        # print(sub_dict)

        # Parse vlan id
        vlan_id_regex = re.compile(r"\d{1,3}")
        vlan_id_matches = vlan_id_regex.search(line)
        # print(vlan_id_matches.group())
        sub_dict.update({"vlan_number": vlan_id_matches.group()})
        # print(sub_dict)

        # Append dictionary to return list
        return_dict.update(vlan_dict)

    return return_dict


if __name__ == "__main__":
    text = """
        VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Eth1/2, Eth1/3, Eth1/4, Eth1/5
                                                Eth1/6, Eth1/9, Eth1/12, Eth1/13
                                                Eth1/14, Eth1/15, Eth1/16
                                                Eth1/17, Eth1/18, Eth1/19
                                                Eth1/20, Eth1/21, Eth1/22
                                                Eth1/23, Eth1/24, Eth1/25
                                                Eth1/26, Eth1/27, Eth1/28
                                                Eth1/29, Eth1/30, Eth1/31
                                                Eth1/32, Eth1/33, Eth1/34
                                                Eth1/35, Eth1/36, Eth1/37
                                                Eth1/38, Eth1/39, Eth1/40
                                                Eth1/41, Eth1/42, Eth1/43
                                                Eth1/44, Eth1/45, Eth1/46
                                                Eth1/47, Eth1/48, Eth1/49
                                                Eth1/50, Eth1/51, Eth1/52
                                                Eth1/53, Eth1/54, Eth1/55
                                                Eth1/56, Eth1/57, Eth1/58
                                                Eth1/59, Eth1/60, Eth1/61
                                                Eth1/62, Eth1/63, Eth1/64
101  SR-DB-SERVERS                    active    Eth1/10
110  SR-LAB-0                         active    
211  NOBODY                           active    
222  TEST                             active    
254  SR-MGMT-1                        active    Eth1/7, Eth1/8, Eth1/11
"""

vlan_dict_1 = parse_vlan_nxos(text)
pprint.pprint(vlan_dict_1)
print()
print(len(vlan_dict_1))

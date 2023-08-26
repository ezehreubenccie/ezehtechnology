#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: The pytest functions for ensuring vlan configuration parsers
for nxos are functional. Run with "-s" to see outputs.
"""

from parse_nxos_vlans_6 import parse_vlan_nxos, vlan_diff
import pprint

def test_parse_vlan_nxos():
    """
    Defines unit tests for the Cisco NXOS VLANS parser.
    """

    # Create and display some test data
    vlan_output = """
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

    print(vlan_output)

    # Perform parsing, print structured data, and validate
    vlan_data = parse_vlan_nxos(vlan_output)
    print(vlan_data)
    _check_vlan_data(vlan_data)


def test_vlan_diff():
    """
    Ensure the set theory logic functions correctly
    """
    run_vlan_dict = {
        "NOBODY": {
            "assg_ports": ["Eth1/15"],
            "status": "disabled",
            "vlan_number": "120",
        },
        "SR-LAB-0": {
            "assg_ports": ["Eth1/23", "Eth1/35"],
            "status": "active",
            "vlan_number": "122",
        },
    }

    int_vlan_list = [
        {"name": "NOBODY", "vlan_number": "211", "status": "active", "assg_ports": []},
        {
            "name": "SR-DB-SERVERS",
            "vlan_number": "101",
            "status": "active",
            "assg_ports": ["Eth1/10"],
        },
        {
            "name": "SR-LAB-0",
            "vlan_number": "110",
            "status": "active",
            "assg_ports": [],
        },
        {
            "name": "SR-MGMT-1",
            "vlan_number": "254",
            "status": "active",
            "assg_ports": ["Eth1/7", "Eth1/8", "Eth1/11"],
        },
    ]

    # Perform set theory intersection of intended vs actual
    vlan_updates = vlan_diff(int_vlan_list, run_vlan_dict)
    pprint.pprint(vlan_updates)

    # Ensure there are 4 items in the list
    assert len(vlan_updates) == 4

    # Check the NOBODY VLAN results
    assert vlan_updates[0]["name"] == "NOBODY"
    assert vlan_updates[0]["status"] == "active"
    assert vlan_updates[0]["vlan_number"] == "211"
    assert len(vlan_updates[0]["del_assg_ports"]) == 1
    assert vlan_updates[0]["del_assg_ports"][0] == "Eth1/15"
    assert vlan_updates[0]["add_assg_ports"] == []

    # Check the SR-DB-SERVERS VLAN results
    assert vlan_updates[1]["name"] == "SR-DB-SERVERS"
    assert vlan_updates[1]["status"] == "active"
    assert vlan_updates[1]["vlan_number"] == "101"
    assert len(vlan_updates[1]["add_assg_ports"]) == 1
    assert vlan_updates[1]["add_assg_ports"][0] == "Eth1/10"
    assert vlan_updates[1]["del_assg_ports"] == []

    # Check the SR-LAB-0 VLAN results
    assert vlan_updates[2]["name"] == "SR-LAB-0"
    assert vlan_updates[2]["status"] == "active"
    assert vlan_updates[2]["vlan_number"] == "110"
    assert len(vlan_updates[2]["del_assg_ports"]) == 2
    vlan_updates[2]["del_assg_ports"] = ["Eth1/23", "Eth1/35"]
    assert vlan_updates[2]["del_assg_ports"][1] == "Eth1/35"
    assert vlan_updates[2]["del_assg_ports"][0] == "Eth1/23"
    assert vlan_updates[2]["add_assg_ports"] == []

    # Check the SR-MGMT-1 VLAN results
    assert vlan_updates[3]["name"] == "SR-MGMT-1"
    assert vlan_updates[3]["status"] == "active"
    assert vlan_updates[3]["vlan_number"] == "254"
    assert len(vlan_updates[3]["add_assg_ports"]) == 3
    assert vlan_updates[3]["add_assg_ports"][0] == "Eth1/7"
    assert vlan_updates[3]["add_assg_ports"][1] == "Eth1/8"
    assert vlan_updates[3]["add_assg_ports"][2] == "Eth1/11"
    assert vlan_updates[3]["del_assg_ports"] == []


def _check_vlan_data(vlan_data):
    """
    Common asserts for all parsers
    """

    # Returned dict should have exactly 6 keys
    assert len(vlan_data) == 6

    # Ensure VLAN NOBODY parsing succeeded
    assert len(vlan_data["NOBODY"]["assg_ports"]) == 0
    assert vlan_data["NOBODY"]["status"] == "active"
    assert vlan_data["NOBODY"]["vlan_number"] == "211"

    # Ensure VLAN SR-DB-SERVERS parsing succeeded
    assert len(vlan_data["SR-DB-SERVERS"]["assg_ports"]) == 1
    assert vlan_data["SR-DB-SERVERS"]["assg_ports"][0] == "Eth1/10"
    assert vlan_data["SR-DB-SERVERS"]["status"] == "active"
    assert vlan_data["SR-DB-SERVERS"]["vlan_number"] == "101"

    # Ensure VLAN SR-LAB-0 parsing succeeded
    assert len(vlan_data["SR-LAB-0"]["assg_ports"]) == 0
    assert vlan_data["SR-LAB-0"]["status"] == "active"
    assert vlan_data["SR-LAB-0"]["vlan_number"] == "110"

    # Ensure VLAN SR-MGMT-1 parsing succeeded
    assert len(vlan_data["SR-MGMT-1"]["assg_ports"]) == 3
    assert vlan_data["SR-MGMT-1"]["assg_ports"][0] == "Eth1/7"
    assert vlan_data["SR-MGMT-1"]["assg_ports"][1] == "Eth1/8"
    assert vlan_data["SR-MGMT-1"]["assg_ports"][2] == "Eth1/11"
    assert vlan_data["SR-MGMT-1"]["status"] == "active"
    assert vlan_data["SR-MGMT-1"]["vlan_number"] == "254"

    # Ensure VLAN TEST parsing succeeded
    assert len(vlan_data["TEST"]["assg_ports"]) == 0
    assert vlan_data["TEST"]["status"] == "active"
    assert vlan_data["TEST"]["vlan_number"] == "222"

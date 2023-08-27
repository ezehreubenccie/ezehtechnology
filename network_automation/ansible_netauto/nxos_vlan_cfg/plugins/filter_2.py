#!/usr/bin/env python3


import re
import pprint
import regex


class FilterModule:
    @staticmethod
    def filters():
        return {"nxos_vlans": FilterModule.nxos_vlans}

    @staticmethod
    def nxos_vlans(text):
        #print(text)
        lines = regex.split("\n(?=[^\s])", text)
        #pprint.pprint(lines)
        lines = lines[2:]
        return_dict = {}
        for line in lines:
            name_regex = re.compile(r'\d{1,3}\s+(?P<vlan_name>\S+)')
            name_match = name_regex.search(line)
            #print(name_match)
            sub_dict = {}
            vlan_dict = {name_match.group('vlan_name'): sub_dict}
            #pprint.pprint(vlan_dict)

            # Parse assigned ports
            port_regex = re.compile(r'(?P<assn_ports>Eth\d{1,3}\/\d{1,3})')
            port_matches = port_regex.findall(line)
            sub_dict.update({'assg_ports': port_matches})
            #print(sub_dict)

            # Parse vlan status
            status_regex = re.compile(r'(?P<status>active|suspended|act\/lshut)')
            status_matches = status_regex.search(line)
            sub_dict.update({'status': status_matches.group('status')})
            #print(sub_dict)

            # Parse vlan id
            vlan_id_regex = re.compile(r'\d{1,3}')
            vlan_id_matches = vlan_id_regex.search(line)
            #print(vlan_id_matches.group())
            sub_dict.update({'vlan_number': vlan_id_matches.group()})
            #print(sub_dict)

            # Append dictionary to return list
            return_dict.update(vlan_dict)

        return return_dict
        
    @staticmethod
    def vlan_diff(int_vlan_list, run_vlan_dict):
        """
        Uses set theory to determine the vlans that
        should be added or deleted. Only differences are 
        captured, which helps Ansible achieve idempotence
        when making configuration updates.
        """
        return_list = []
        for int_vlan in int_vlan_list:
            # Copy benign parameters from intended config
            vlan_dict = {
                'name': int_vlan['name'],
                'vlan_id': int_vlan['vlan_id'],
                'state': int_vlan['state']
            }

            # If the intended VRF exists in the running config
            run_vlan = run_vlan_dict.get(str(int_vlan['name']))
            if run_vlan:
                # Convert each list to a set
                int_assg_ports = set(int_vlan[])        

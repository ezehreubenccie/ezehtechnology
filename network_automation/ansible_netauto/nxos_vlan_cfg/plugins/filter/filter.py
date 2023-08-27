#!/usr/bin/env python3


import re
import pprint
import regex
import json

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
        
        return_dict_str = json.dumps(return_dict)
        return_dict_json = json.loads(return_dict_str)
        pprint.pprint(return_dict_json)
       # pprint.pprint(json.loads(return_dict_str))
#        return return_dict
        return return_dict_json
            
           

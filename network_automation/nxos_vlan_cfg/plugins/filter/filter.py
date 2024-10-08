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
        pprint.pprint(lines)
        lines = lines[2:]
        for line in lines:
            name_regex = re.compile(r'\d{1,3}\s+(?P<vlan_name>\S+)')
            name_match = name_regex.search(line)
            #print(name_match)
            sub_dict = {}
            vlan_dict = {name_match.group('vlan_name'): sub_dict}
            pprint.pprint(vlan_dict)

            # Parse assigned ports
            port_regex = re.compile(r'(?P<assn_ports>Eth\d{1,3}\/\d{1,3})')
            port_matches = port_regex.findall(line)
            sub_dict.update({'assg_ports': port_matches})
            print(sub_dict)
        #return text
        
            
           

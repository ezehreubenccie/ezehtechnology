#!/usr/bin/env python3

import re
import pprint






def ios_vrf_rt(text):
        """
        Parses blocks of VRF text into indexable dictionary entries. This
        typically feeds into the rt_diff function to be tested against the
        intended config.
        """
        pprint.pprint(text.split('vrf'))
        print()
#        vrf_list = []
#        for s in text.split('vrf'):
#          if s != '"':
#              vrf_list.append('vrf' + s)
        vrf_list = ['vrf' + s for s in text.split('vrf') if s]
        return_dict = {} 
        pprint.pprint(vrf_list)
        #vrf_list = ['vrf' + s for s in text.split('vrf') if s]
        #vrf_list = vrf_list[1:]
        for vrf in vrf_list:
            print()
            print(vrf)
            # Parse the VRF name from the definition line
            name_regex = re.compile(r'vrf\s+definition\s+(?P<name>\S+)')
            name_match = name_regex.search(vrf)
            print(name_match.group('name'))
            sub_dict = {}
            vrf_dict = {name_match.group('name'): sub_dict}
        #pprint.pprint(vrf_dict)
        #print()
        
            # Parse the RT imports into a list of strings
            rti_regex = re.compile(r'route-target\s+import\s+(?P<rti>\d+:\d+)')
            rti_matches = rti_regex.findall(vrf)
            sub_dict.update({'route_import': rti_matches})
            
            # Parse the RT exports into a list of strings
            rte_regex = re.compile(r'route-target\s+export\s+(?P<rte>\d+:\d+)')
            rte_matches = rte_regex.findall(vrf)
            sub_dict.update({'route_export': rte_matches})

            # Append dictionary to return list
            return_dict.update(vrf_dict)
        print()
        pprint.pprint(return_dict)
        return return_dict
        
        #pprint.pprint(vrf_dict)
        
        
if __name__=="__main__":

    with open('vrf_out.txt', 'r') as f:
        text = f.read()
        
    #print(text)
        
    ios_vrf_rt(text)
        

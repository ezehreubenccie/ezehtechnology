#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Develop product model ID parsers for IOS-XE, ASA, FTD,
These are focused on just the model ID and not general information
"""

import re

def parse_model_ios(text):
    """
    Parses the model ID from the IOS 'show version' command
    if no match is found, None is returned. Sample:
    cisco WS-C4510R+E (P5040) processor (revision 2) with 4194304K bytes of physical memory.
    """
    model_regex = re.complile(r'cisco\s+(?P<model>\S+)\s+\(\S+\)\s+processor\s+')
    # Attempt to match the regex against the specific input.
    model_match = model_regex.search(text) 
    if model_match:
        return model_match.group("model")

    # No match was found
    return None

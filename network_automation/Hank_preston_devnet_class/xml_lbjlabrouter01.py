#!/usr/bin/env python

import xmltodict
from pprint import pprint


with open('xml_response_lbjlabrouter01.xml') as f:
    xml_data = f.read()
#print(xml_data)

xml_dict = xmltodict.parse(xml_data)
pprint(xml_data)

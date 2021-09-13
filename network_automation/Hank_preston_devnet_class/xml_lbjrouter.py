#!/usr/bin/env python

import xmltodict
from pprint import pprint


with open('lbjrouter01_xml.xml') as f:
    xml_data = f.read()
#print(xml_data)

xml_dict = xmltodict.parse(xml_data)
pprint(xml_data)

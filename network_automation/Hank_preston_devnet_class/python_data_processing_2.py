#!/usr/bin/env python


#XML
#print('Treat XML like Python Dictionaries with xmltodict\n\n')
import xmltodict
from pprint import pprint

with open('xml_example.xml') as f:
    xml_data = f.read()
#pprint(xml_data)

xml_dict = xmltodict.parse(xml_data)
pprint(xml_dict)
intf_name = xml_dict['interface']['name']
#print(intf_name)
#print('\n\n')
#print(xmltodict.unparse(xml_dict))

#print('\n\n')

#JSON
#print('To JSON and back again with json\n\n ')
import json
from pprint import pprint

with open('json_example.json') as f:
    json_data = f.read()
#pprint(json_data)

json_python = json.loads(json_data)
#pprint(json_python)
intf_name = json_python['ietf-interfaces:interface']['name']
#print(intf_name)

#print(json.dumps(json_python))

#YAML
#print('YAML? Yep, Python Can Do That Too!\n\n')
import yaml
from pprint import pprint

with open('yaml_example.yaml') as f:
    yml_data = f.read()
#pprint(yml_data)

yaml_python = yaml.safe_load(yml_data)
#pprint(yaml_python)
#intf_name = yaml_python['ietf-interfaces:interface']['name']
#print(intf_name)

#print(yaml.dump(yaml_python))

#print('\n\n')

#CSV
print("Import Spreadsheets and Data with csv\n")
import csv 
from pprint import pprint 

with open("csv_example.csv") as f:
    csv_data = f.read() 
#pprint(csv_data)

csv_data = open("csv_example.csv")
csv_python = csv.reader(csv_data)
#print(csv_python)
#print(type(csv_python))
for row in csv_python: 
#    print(row)
    print("{} is in {}, {} and has IP {}.".format(row[0].upper(), row[2], row[3], row[1]))



#!/usr/bin/env python

import yaml
from pprint import pprint

with open('seattle_firewall.yml') as f:
    yml_data = f.read()
#pprint(yml_data)

yaml_python = yaml.safe_load(yml_data)
#pprint(yaml_python)

print(yaml.dump(yaml_python))

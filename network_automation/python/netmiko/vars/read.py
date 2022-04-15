#!/usr/bin/env python

import yaml
with open('example.yml') as f:
    result = yaml.safe_load(f)
    print(result)
    type(result)


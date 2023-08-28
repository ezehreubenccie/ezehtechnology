#!/usr/bin/env python3

from nornir.core.inventory import Host
import json

print(json.dumps(Host.schema(), indent=4))


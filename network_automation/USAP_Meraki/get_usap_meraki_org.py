#!/usr/bin/env python

import meraki
from pprint import pprint
import os

key = os.getenv('MERAKI_DASHBOARD_API_KEY') 
dashboard = meraki.DashboardAPI(key)


usap_meraki_org = dashboard.organizations.getOrganizations()

print(usap_meraki_org)

#!/usr/bin/env python3

#import pprint

#import pandas

import pandas as pd

read_file = pd.read_csv (r'NY_rule_hit_export_1.txt')
read_file.to_csv (r'NY_rule_hit_export_3.csv', index=None)

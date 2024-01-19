#!/usr/bin/env python3

import pandas as pd

df = pd.read_fwf('NY_rule_hit_export.txt')
df.to_csv('NY_rule_hit_export.csv')

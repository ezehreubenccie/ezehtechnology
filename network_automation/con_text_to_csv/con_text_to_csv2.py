#!/usr/bin/env python3

import csv


with open('NY_rule_hit_export.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('NY_rule_hit_export.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('RuleID', 'Hit Count', 'First Hit Time(EST)', 'Last Hit Time(EST)'))
        writer.writerows(lines)

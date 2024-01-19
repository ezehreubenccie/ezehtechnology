#!/usr/bin/env python3



import csv
import itertools

with open('NY_rule_hit_export.txt', 'r') as in_file:
    lines = in_file.read().splitlines()
    stripped = [line.replace(","," ").split() for line in lines]
    grouped = itertools.izip(*[stripped]*1)
    with open('NY_rule_hit_export.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('RuleID', 'Hit Count', 'First Hit Time(EST)', 'Last Hit Time(EST)'))
        for group in grouped:
            writer.writerows(group)

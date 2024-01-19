#!/usr/bin/env python3

import pprint
import csv


with open('NY_rule_hit_export.txt', 'r') as handle:
    lines = handle.read().splitlines()

list1 = []
#pprint.pprint(lines[2:])
for line in lines[2:]:
    #print(line.split())
    list1.append(line.split())

#pprint.pprint(list1)
#print(len(list1))
#print(list1)

NY_rule_hits = open("NY_rule_hit_export_6.csv", "a")
NY_rule_hits.write("RuleID,Hit Count,First Hit Time(EST),Last Hit Time(EST)\n")
for item in list1:
    slice1 = ",".join(item[0:2])
    slice2 = " ".join(item[2:6])
    slice3 = " ".join(item[6:])
    
    item = slice1 + "," + slice2 + "," + slice3
    NY_rule_hits.write(f"{item}\n")
    

    #print(item)
NY_rule_hits.close()

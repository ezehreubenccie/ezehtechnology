#!/usr/bin/env

#CSV
print('Import Spreadsheets and Data With csv\n\n')
import csv
from pprint import pprint

with open('csv_example.csv', 'r') as f:
    csv_data = f.read()
#pprint(csv_data)

csv_python = csv.reader(csv_data)
#print(csv_python)
#print(type(csv_python))
for row in csv_python:
    print(row)
#    print('{} is in {}, {} and has IP {}.'.format(row[0], row[2], row[3], row[1]))

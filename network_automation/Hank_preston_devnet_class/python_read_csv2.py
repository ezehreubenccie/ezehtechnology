print("Import Spreadsheets and Data with csv\n\n")
import csv 
from pprint import pprint 

csv_example = open("csv_example.csv").read() 
pprint(csv_example)

csv_example = open("csv_example.csv")
csv_python = csv.reader(csv_example)
print(csv_python)
print(type(csv_python))
for row in csv_python: 
    print(row)
#    print("{} is in {} and has IP {}.".format(row[0], row[2], row[1]))

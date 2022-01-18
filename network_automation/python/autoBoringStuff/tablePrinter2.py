#!/usr/bin/env python3

import copy

tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose'],
             ['Reuben', 'Hannah', 'Jaden', 'Naomi']]








def printTable(data, row):
    colWidths = [0] * len(data)
    listItemLen = copy.deepcopy(data) 
    for i in range(len(listItemLen)):
        for j in range(len(listItemLen[i])):
            listItemLen[i][j] = len(listItemLen[i][j])
#    print(listItemLen)
        colWidths[i] = max(listItemLen[i])
#    print(colWidths) 
        
    for k in range(row):
        for l in range(len(data)):
            print(data[l][k].rjust(colWidths[l]), end=' ') 
        print()

printTable(tableData, 4)

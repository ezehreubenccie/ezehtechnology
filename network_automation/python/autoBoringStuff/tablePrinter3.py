#!/usr/bin/env python3

import copy


def printTable(data, row):
    colWidths = [0] * len(data)
    listItemLen = copy.deepcopy(data) 
    for i in range(len(listItemLen)):
        for j in range(len(listItemLen[i])):
            listItemLen[i][j] = len(listItemLen[i][j])
        colWidths[i] = max(listItemLen[i])

    for k in range(row):
        for l in range(len(data)):
            print(data[l][k].rjust(colWidths[l]), end=' ') 
        print()


if __name__=='__main__':
    tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose'],
             ['Reuben', 'Hannah', 'Jaden', 'Naomi']]

    printTable(tableData, 4)

#!/usr/bin/env python3


import random

list1 = []
slice = []
count = 0
streak = 0

for experimentNumber in range(10000):
    print(f'experimentNumber is: {experimentNumber}') # Print out experimentNumber
    for i in range(100):
        if random.randint(0, 1) == 0:
            list1.append('H')
        else:
            list1.append('T')
    print(list1)
    print(len(list1))
    while len(list1) >= 6:
        slice = list1[:6]
        print('Slice is:')
        print(slice)
        list1 = list1[6:]
        count = slice.count('H')
        print(count)
        if count == 6:
            streak += 1
        else:
            continue
print(f'Chance of streak: {streak / 100}%')
print(f'Number of streaks is: {streak}')

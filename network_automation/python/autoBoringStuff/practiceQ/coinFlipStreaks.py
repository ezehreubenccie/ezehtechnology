#!/usr/bin/env python3


import random

list1 = []
for i in range(100):
    if random.randint(0, 1) == 0:
        list1.append('H')
    else:
        list1.append('T')
#print(list1)
#print(len(list1))

slice = []
count = 0
streak = 0
while len(list1) >= 6:
    slice = list1[:6]
    print('Slice is:')
    print(slice)
    list1 = list1[6:]
    count = slice.count('H')
    if count == 6:
        streak += 1
    else:
        continue
#    print()
#    list1 = list1[6:]
#    print('list1 is:')
#    print(list1)
#    print(f'list1 length is: {len(list1)}')
print(streak)

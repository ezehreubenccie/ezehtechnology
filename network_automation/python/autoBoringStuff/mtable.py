#!/usr/bin/env python3


num = 1
for j in range(1, 13):
    print(f'Multiplication table for {j}')
    print('-' * 30)
    for i in range(12):
        print(f'{j} x {(i + 1)} = {j * (i + 1)}')
    print('-' * 30)

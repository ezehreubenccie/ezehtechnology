#!/usr/bin/env python

import sys

def doubler(number):
    number = number * 2
    return number


if __name__== '__main__':
    try:
        input = float(sys.argv[1])
    except (IndexError, ValueError) as e:
        print('You must provide a number as a parameter to this script.')
        print('Example: ')
        print('    python3 acceptSysInput.py 45')
        sys.exit(1)

    answer = doubler(input)
    print(answer)

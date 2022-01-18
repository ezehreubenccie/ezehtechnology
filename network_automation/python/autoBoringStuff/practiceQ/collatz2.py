#!/usr/bin/env python3


def collatz(number):
    if number % 2 == 0:
        return number // 2
    if number % 2 == 1:
        return 3 * number + 1


if __name__ == '__main__':
    
    print('Enter a number:')
    while True:
        number = input()
        try:
            number = int(number)
        except ValueError:
            print('Error: You must enter an integer.')
            continue
        result = collatz(number)
        if result == 1:
            break
    print(f'Looks like {result} was returned.')


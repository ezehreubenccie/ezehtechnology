#!/usr/bin/env python

# Counting Program
# Demonstrates counting by offset - eg by 5

# Enter starting number 
startNumber = int(input("Enter starting number: "))

# Enter ending number
endNumber = int(input("Enter ending number: "))

# Enter offset number - eg count by 5s, 10s, 2s etc
offsetNumber = int(input("Enter offset number: "))

for number in range(startNumber, endNumber, offsetNumber):
    print(number)

input("\n\nPress the enter key to exit.")
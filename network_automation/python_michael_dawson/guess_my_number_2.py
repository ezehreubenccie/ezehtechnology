#!/usr/bin/env python

# Guessing Game
#

import random

secretNumber = random.randint(1, 100)

print("I am thinking of a number between 1 and 100")

playerGuess = int(input("Take a guess: "))

if playerGuess == secretNumber:
    print("correct! the number is ", secretNumber )
elif playerGuess > secretNumber:
    print("lower..." )
elif playerGuess < secretNumber:
    print("higher...")
else:
    print("Wrong Number!")

input("\n\nPress the enter key to exit.")
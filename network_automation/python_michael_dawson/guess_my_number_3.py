#!/usr/bin/env python

# Guessing Game
#

import random

secretNumber = random.randint(1, 100)

print("I am thinking of a number between 1 and 100")

playerGuess = int(input("Take a guess: "))

while playerGuess != secretNumber:
    if playerGuess > secretNumber:
        print("Lower...")
    if playerGuess < secretNumber:
        print("Higher...")

    playerGuess = int(input("Take a guess: "))

print(playerGuess, "was the right number!")

input("\n\nPress the enter key to exit.")
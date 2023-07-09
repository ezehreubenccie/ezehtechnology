#!/usr/bin/env python

# Word Jumble
#
# The computer picks a random word and then "Jumbles" it
# The player has to guess the original word

import random

# create a sequence of words to choose from
WORDS = ("python", "jumble", "easy", "difficult", "answer", "xylophone")

# pick one word randomly from sequence
word = random.choice(WORDS)

# create a variable to use later to see if the guess is correct
correct = word

# create a jumbled version of the word
jumble = ""

# set up the loop
while word:

    # generating a random position in word
    position = random.randrange(len(word))

    # so the letter word[position] is going to be extracted
    # from word and added to jumble

    # create a new version of jumble
    # the next line in the loop creates a new version of the 
    # string jumble. it becomes equal to its old self, plus the 
    # letter word[position] 

    jumble += word[position]

    # create a new version of word
    word = word[:position] + word[(position + 1):]

# start the game
print(
"""
        Welcome to Word Jumble!

    Unscramble the letters to make a word
(Press the enter key at the prompt to quit.)
"""
)

print("The jumble is:", jumble)

# getting the players guess
guess = input("\nYour guess: ")
while guess != correct and guess != "":
    print("Sorry, that's not it.")
    guess = input("Your guess: ")

if guess == correct:
    print("That's it! You guessed it!\n")

# End the game
print("Thanks for playing")

input("\n\nPress the enter key to exit.")
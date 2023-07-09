#!/usr/bin/env python

# Word Jumble
#
# The computer picks a random word and then "Jumbles" it
# The player has to guess the original word

import random

# create a sequence of words to choose from
#WORDS = ("python", "jumble", "easy", "difficult", "answer", "xylophone")
WORDS = {"python": "number 1 programming language", "jumble": "confuse",
         "difficult": "tough", "answer": "response", "confuse": "puzzle"}
# pick one word randomly from sequence
word = random.choice(list(WORDS.keys()))

# create a variable to use later to see if the guess is correct
correct = word
hint = word
score = 0
response = ""

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
#score += 5
while guess != correct and guess != "":
    print("Sorry, that's not it.")
    response = input("\nNeed a hint?(yes/no):")
    if response == "yes" or response == "y":
        print("Your hint is: ", WORDS[hint])
        guess = input("Your guess: ")
    else:
        guess = input("Your guess: ")
        #score += 5

    #guess = input("Your guess: ")

if guess == correct and (response == "yes" or response == "y"):
    print("That's it! You guessed it!\n")
    print("Your score is,", score)
elif guess == correct and (response == "no" or response == "n"):
    print("That's it! You guessed it!\n")
    print("Your score is,", score + 5)
elif guess == correct and response == "":
    print("That's it! You guessed it!\n")
    print("Your score is,", score + 5)

# End the game
print("Thanks for playing")

input("\n\nPress the enter key to exit.")
#!/usr/bin/env python

import random

WORDS = ("python", "jumble", "easy", "difficult", "answer", "xylophone")

word = random.choice(WORDS)
numberOfChances = 0
letter = ""
playerGuessedLetters = ""
new_word = word


print("The word I am thinking about has: ", len(new_word), " letters in it.")

print("\nYou have five chances to ask if a letter is in the word:")

for chances in range(1, 6):
    print(chances, " Attempt: ")
    letter = input()
    #letterPosition = word.index(letter)
    
    if letter in new_word:
        print("yes")
        letterPosition = new_word.index(letter)
        new_word = new_word[:letterPosition] + new_word[(letterPosition + 1):]
    else:
        print("no")
    
    
    
    playerGuessedLetters += letter

print("\nYour guessed letters are: ", playerGuessedLetters)

guess = input("\nYour guess: ")
if guess == word:
    print("That's it! You guessed it!\n")
else:
    print("Wrong Guess!, The word is", word)

print("Thanks for playing!")

input("\n\nPress the enter key to exit.")
    

